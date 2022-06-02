from matplotlib import transforms
from classes.alphabet import Alphabet
from classes.fa import FA
from classes.dfa import DFA
from classes.nfa import NFA
from classes.state import State
import numpy as np

from classes.symbol import Symbol

class Node:

    def __init__(self, value, left=None, right=None, attribute=None) -> None:
        self.value = value
        self.left = left
        self.right = right
        self.epsilon = Symbol('ε')
        self.operands = ['*', '+', '|', '?', '؞']
        self.nfa = None
        self.is_leaf = False
        self.leaf_value = None
        self.null = None
        self.firstpos_ = None
        self.lastpos_ = None
        self.followpos_ = dict()
        self.attr = attribute
        self.instruction = None
        self.n_terminals = None
        self.leafs = None
        self.is_root = False

    def add_child(self, child : any) -> None:
        self.children.append(child)

    def get_children(self) -> list:
        return self.children

    def generate_NFA(self) -> None:
        if self.value == '|':
            self.nfa = self.generate_or_NFA()
        elif self.value == '*':
            self.nfa = self.generate_kleene_plus_NFA()
        elif self.value == '؞':
            self.nfa = self.generate_concat_NFA()
        elif self.value == '?':
            self.nfa = self.generate_qmark_NFA()
        elif self.value == '+':
            self.nfa = self.generate_plus_NFA()
        else:
            self.nfa = self.generate_alphabet_NFA()
        

    def generate_concat_NFA(self) -> NFA:
        init_state = self.left.nfa.get_init()
        final_state = self.right.nfa.get_final()
        states = [init_state, final_state]
        alphabet = []
        trans_func = dict()

        nfa = NFA(states, alphabet, init_state, trans_func, [final_state])

        #TODO: reemplazar el nodo para evitar esta transición epsilon
        nfa.add_transition(self.left.nfa.get_final(), self.right.nfa.get_init(), self.epsilon)

        for _nfa in [self.left.nfa, self.right.nfa]:
            for from_s in _nfa.trans_func.keys():
                for symb in _nfa.trans_func[from_s].keys():
                    for to_s in _nfa.trans_func[from_s][symb]:
                        nfa.add_transition(from_s, to_s, symb)

        
        return nfa


    def build_instructions(self, n_terminals : list):
        leafs = self.leafs # root leafs
        data = []
        def _postorder(node):
            if node is None:
                return
            _postorder(node.left)
            _postorder(node.right)
            data.append(node.generate_code(n_terminals, leafs))
        _postorder(self)
        return data

    def generate_code(self, n_terminals, leafs):
        if self.value == 'Ω':
            self.kleene_instruction(n_terminals, leafs)
        elif self.value == '|':
            self.or_instruction(n_terminals, leafs)
        elif self.value == '؞':
            self.concat_instruction(n_terminals, leafs)
        elif self.value == '?':
            self.question_instruction(n_terminals, leafs)
            pass
        else: #is terminal or non terminal node
            self.gen_instruction(n_terminals, leafs)

    def tab(self, instruction):
        result = []
        for i in instruction.split('\n'):
            result.append('\t'+i)
        
        return '\n'.join(result)
    
    def question_instruction(self, n_terminals, leafs):
        condition = []
        for i in self.left.firstpos_:
            if i.value in n_terminals:
                if i.attr:
                    condition.append(i.value+f"({i.attr})")
                else:
                    condition.append(i.value+"()")
            else:
                condition.append(i.value)
        inst = f"""
if self.current_token.value in {condition} or self.curren_token.ident in {condition}:
{self.tab(self.left.instruction)}"""

        self.instruction = inst

    def gen_instruction(self, n_terminals, leafs):
        if self.value in n_terminals and not self.is_root:
            self.instruction = f"{self.attr + '=' if self.attr  else ''}" + "self." + self.value + f"({self.attr if self.attr else ''})"
        elif self.value in n_terminals and self.is_root:
            self.instruction = "def "+self.value+f"(self,{self.attr if self.attr else ''}):"
            self.instruction = self.instruction + self.tab(self.left.instruction) + self.tab(f"\nreturn {self.attr}")
            self.instruction = "\n" + self.tab(self.instruction)
        else:
            if "(." in self.value:
                inst = self.value
                inst = inst.replace("(.", "")
                inst = inst.replace(".)", "")
                inst = inst.strip()
                self.instruction = inst
            else:
                self.instruction = f"self.expect({self.value})"

    def concat_instruction(self, n_terminals, leafs):
        inst = f"""
{self.left.instruction}
{self.right.instruction}"""
        self.instruction = inst

    def or_instruction(self, n_terminals,leafs):
        condition1 = []
        if self.left:
            for i in self.left.firstpos_:
                if i.value in n_terminals:
                    if i.attr:
                        condition1.append(i.value+f"({i.attr})")
                    else:
                        condition1.append(i.value+"()")
                else:
                    condition1.append(i.value)
        condition2 = []
        if self.right:
            for i in self.right.firstpos_:
                if i.value in n_terminals:
                    if i.attr:
                        condition2.append(i.value+f"({i.attr})")
                    else:
                        condition2.append(i.value+"()")
                else:
                    condition2.append(i.value)
        inst = f"""
if self.current_token.value in {condition1} or self.curren_token.ident in {condition1}:
{self.tab(self.left.instruction)}
elif self.current_token.value in {condition2} or self.curren_token.ident in {condition2}:
{self.tab(self.right.instruction)}
else:
{self.tab("print('Error sintáctico')")}
{self.tab("return 0")}"""
        self.instruction = inst  

    def kleene_instruction(self,n_terminals, leafs):
        condition = []
        for i in self.firstpos_:
            if i.value in n_terminals:
                if i.attr:
                    condition.append(i.value+f"({i.attr})")
                else:
                    condition.append(i.value+"()")
            else:
                condition.append(i.value)
        inst = f"""
while self.current_token.value in {condition} or self.current_token.ident in {condition}:
{self.tab(self.left.instruction)}"""
        self.instruction = inst



    def generate_alphabet_NFA(self) -> NFA:
        init_state = State(is_init=True)
        final_state = State(is_terminal=True)
        states = [init_state, final_state]
        alphabet = [Symbol(self.value)]
        trans_func = dict()
        nfa = NFA(states, alphabet, init_state, trans_func, [final_state])
        nfa.add_transition(from_state=init_state, to_state=final_state, symbol=alphabet[0])
        return nfa

    def generate_kleene_plus_NFA(self) -> NFA:
        init_state = State(is_init=True)
        final_state = State(is_terminal=True)
        alphabet = [self.epsilon]
        states = [init_state,final_state]
        trans_func = dict()
        nfa = NFA(states, alphabet, init_state, trans_func, [final_state])
        nfa.add_transition(init_state, final_state, self.epsilon)
        nfa.add_transition(init_state, self.left.nfa.get_init(), self.epsilon)
        self.left.nfa.add_transition(self.left.nfa.get_final(), self.left.nfa.get_init(), self.epsilon)
        self.left.nfa.add_transition(self.left.nfa.get_final(), final_state, self.epsilon)
        # merge trans func of both NFAs
        for from_s in self.left.nfa.trans_func.keys():
            for symb in self.left.nfa.trans_func[from_s].keys():
                for to_s in self.left.nfa.trans_func[from_s][symb]:
                    nfa.add_transition(from_s, to_s, symb)
        return nfa

    def generate_plus_NFA(self) -> NFA:
        init_state = State(is_init=True)
        final_state = State(is_terminal=True)
        alphabet = [self.epsilon]
        states = [init_state,final_state]
        trans_func = dict()
        nfa = NFA(states, alphabet, init_state, trans_func, [final_state])
        nfa.add_transition(init_state, self.left.nfa.get_init(), self.epsilon)
        self.left.nfa.add_transition(self.left.nfa.get_final(), self.left.nfa.get_init(), self.epsilon)
        self.left.nfa.add_transition(self.left.nfa.get_final(), final_state, self.epsilon)
        # merge trans func of both NFAs
        for from_s in self.left.nfa.trans_func.keys():
            for symb in self.left.nfa.trans_func[from_s].keys():
                for to_s in self.left.nfa.trans_func[from_s][symb]:
                    nfa.add_transition(from_s, to_s, symb)
        return nfa

    def generate_or_NFA(self) -> NFA:

        init_state = State(is_init=True)
        final_state = State(is_terminal=True)
        states = [init_state, final_state]
        alphabet = []
        states = [init_state,final_state]
        trans_func = dict()
        nfa = NFA(states, alphabet, init_state, trans_func, [final_state])
        for _nfa in [self.left.nfa, self.right.nfa]:
            if _nfa:
                nfa.add_transition(init_state, _nfa.get_init(), self.epsilon)
                _nfa.add_transition(_nfa.get_final(), final_state, self.epsilon)

                for from_s in _nfa.trans_func.keys():
                    for symb in _nfa.trans_func[from_s].keys():
                        for to_s in  _nfa.trans_func[from_s][symb]:
                            nfa.add_transition(from_s, to_s, symb)


        return nfa

    
    def generate_qmark_NFA(self) -> NFA:

        init_state = State(is_init=True)
        final_state = State(is_terminal=True)
        states = [init_state, final_state]
        alphabet = []
        states = [init_state,final_state]
        trans_func = dict()
        nfa = NFA(states, alphabet, init_state, trans_func, [final_state])
        nfa.add_transition(init_state, self.left.nfa.get_init(), self.epsilon)
        nfa.add_transition(init_state, final_state, self.epsilon)
        self.left.nfa.add_transition(self.left.nfa.get_final(), final_state, self.epsilon)

        for from_s in self.left.nfa.trans_func.keys():
            for symb in self.left.nfa.trans_func[from_s].keys():
                for to_s in self.left.nfa.trans_func[from_s][symb]:
                    nfa.add_transition(from_s, to_s, symb)


        return nfa
            
    def build_NFA(self):
        
        data = []
        def _postorder(node):
            if node is None:
                return
            _postorder(node.left)
            _postorder(node.right)
            data.append(node.generate_NFA())

        _postorder(self)
        return data

    def null_(self) -> bool:
        if self.value == self.epsilon:
            self.null = True
        elif self.value == '|':
            self.null = self.left.null or self.right.null
        elif self.value == '؞':
            self.null = self.left.null and self.right.null
        elif self.value == 'Ω':
            self.null = True
        elif self.value == '?':
            self.null = True # Existe la posiblidad de generar la cadena vacia
        elif self.value == '+':
            self.null = False # No existe posiblidad de generar la cadena vacia
        else:
            self.null = False

    def nullable(self) -> bool:
        if self.value == self.epsilon:
            self.null = True
        elif self.value == '|':
            self.null = self.left.null or self.right.null
        elif self.value == '؞':
            self.null = self.left.null and self.right.null
        elif self.value == '*':
            self.null = True
        elif self.value == '?':
            self.null = True # Existe la posiblidad de generar la cadena vacia
        elif self.value == '+':
            self.null = False # No existe posiblidad de generar la cadena vacia
        else:
            self.null = False
    
    def build_firstlast_pos(self) -> tuple:
        leafs = []
        nodes = []
        def _postorder(node):
            if node is None:
                return
            if not node.left and not node.right:
                node.leaf_value = len(leafs)
                leafs.append(node)
            _postorder(node.left)
            _postorder(node.right)
            node.nullable()
            node.firstpos()
            node.lastpos()
            nodes.append(node)
        _postorder(self)

        return leafs, nodes




    def build_null_first(self, n_terminals : list):
        leafs = []
        nodes = []
        def _postorder(node):
            if node is None:
                return
            if not node.left and not node.right:
                node.leaf_value = len(leafs)
                leafs.append(node)
            _postorder(node.left)
            _postorder(node.right)
            node.null_()
            node.first(n_terminals)
            #node.lastpos()
            nodes.append(node)
        _postorder(self)
        return leafs, nodes

    def firstpos(self) -> set:
        if self.value == self.epsilon:
            self.firstpos_ = set([])
        elif self.value == '|':
            self.firstpos_ = self.left.firstpos_.union(self.right.firstpos_)
        elif self.value == '؞':
            if self.left.null:
                self.firstpos_ = self.left.firstpos_.union(self.right.firstpos_)
            else:
                self.firstpos_ = self.left.firstpos_
        elif self.value == '*':
            self.firstpos_ = self.left.firstpos_
        elif self.value == '?':
            self.firstpos_ = self.left.firstpos_
        elif self.value == '+':
            self.firstpos_ = self.left.firstpos_
        else:
            self.firstpos_ = set([self.leaf_value])

    def first(self, n_terminals : list) -> set:
            if self.value == self.epsilon:
                self.firstpos_ = set([])
            elif self.value == '|':
                self.firstpos_ = self.left.firstpos_.union(self.right.firstpos_)
            elif self.value == '؞':
                if self.left.null:
                    self.firstpos_ = self.left.firstpos_.union(self.right.firstpos_)
                else:
                    self.firstpos_ = self.left.firstpos_
            elif self.value == 'Ω':
                self.firstpos_ = self.left.firstpos_
            elif self.value == '?':
                self.firstpos_ = self.left.firstpos_
            elif self.value == '+':
                self.firstpos_ = self.left.firstpos_
            else:
                for i in n_terminals:
                    if i.value == self.value:
                        self.firstpos_ = i.firstpos_
                        return
                self.firstpos_ = set([self])

    def lastpos(self):
        if self.value == self.epsilon:
            self.lastpos_ = set([])
        elif self.value == '|':
            self.lastpos_ =  self.left.lastpos_.union(self.right.lastpos_)
        elif self.value == '؞':
            if self.right.null:
                self.lastpos_ = self.left.lastpos_.union(self.right.lastpos_)
            else:
                self.lastpos_ = self.right.lastpos_
        elif self.value == '*':
            self.lastpos_ = self.left.lastpos_
        elif self.value == '?':
            self.lastpos_ = self.left.lastpos_
        elif self.value == '+':
            self.lastpos_ = self.left.lastpos_
        else:
            self.lastpos_ = set([self.leaf_value])

    def followpos(self, leafs : list, nodes : list) -> set:
        followpos_struct = {}
        for index, _ in enumerate(leafs):
            followpos_struct[index] = set([])
        for node in nodes:
            if node.value == '؞':
                for i in node.left.lastpos_:
                    followpos_struct[i] = followpos_struct[i].union(node.right.firstpos_)

            elif node.value == '*':
                for i in node.lastpos_:
                    followpos_struct[i] = followpos_struct[i].union(node.firstpos_)

        return followpos_struct
    
    def check_marked(self, dStates : list) -> State:
        for state in dStates:
            if state[0].mark == False:
                return state
        return None

    def in_dstates(self, U: set, dstates : list) -> bool:
        for state in dstates:
            if state[1] == U:
                return True
        
        return False

    def get_U_state(self, U, dstates):
        for state in dstates:
            if state[1] == U:
                return state[0] 
        return None


    def build_direct_DFA(self, alphabet : Alphabet, followpos : dict, leaf_nodes : list) -> None:
        dStates = []
        trans_func = dict()
        dStates.append((State(), self.firstpos_))
        unmarked_state = self.check_marked(dStates)
        while unmarked_state:
            unmarked_state[0].mark = True
            for symbol in alphabet:
                U = set()
                if symbol != self.epsilon:
                    indexes = [i for i,val in enumerate(leaf_nodes) if (val.value == str(symbol) and i in unmarked_state[1])]
                    # print("indexes: ", indexes, "symbol ", symbol)
                    for followpos_state in followpos.keys():
                        for s_index in indexes:
                            if followpos_state == s_index:
                                U = followpos[followpos_state].union(U)
                else:
                    continue
                if len(U) == 0:
                    continue
                if not self.in_dstates(U, dStates):
                    dStates.append((State(), U))

                state = self.get_U_state(U, dStates)

                # print(dStates)
                if unmarked_state[0] in trans_func.keys():
                    if symbol in trans_func[unmarked_state[0]].keys():
                        if state not in trans_func[unmarked_state[0]][symbol]:
                            trans_func[unmarked_state[0]][symbol].append(state)
                    else:
                        trans_func[unmarked_state[0]][symbol] = [state]

                else:
                    trans_func[unmarked_state[0]] = {symbol : [state]}

            unmarked_state = self.check_marked(dStates)

        end_index = [i for i,val in enumerate(leaf_nodes) if val.value == "፨" ]

        # print(dStates)

        final_states = []
        states = []

        for state in dStates:
            for index in state[1]:
                if index == end_index[0]:
                    final_states.append(state[0])
            states.append(state[0])

        new_alphabet = [i for i in alphabet if i != self.epsilon and i != "፨"]

        init_state = dStates[0][0]

        return DFA(states, new_alphabet, init_state, trans_func, final_states)
        

    def __repr__(self) -> str:
        return f"{str(self.value)}"


    def in_order(self, node): #left root right
        if node == None:
            return

        self.in_order(node.left)
        self.in_order(node.right)
        print(node.value)
