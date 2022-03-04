from Symbol import Symbol

class Alphabet(object):
    def __init__(self) -> None:
        self.symbols = []

    def add_symbol(self, symbol : Symbol) -> None:
        self.symbols.append(symbol)
    
