from .symbol import Symbol
from .alphabet import Alphabet
from structures.stack import Stack
from structures.node import Node

class Expression(object):

    def __init__(self, string : str, is_extended=False) -> None:
        if is_extended:
            self.string ='(' + string + ')' + '#' 
        else:
            self.string = string
        self.alphabet = Alphabet()
        self.generate_alphabet()
        

    def generate_alphabet(self) -> None:
        ops = ['*', '?', '(', ')', '+', '|']
        for char in self.string:
            if char not in ops and char != ' ':
                sym = Symbol(char)
                self.alphabet.add_symbol(sym)

    def balanced(self) -> bool:
        pile = Stack()
        for i in self.string:
            if i == '(':
                pile.push('(')
            elif i == ')' and not pile.is_empty():
                pile.pop()
            elif i == ')' and pile.is_empty():
                return False
            else:
                continue
        
        if pile.is_empty():
            return True
        
        return False 

    def precedence(self, op):
        if op == '|':
            return 1
        if op == '؞':
            return 2
        if (op == '*' or op == '+' or op == '?'):
            return 3
        return 0
        

    def analyze(self):

        self.alphabet.add_symbol(Symbol('ε'))
        symbols = Stack()
        operands = Stack()
        word_size = len(self.string)
        i=0
        while i < word_size:

            if self.string[i] == " ":
                if i+1 < word_size:
                    if self.string[i+1] in str(self.alphabet) and not symbols.is_empty():
                        operands.push('؞')
                i += 1
                continue

            elif self.string[i] in str(self.alphabet):
                symbols.push(self.string[i])
                if i+1 < word_size:
                    if self.string[i+1] in str(self.alphabet):
                        operands.push('؞')
            
            elif self.string[i] == '(':
                operands.push(self.string[i])
            
            elif self.string[i] == ')':
                while not operands.is_empty() and operands.top() != '(':
                    val2 = symbols.pop()
                    val1 = symbols.pop()
                    op = operands.pop()
                    symbols.push(val1+val2+op)
                if not operands.is_empty():
                    operands.pop()
                if i+1 < word_size:
                    if self.string[i+1] in str(self.alphabet) or self.string[i+1] == '(':
                        operands.push('؞')

            elif (self.string[i] == '*' or self.string[i] == '+' or self.string[i] == '?'):
                val1 = symbols.pop()
                op = self.string[i]
                symbols.push(val1+op)
                if i+1 < word_size:
                    if self.string[i+1] in str(self.alphabet) or self.string[i+1] == '(':
                        operands.push('؞')
            else:
                while not operands.is_empty() and (self.precedence(operands.top()) > self.precedence(self.string[i])):
                    val2 = symbols.pop()
                    val1 = symbols.pop()
                    op = operands.pop()
                    symbols.push(val1+val2+op)
                operands.push(self.string[i])
            i+= 1
        
        while not operands.is_empty():
            op = operands.pop()
            if (op != '*' and op != '+' and op != '?'):
                val2 = symbols.pop()
                val1 = symbols.pop()
                symbols.push(val1+val2+op)
            else:
                val1 = symbols.pop()
                symbols.push(val1+op)
        return symbols.top()


    def anlyze_build_tree(self):

        self.alphabet.add_symbol(Symbol('ε'))
        symbols = Stack()
        operands = Stack()
        word_size = len(self.string)
        i=0
        while i < word_size:
            if self.string[i] == " ":
                if i+1 < word_size:
                    if self.string[i+1] in str(self.alphabet) and not symbols.is_empty():
                        operands.push(Node('؞'))
                i += 1
                continue

            elif self.string[i] in str(self.alphabet):
                symbols.push(Node(self.string[i]))
                if i+1 < word_size:
                    if self.string[i+1] in str(self.alphabet) or self.string[i+1] == '(':
                        operands.push(Node('؞'))
            
            elif self.string[i] == '(':
                operands.push(Node(self.string[i]))
            
            elif self.string[i] == ')':
                while not operands.is_empty() and operands.top().value != '(':
                    val2 = symbols.pop()
                    val1 = symbols.pop()
                    op = operands.pop()
                    op.left = val1
                    op.right = val2
                    symbols.push(op)
                    # symbols.push(val1.value+val2.value+op.value)
                if not operands.is_empty():
                    operands.pop()
                if i+1 < word_size:
                    if self.string[i+1] in str(self.alphabet) or self.string[i+1] == '(':
                        operands.push(Node('؞'))

            elif (self.string[i] == '*' or self.string[i] == '+' or self.string[i] == '?'):
                val1 = symbols.pop()
                op = Node(self.string[i])
                op.left = val1
                symbols.push(op)
                if i+1 < word_size:
                    if self.string[i+1] in str(self.alphabet) or self.string[i+1] == '(':
                        operands.push(Node('؞'))
            else:
                while not operands.is_empty() and (self.precedence(operands.top().value) > self.precedence(self.string[i])):
                    val2 = symbols.pop()
                    val1 = symbols.pop()
                    op = operands.pop()
                    op.left = val1
                    op.right = val2
                    symbols.push(op)
                operands.push(Node(self.string[i]))
            i+= 1
        
        while not operands.is_empty():
            op = operands.pop()
            if (op.value != '*' and op.value != '+' and op.value != '?'):
                val2 = symbols.pop()
                val1 = symbols.pop()
                op.left = val1
                op.right = val2
                symbols.push(op)
            else:
                val1 = symbols.pop()
                op.left = val1
                symbols.push(op)
        self.alphabet.symbols.pop()
        return symbols.top()
