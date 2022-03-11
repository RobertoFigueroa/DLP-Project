from classes.fa import FA
from classes.state import State

class DFA(FA):


    def __init__(self, states: list, alphabet: list, init_state: State, trans_func: dict, final_states: list) -> None:
        super().__init__(states, alphabet, init_state, trans_func, final_states)
        
        self.trans_func = self.trans_func[0]
        self.init_state = self.init_state[0]

    
    def __str__(self) -> str:
        return f"{str(self.states)}, {self.init_state}, {str(self.trans_func)}, {str(self.final_states)}, {str(self.alphabet)}"