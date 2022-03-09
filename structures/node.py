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

    def add_child(self, child : any) -> None:
        self.children.append(child)

    def get_children(self) -> list:
        return self.children

    def generate_alphabet_NFA(self) -> NFA:
        init_state = State(is_init=True)
        final_state = State(is_terminal=True)
        states = [init_state, final_state]
        alphabet = [Symbol(self.value)]
        trans_func = {}
        nfa = NFA(states, alphabet, init_state, trans_func, [final_state])
        nfa.add_transition(from_state=init_state, to_state=final_state, symbol=alphabet[0])
        return nfa

    def generate_kleene_NFA(self, nfa : NFA) -> NFA:
        init_state = State(is_init=True)
        final_state = State(is_terminal=True)
        alphabet = [self.epsilon]
        states = [init_state,final_state]
        trans_func = dict()
        nfa = NFA(states, alphabet, init_state, trans_func, [final_state])
        nfa.add_transition(init_state, final_state, self.epsilon)
        nfa.add_transition(init_state, self.left.get_init(), self.epsilon)
        self.left.add_transition(self.left.get_final(), self.left.get_init(), self.epsilon)
        self.left.add_transition(self.left.get_final(), final_state, self.epsilon)
        # merge trans func of both NFAs
        for from_s in self.left.trans_func.keys():
            for symb in self.left.trans_func[from_s]:
                nfa.add_transition(from_s, self.left.trans_func[from_s][symb], symb)
        return nfa


    def generate_or_NFA(self) -> NFA:

        init_state = State(is_init=True)
        final_state = State(is_terminal=True)
        states = [init_state, final_state]
        alphabet = []
        states = [init_state,final_state]
        trans_func = dict()
        nfa = NFA(states, alphabet, init_state, trans_func, [final_state])
        for _nfa in [self.left, self.right]:
            if _nfa:
                nfa.add_transition(init_state, _nfa.get_init(), self.epsilon)
                _nfa.add_transition(_nfa.get_final(), final_state, self.epsilon)

        return nfa
                
    def __repr__(self) -> str:
        return f"{str(self.value)}"