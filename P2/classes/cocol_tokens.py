
from numpy import fromregex
from classes.alphabet import Alphabet
from classes.dtypes import VarType
import string
from classes.expression import Expression
from classes.nfa import NFA
from classes.state import State
from classes.symbol import Symbol

EPSILON = Symbol('ε')

class CocolProcessor:

    def __init__(self) -> None:
        self.nfa = None
        self.dfas = []
        self.final_states = {}
        self.dfa = None


    def build_dfa(self, exp, name):
        root = exp.anlyze_build_tree()
        leafs, nodes = root.build_firstlast_pos()
        followpos = root.followpos(leafs, nodes)
        ddfa = root.build_direct_DFA(exp.alphabet.get_alphabet(), followpos, leafs)
        self.dfas.append(
            ddfa
        )
        self.final_states[ddfa.final_states[0]] = name

        if self.nfa == None:
            init_state = State(is_init=True)
            final_state = State(is_terminal=True)
            states = ddfa.states + [init_state, final_state]
            trans_func = ddfa.trans_func
            self.nfa = NFA(states,
                        ddfa.alphabet,
                        init_state,
                        trans_func, [final_state])
            self.nfa.add_transition(init_state, 
                                    ddfa.init_state,
                                    EPSILON)
            
            self.nfa.add_transition(ddfa.final_states[0],
                                    final_state,
                                    EPSILON)

        else:
            for from_s in ddfa.trans_func.keys():
                for symbol in ddfa.trans_func[from_s]:
                    to_states = ddfa.trans_func[from_s][symbol]
                    for to_state in to_states:
                        self.nfa.add_transition(
                            from_s,
                            to_state,
                            symbol
                        )
                    
            init_state = self.nfa.init_state
            final_state = self.nfa.final_states[0]
            self.nfa.add_transition(init_state, ddfa.init_state, EPSILON)
            self.nfa.add_transition(ddfa.final_states[0], final_state, EPSILON)

    def generate_dfas(self):
        open_quote_mark = "«"
        open_par = "܆"
        close_par = "܇"
        plus = "܀"
        
        letter = " | ".join([str(ord(ch)) for ch in string.ascii_letters])
        letter = letter.split(" ")
        
        digit = " | ".join([str(ord(d)) for d in string.digits])
        digit = digit.split(" ")
        
        any_but_quote = " | ".join([str(ord(s)) for s in string.printable.replace('"', "")])
        any_but_quote = any_but_quote.split(" ")

        any_but_apostrophe = " | ".join([str(ord(s)) for s in string.printable.replace("'", "")])
        any_but_apostrophe = any_but_apostrophe.split(" ")

        ident = ['('] + letter + [')'] + ['('] + letter + ['|'] + digit + [')'] + ['*']
        ident = Expression(ident, is_extended=True)

        number = ['('] + ['('] + digit + [')'] + ['(']+ digit + [')'] + ['*'] + [')']
        number = Expression(number, is_extended=True)

        String = [str(ord('"'))] + ['('] + any_but_quote + [')'] + ['*'] + [str(ord('"'))]
        String = Expression(String, is_extended=True)

        char = [str(ord("\\"))] + [str(ord("'"))] + ['('] + any_but_apostrophe + [')'] + [str(ord("\\"))] + [str(ord("'"))]
        char = Expression(char, is_extended=True)

        chardf = [str(ord("C")), str(ord("H")), str(ord("R")), str(ord("("))] 
        chardf = Expression(chardf, is_extended=True)

        lbrack = Expression([str(ord('{'))], is_extended=True)

        rbrack = Expression([str(ord('}'))], is_extended=True)

        union = Expression([str(ord('+'))], is_extended=True)

        diff = Expression([str(ord('-'))], is_extended=True)

        _range = Expression([str(ord('.')), str(ord('.'))], is_extended=True)

        lpar = Expression([str(ord('('))], is_extended=True)

        rpar = Expression([str(ord(')'))], is_extended=True)

        self.build_dfa(ident, VarType.IDENT)
        self.build_dfa(number, VarType.NUMBER)
        self.build_dfa(String, VarType.STRING)
        self.build_dfa(char, VarType.CHAR)
        self.build_dfa(lbrack, VarType.LBRACKET)
        self.build_dfa(rbrack, VarType.RBRACKET)
        self.build_dfa(union, VarType.UNION)
        self.build_dfa(diff, VarType.DIFFERENCE)
        self.build_dfa(_range, VarType.RANGE)
        self.build_dfa(lpar, VarType.LPAR)
        self.build_dfa(rpar, VarType.RPAR)
        self.build_dfa(chardf, VarType.CHARDF)

        self.dfa = self.nfa.build_DFA(final_s = self.final_states)

    def format_set(self):
       pass
    
    def analyze(self, set_decl):
        
        tokens = []
        curr_idx = 0
        if '""' in set_decl:
            try:
                idx = set_decl.index('""')
                set_decl = set_decl[:idx] + '" "' + set_decl[idx+2:]
            except ValueError:
                set_decl = set_decl
        set_decl = [str(ord(i)) for i in set_decl]
        # print(set_decl)
        word = set_decl
        size = len(set_decl)
        while curr_idx < size:
            token, idx = self.dfa.get_token(word)
            tokens.append(token)
            curr_idx += idx
            word = set_decl[curr_idx:]

        return tokens



