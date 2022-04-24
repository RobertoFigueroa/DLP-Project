
from dtypes import VarType
import string
from expression import Expression
from nfa import NFA

class CocolProcessor:

    def __init__(self) -> None:
        self.nfa = None
        self.dfas = []
        self.final_states = {}


    def build_dfa(self, exp, name):
        root = exp.anlyze_build_tree()
        leafs, nodes = root.build_firstlast_pos()
        followpos = root.followpos(leafs, nodes)
        ddfa = root.build_direct_DFA(exp.alphabet.get_alphabet(), followpos, leafs)
        self.dfas.append(
            ddfa
        )
        self.final_states[ddfa.final_states[0]] = name

    def generate_dfas(self):
        open_quote_mark = "«"
        open_par = "܆"
        close_par = "܇"
        plus = "܀"
        
        letter = Expression([str(ord(ch)) for ch in string.ascii_letters])
        digit = Expression([str(ord(d)) for d in string.digits])
        any_but_quote = Expression([str(ord(s)) for s in string.printable.replace('"', "")])
        any_but_apostrophe = Expression([str(ord(s)) for s in string.printable.replace("'", "")])
        
        ident = ['('] + letter.string + [')'] + ['('] + letter.string + ['|'] + digit.string + [')'] + ['*']
        ident = Expression(ident)

        number = ['('] + ['('] + digit.string + [')'] + ['(']+ digit.string + [')'] + ['*'] + [')']
        number = Expression(number)

        String = [ord('"')] + ['('] + any_but_quote.string + [')'] + ['*'] + [ord('"')]
        String = Expression(String)

        char = [ord("\\")] + [ord("'")] + ['('] + any_but_apostrophe.string + [')'] + [ord("\\")] + [ord("'")]
        char = Expression(char)


        lbrack = Expression([ord('{')])

        rbrack = Expression([ord('}')])

        union = Expression([ord('+')])

        diff = Expression([ord('-')])

        _range = Expression([ord('.'), ord('.')])

        lpar = Expression([ord('(')])

        rpar = Expression([ord(')')])

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
        

    def format_set(self):
       pass
    
    def analyze(self, set_decl):
        tokens = None
        return tokens

    def join_dfas(self):
        
        trans_func = {}

        for dfa in self.dfas =


