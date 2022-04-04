from itertools import count


class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]



class Counter(metaclass=SingletonMeta):
    
    def __init__(self) -> None:
        self.count = 0

    def get_number(self):
        self.count += 1
        return self.count