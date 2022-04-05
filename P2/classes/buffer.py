class Buffer(object):
    
    def __init__(self, file_name : str) -> None:
        try:
            f = open(file_name, "r")
            self.file = f.read()
            f.close()
        except:
            raise("No se pudo leer el archivo, revise al archivo y/o el path: ", file_name)

        self.file_len = len(self.file)

        self.buf = [char for char in self.file]

        self.bufStart = 10**10

        if self.file_len > 0:
            self.set_pos(0)
        else:
            self.buf_pos = 0

    def set_pos(self, value : int) -> None:
        if value < self.file_len:
            self.buf_pos = value
        else:
            raise("Buffer out of bounds")

    def read(self) -> str:
        if self.buf_pos < self.file_len:
            char = self.buf[self.buf_pos]
            self.buf_pos += 1
            return char
        else:
            return None

    def peek(self) -> str:
        cur_pos = self.buf_pos
        ch = self.read()
        self.set_pos(cur_pos)
        return ch