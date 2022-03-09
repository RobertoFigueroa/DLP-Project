from .counter import Counter


class State:

    def __init__(self, value=None, is_init=False, is_terminal=False) -> None:
        if not value:
            count = Counter()
            self.value = count.get_number()
        else:
            self.value = value
        self.is_terminal = is_terminal
        self.is_init = is_init

    
    def __str__(self) -> str:
        return str(self.value)
        
    