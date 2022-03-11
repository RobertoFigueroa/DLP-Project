
from classes.alphabet import Alphabet
from classes.state import State
from classes.symbol import Symbol
import networkx as nx
import matplotlib.pyplot as plt

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

    def remove_transition():
        pass

    def get_image(self):
        automata = nx.Graph()  
        edges = []
        for from_state in self.trans_func.keys():
            for symbol in self.trans_func[from_state].keys():
                for to_state in self.trans_func[from_state][symbol]:
                    edges.append([from_state, to_state])
        
        automata.add_edges_from(edges)
        plt.axis('off')
        plt.savefig('fa.png')
