from re import S
from classes.nfa import NFA
from classes.state import State
import numpy as np

class Node:

    def __init__(self, value) -> None:
        self.value = value
        self.children = []

    def add_child(self, child : any) -> None:
        self.children.append(child)

    def get_children(self) -> list:
        return self.children

    def generate_alphabet_NFA(self) -> NFA:
        s1 = State(is_init=True)
        s2 = State(is_terminal=True)
        states = [s1, s2]
        trans_func = {
            s1: {self.value : [s2]}
        }

        return NFA(states, ['ε'], s1, trans_func, [s2])

    def generate_kleene_NFA(self, nfa : NFA) -> NFA:
        s1 = State(is_init=True)
        s2 = State(is_terminal=True)
        alphabet = []
        states = [s1,s2]
        trans_func = dict()
        states = states + nfa.states
        alphabet = alphabet + nfa.alphabet
        
       

        return NFA(states, alphabet, s1, trans_func, [s2])


    def generate_or_NFA(self, nfas : list) -> NFA:
            s1 = State(is_init=True)
            s2 = State(is_terminal=True)
            alphabet = []
            states = [s1,s2]
            trans_func = dict()
            for nfa in nfas:
                states = states + nfa.states
                alphabet = alphabet + nfa.alphabet
                for state in nfa.trans_func.keys():
                    trans_func[state] = nfa.trans_func[state]
                
                #Posbile bug, que sucede si ya existe una transicion del final a otro estado o a el mismo
                trans_func[nfa.final_states[0]] = {
                    'ε' : [s2]
                }

            trans_func[s1] = {
                'ε' : [nfa.init_state for nfa in nfas]
            }

            return NFA(states, alphabet, s1, trans_func, [s2])
                
    def __str__(self) -> str:
        return f"Value {str(self.value)} children {str(self.children)}"