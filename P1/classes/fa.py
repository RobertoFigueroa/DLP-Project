
from classes.alphabet import Alphabet
from classes.state import State
from classes.symbol import Symbol
import networkx as nx
import matplotlib.pyplot as plt
import graphviz

class FA:



    def __init__(self,
                 states : list,
                 alphabet : list,
                 init_state: State,
                 trans_func: dict,
                 final_states: list) -> None:

        self.states = states  # List of states
        self.alphabet = alphabet  # List of symbols objects
        self.init_state = init_state, # Object state
        self.trans_func = dict(trans_func), # Dict-like function
        self.final_states = final_states # List of states
        self.epsilon = Symbol('ε')

    def move():
        pass

    def simulate():
        pass
    
    def add_transition():
        pass

    def simulate():
        pass

    def remove_transition():
        pass

    def get_image(self):
        graph = graphviz.Digraph("fa")  
        edges = []
        for state in self.states:
            graph.node(str(state), str(state))

        for state in self.states:
            if state in self.final_states:
                graph.node(str(state), _attributes = {'shape': 'doublecircle'})
            else:
                graph.node(str(state))

        for from_state in self.trans_func.keys():
            for symbol in self.trans_func[from_state].keys():
                for to_state in self.trans_func[from_state][symbol]:
                    graph.edge(str(from_state), str(to_state), label=str(symbol))

        graph.node('', _attributes={'shape' : 'plaintext'})
        graph.edge('', str(self.init_state))
        
        graph.render(directory=f"output/{repr(self)}", view=True)

