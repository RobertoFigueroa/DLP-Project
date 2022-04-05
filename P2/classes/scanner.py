from classes.buffer import Buffer

class Scanner(object):
    def __init__(self, file_name : str) -> None:
        self.buffer = Buffer(file_name)
        self.pos = -1
        self.line = 1
        self.col = 0
        self.char_pos = -1
        self.ch = None
    

    def next_ch(self):
        pass