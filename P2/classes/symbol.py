class Symbol(object):
    
    def __init__(self, symbol : str) -> None:
        self.symbol = symbol
    
    def __str__(self) -> str:
        return str(self.symbol)
    

    def __eq__(self, other: object) -> bool:

        if type(other) == str:
            return self.symbol == other
        else:
            return self.symbol == other.symbol
        

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(str(self))

    def __repr__(self) -> str:
        return self.symbol