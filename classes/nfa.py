from .fa import FA
from classes.state import State
from classes.symbol import Symbol

class NFA(FA):

    def __init__(self, states: list, alphabet: list, init_state: State, trans_func: dict, final_states: list) -> None:
        super().__init__(states, alphabet, init_state, trans_func, final_states)
        
        self.trans_func = self.trans_func[0]
        self.init_state = self.init_state[0]


    def get_init(self) -> State:
        return self.init_state

    def get_final(self) -> State:
        if len(self.final_states) > 0:
            return self.final_states[0]
        return None

    def add_transition(self, from_state : State, to_state : State, symbol : Symbol) -> None:
        
        print("Trans ", self.trans_func)

        if symbol not in self.alphabet:
            self.alphabet.append(symbol)
        
        if from_state not in self.states:
            self.states.append(from_state)
        
        
        if to_state not in self.states:
            self.states.append(to_state)


        if from_state in self.trans_func.keys():
            if symbol in self.trans_func[from_state].keys():
                if to_state not in self.trans_func[from_state][symbol]:
                    self.trans_func[from_state][symbol].append(to_state)
            else:
                self.trans_func[from_state][symbol] = [to_state]
        else:
            self.trans_func[from_state] = {
                symbol : [to_state]
            }


    def __str__(self) -> str:
        return f"{str(self.states)}, {self.init_state}, {str(self.trans_func)}, {str(self.final_states)}, {str(self.alphabet)}"