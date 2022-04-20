from .fa import FA
from classes.state import State
from classes.symbol import Symbol
from structures.stack import Stack
from classes.dfa import DFA
from time import time

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

    def check_marked(self, dstates : list) -> State:
        for state in dstates:
            if state[0].mark == False:
                return state
        return None

    def in_dstates(self, U: set, dstates : list) -> bool:
        for state in dstates:
            if state[1] == U:
                return True
        
        return False

    def get_U_state(self, U, dstates):
        for state in dstates:
            if state[1] == U:
                return state[0] 
        return None


    def build_DFA(self):
        # DTran es la funcion de transicion del dfa
        trans_func = dict()
        dStates = []
        dStates.append((State(), self.e_closure(set([self.init_state]))))
        unmarked_state = self.check_marked(dStates)
        while unmarked_state:
            unmarked_state[0].mark = True
            for symbol in self.alphabet:
                if symbol != self.epsilon:
                    U = self.e_closure(self.move(unmarked_state[1], symbol))
                else:
                    continue
                # print(f"with {symbol} --> {U}")
                if len(U) == 0:
                    continue
                
                if self.in_dstates(U, dStates) == False:
                    dStates.append((State(), U))
                
                state = self.get_U_state(U, dStates)

                if unmarked_state[0] in trans_func.keys():
                    if symbol in trans_func[unmarked_state[0]].keys():
                        if state not in trans_func[unmarked_state[0]][symbol]:
                            trans_func[unmarked_state[0]][symbol].append(state)
                    else:
                        trans_func[unmarked_state[0]][symbol] = [state]

                else:
                    trans_func[unmarked_state[0]] = {symbol : [state]}

            unmarked_state = self.check_marked(dStates)

        final_states = []
        states = []

        for tup in dStates:
            states.append(tup[0])
            for state in tup[1]:
                if state in self.final_states:
                    final_states.append(tup[0])

        dfa = DFA(states, [sym for sym in self.alphabet if sym != self.epsilon], dStates[0][0], trans_func, final_states)

        # print("DStates: ", dStates)

        return dfa
    

    def e_closure(self, state : any) -> set:
        # return: conjunto de estados E conjunto P(states)
        if type(state) == State:
            e_trans = []
            if state in self.trans_func.keys():
                for symbol in self.trans_func[state].keys():
                    if symbol == self.epsilon:
                        e_trans = self.trans_func[state][symbol]

            return set(e_trans)
        
        if type(state) == set:
            pile = Stack()
            e_trans=[]
            for st in state:
                pile.push(st)
                e_trans.append(st)

            while not pile.is_empty():
                t = pile.pop()
                for u in self.e_closure(t):
                    if u not in e_trans:
                        e_trans.append(u)
                        pile.push(u)
            return set(e_trans)

    def move(self, T, a):
        trans = []
        for state in T:
            if state in self.trans_func.keys():
                for symbol in self.trans_func[state].keys():
                    if symbol == a:
                        for to_state in self.trans_func[state][symbol]:
                            trans.append(to_state)

        return set(trans)

    def simulate(self, word : str) -> tuple:
        start = time()
        S = self.e_closure(set([self.init_state]))
        for letter in word:
            S = self.e_closure(self.move(S, letter))
        end = time()
        if len(S.intersection(set(self.final_states))) > 0:
            return (True, end-start)
        return (False, end-start)


    def __str__(self) -> str:
        # Sanity check
        self.alphabet = [i for i in self.alphabet if i != self.epsilon]
        return f"States: {str(self.states)}\nInit state: {self.init_state}\n Tran func: {str(self.trans_func)}\n Final states: {str(self.final_states)}\n Alphabet: {str(self.alphabet)}\n"

    def __repr__(self) -> str:
        return f"nfa-{time()}"