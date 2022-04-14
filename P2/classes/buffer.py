class Buffer(object):
    
    def __init__(self, file_name : str) -> None:
        try:
            f = open(file_name, "r")
            self.file = f.readlines()
            f.close()
        except:
            raise("No se pudo leer el archivo, revise al archivo y/o el path: ", file_name)

        self.buffer = self.format_file()
        self.total_lines = len(self.buffer)
        self.pos = 0

    def format_file(self) -> list:
        formatted_lines = []
        for line in self.file:
            if line != '\n':
                line = line.strip()
                line = line.strip("\n\r\t")
                line = line.split(" ")
                line = [i for i in line if i != ""]
                formatted_lines.append(line)
        return formatted_lines

    def set_pos(self, value : int) -> None:
        if value < self.total_lines:
            self.pos = value
        else:
            raise("Buffer fuera de límites")

    def read(self) -> str:
        if self.pos < self.total_lines:
            char = self.buffer[self.pos]
            self.pos += 1
            return char
        else:
            return None

    def peek(self) -> str:
        cur_pos = self.pos
        ch = self.read()
        self.set_pos(cur_pos)
        return ch

    def get_pos(self) -> int:
        return self.pos