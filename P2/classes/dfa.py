from asyncio import current_task
from urllib.parse import non_hierarchical
from classes.fa import FA
from classes.state import State
from time import time
from classes.dtypes import Token

class DFA(FA):


    def __init__(self, states: list, alphabet: list, init_state: State, trans_func: dict, final_states: list) -> None:
        super().__init__(states, alphabet, init_state, trans_func, final_states)
        
        self.trans_func = self.trans_func[0]
        self.init_state = self.init_state[0]

    def move(self, state, symbol):
        if state:
            if state in self.trans_func.keys():
                if symbol in self.trans_func[state].keys():
                    return self.trans_func[state][symbol][0]
            
        return None

    def move2(self, state, symbol):
        if state:
            if state in self.trans_func.keys():
                if symbol in self.trans_func[state].keys():
                    return self.trans_func[state][symbol]
            
        return None

    def simulate(self, word : str) -> tuple:
        start = time()
        current_state = self.init_state
        for letter in word:
            if letter == " ":
                continue
            next_state = self.move(current_state, letter)
            current_state = next_state
        end = time()
        if current_state in self.final_states:
                return (True, end-start)
        return (False, end-start)

    def get_token(self, word : list) -> tuple:
        current_state = self.init_state
        cs = self.init_state
        word_len = len(word)
        idx = 0
        buff = ''
        last_token = None
        while idx < word_len:
            if word[idx] == '32':
                if '"' not in buff:
                    continue
            next_state = self.move(current_state, word[idx])
            current_state = next_state
            buff += chr(int(word[idx])) 
            idx += 1
            if next_state == None:
                if last_token:
                    return last_token
                else:
                    raise Exception("Lex error in characters definition (no transition found)")

            if current_state.lexeme != None:
                last_token = (Token(current_state.lexeme, buff), idx)
            
        if last_token != None:
            return last_token
        else:
            raise Exception("Lex error in characters definition (found end of string)")
    


    def analyze(self, word : str) -> tuple:
        current_state = self.init_state
        cs = self.init_state
        word_len = len(word)
        idx = 0
        while idx < word_len:
            next_state = self.move(current_state, word[idx])
            ns2 = self.move2(current_state, word[idx])
            print(ns2)
            current_state = next_state
            idx += 1
        if current_state in self.final_states:
                print("Fina states: ", current_state)
                return True
        return False

    def __str__(self) -> str:
        return f"States: {str(self.states)}\nInit state: {self.init_state}\n Tran func: {str(self.trans_func)}\n Final states: {str(self.final_states)}\n Alphabet: {str(self.alphabet)}\n"

    def __repr__(self) -> str:
        return f"dfa-{time()}"

