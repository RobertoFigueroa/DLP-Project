
from classes.alphabet import Alphabet
from classes.state import State

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

    def move():
        pass

    def simulate():
        pass
    
    def add_transition():
        pass

    def remove_transition():
        pass