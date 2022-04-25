from .counter import Counter


class State(object):

    def __init__(self, value=None, is_init=False, is_terminal=False) -> None:
        if not value:
            count = Counter()
            self.value = count.get_number()
        else:
            self.value = value
        self.is_terminal = is_terminal
        self.is_init = is_init
        self.mark = False
        self.lexeme = None

    
    def __cmp__(self, other):
        if type(other) == str:
            return self.value == other
        else:
            return self.value == other.value

    def __hash__(self) -> int:
        return hash(str(self))
    
    def __eq__(self, other: object) -> bool:
        if other == None:
            return False
        if type(other) == str:
            return self.value == other
        else:
            return self.value == other.value
    
    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
        

    def __str__(self) -> str:
        return str(self.value)
        
    def __repr__(self) -> str:
        return str(self.value)