from classes.symbol import Symbol

class Alphabet(object):
    def __init__(self, symbols=[]) -> None:
        self.symbols = symbols

    def add_symbol(self, symbol : Symbol) -> None:
        if not self.duplicate(symbol):
            self.symbols.append(symbol)
    
    
    def duplicate(self, symbol : Symbol) -> bool:
        for sym in self.symbols:
            if str(sym) == str(symbol):
                return True
        
        return False


    def __str__(self) -> str:
        syms = []
        for symbol in self.symbols:
            syms.append(str(symbol))
        return str(syms)
