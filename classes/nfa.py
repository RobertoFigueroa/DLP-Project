from .fa import FA

class NFA(FA):

    def __init__(self, states, alphabet, init_state, trans_func, final_states) -> None:
        super().__init__(states, alphabet, init_state, trans_func, final_states)


    def add_transition(self, from_state, to_state, symbol):
        if from_state in self.trans_func.keys():
            if symbol.value in self.trans_func[from_state].keys():
                
        