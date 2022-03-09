
from classes.alphabet import Alphabet


class FA(object):

    def __init__(self,
                 states,
                 alphabet,
                 init_state,
                 trans_func,
                 final_states) -> None:

        self.states = states  # List of states
        self.alphabet = alphabet  # List of symbols objects
        self.init_state = init_state, # Object state
        self.trans_func = trans_func, # Dict-like function
        self.final_states = final_states # List of states

    def move():
        pass

    def simulate():
        pass
    
    def add_transition():
        pass

    def remove_transition():
        pass