import string
from .dtypes import Token
from .alphabet import Alphabet
from structures.stack import Stack
from structures.node import Node
from .symbol import Symbol

class ProdNode:

    def __init__(self, production : list) -> None:
        self.head = Node(production[0].value, attribute=production[0].attr)
        self.string = production[1:]
        self.alphabet = Alphabet()
        self.generate_alphabet()
        
    def generate_alphabet(self) -> None:
        ops = ['Ω', '?', '◀', '▶', '|']
        for token in self.string:
            if token.value not in ops:
                sym = Symbol(token.value)
                self.alphabet.add_symbol(sym)

    def precedence(self, op):
        if op == '|':
            return 1
        if op == '؞':
            return 2
        if (op == 'Ω' or op == '?'):
            return 3
        return 0


    def anlyze_build_tree(self):

        #self.alphabet.add_symbol(Symbol('ε'))
        symbols = Stack()
        operands = Stack()
        word_size = len(self.string)
        i=0
        while i < word_size:
            if self.string[i].value == " ":
                if i+1 < word_size:
                    if str(self.string[i+1].value) in str(self.alphabet) and not symbols.is_empty():
                        operands.push(Node('؞'))
                i += 1
                continue

            elif str(self.string[i].value) in str(self.alphabet):
                symbols.push(Node(self.string[i].value, attribute=self.string[i].attr))
                if i+1 < word_size:
                    if str(self.string[i+1].value) in str(self.alphabet) or self.string[i+1].value == '◀':
                        operands.push(Node('؞'))
            
            elif self.string[i].value == '◀':
                operands.push(Node(self.string[i].value))
            
            elif self.string[i].value == '▶':
                while not operands.is_empty() and operands.top().value != '◀':
                    val2 = symbols.pop()
                    val1 = symbols.pop()
                    op = operands.pop()
                    op.left = val1
                    op.right = val2
                    op.attr=self.string[i].attr
                    symbols.push(op)
                    # symbols.push(val1.value+val2.value+op.value)
                if not operands.is_empty():
                    operands.pop()
                if i+1 < word_size:
                    if str(self.string[i+1].value) in str(self.alphabet) or self.string[i+1].value == '◀':
                        operands.push(Node('؞'))

            elif (self.string[i].value == 'Ω' or self.string[i].value == '?'):
                val1 = symbols.pop()
                op = Node(self.string[i].value, attribute=self.string[i].attr)
                op.left = val1
                symbols.push(op)
                if i+1 < word_size:
                    if str(self.string[i+1].value) in str(self.alphabet) or self.string[i+1].value == '◀':
                        operands.push(Node('؞'))
            else:
                while not operands.is_empty() and (self.precedence(operands.top().value) > self.precedence(self.string[i].value)):
                    val2 = symbols.pop()
                    val1 = symbols.pop()
                    op = operands.pop()
                    op.left = val1
                    op.right = val2
                    symbols.push(op)
                operands.push(Node(self.string[i].value, attribute=self.string[i].attr))
            i+= 1
        
        while not operands.is_empty():
            op = operands.pop()
            if (op.value != 'Ω' != '?'):
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
        t = symbols.top()
        self.head.left = t
        return self.head

    def __repr__(self) -> str:
        return f"\n->{self.string}\n->{self.alphabet}"
        