from matplotlib import transforms
from classes.nfa import NFA
from classes.state import State
import numpy as np

from classes.symbol import Symbol

class Node:

    def __init__(self, value, left=None, right=None) -> None:
        self.value = value
        self.left = left
        self.right = right
        self.epsilon = Symbol('ε')
        self.operands = ['*', '+', '|', '?', '؞']
        self.nfa = None

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


    def postorder(self):
        
        data = []
        def _postorder(node):
            if node is None:
                return
            _postorder(node.left)
            _postorder(node.right)
            data.append(node.generate_NFA())

        _postorder(self)
        return data 
    
                    
    def __repr__(self) -> str:
        return f"{str(self.value)}"