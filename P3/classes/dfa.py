

from classes.fa import FA
from classes.state import State
from time import time
from classes.dtypes import Token

class DFA(FA):


    def __init__(self, states: list, alphabet: list, init_state: State, trans_func: dict, final_states: list) -> None:
        super().__init__(states, alphabet, init_state, trans_func, final_states)
        
        self.trans_func = self.trans_func[0]
        self.init_state = self.init_state[0]
        self.ignore = None
        self.keywords = []
        self.keywords_except = []
        self.special_tokens = []

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
                    if last_token != None:
                        return last_token
                    idx += 1
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

    def check_except_keywords(self, buff, lexeme): #ident must be ident
        for ke in self.keywords:
            if buff == ke.value:
                return ke
        
        return Token(lexeme, buff)

    def get_tokens(self, word : str):
        tokens = []
        current_state = self.init_state
        cs = self.init_state
        word_len = len(word)
        idx = 0
        buff = ''
        error_buff = '' # chequeo en cada error de scanner si esta en los tokens especiales, borro, append y sigo
        if word_len == 0:
            return tokens
        last_token = None
        while idx < word_len:
            if word[idx] in self.ignore:
                idx += 1
            else:
                next_state = self.move(current_state, word[idx])
                current_state = next_state
                buff += chr(int(word[idx]))

                if next_state == None:
                    if last_token:
                        tokens.append(self.check_except_keywords(last_token.value, last_token.ident))

                    
                    if self.move(self.init_state, word[idx]) != None:
                        current_state = self.init_state
                        buff = ''
                        last_token = None
                        idx -=1
                    else:
                        error_buff += chr(int(word[idx]))
                        for i in self.special_tokens:
                            if error_buff == i:
                                print(f"Revisando en error buff con {i} y {error_buff}")
                                tokens.append(Token("PROD_TOKEN", error_buff))
                                error_buff = ''

                        print(f"Error léxico encontro--> {chr(int(word[idx]))}, {buff}")
                        current_state = self.init_state
                        buff = ''
                        last_token = None


                if current_state in self.final_states:
                    last_token = self.check_except_keywords(buff, current_state.lexeme )
                    # t = self.check_except_keywords(buff)
                    # if t:
                    #     last_token = t
                    # else:
                    #     last_token = Token(current_state.lexeme, buff)
                    # current_state = self.init_state
                idx += 1
            
        if last_token != None:
            if len(tokens) >0:
                if last_token != tokens[-1]:
                    tokens.append(self.check_except_keywords(last_token.value, last_token.ident))
            else:
                tokens.append(self.check_except_keywords(last_token.value, last_token.ident))
        else:
            print(f"Error léxico encontro--> {chr(int(word[idx-1]))}")

        return tokens