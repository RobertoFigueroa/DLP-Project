class Symbol(object):
    
    def __init__(self, symbol : str) -> None:
        self.symbol = symbol
    
    def __str__(self) -> str:
        return str(self.symbol)
    