class GenCode:

    def __init__(self, file_name="custom_scanner.py") -> None:
        self.file = open(file_name, "w")

    def write_imports(self):
        self.file.write(
            """
import pickle
import sys
            """
        )
    
    def write_read_file(self):
        self.file.write(
        """
file_name = sys.argv[1]
_file = None
try:
    f = open(file_name, "r")
    _file = f.readlines()
    f.close()
except:
    raise("No se pudo leer el archivo, revise al archivo y/o el path: ", file_name)

stream = []
for i in _file:
    for j in i:
        stream.append(str(ord(j)))

        """
        )

    def create_automata(self):
        self.file.write(
        """
_f = open("dfa", "rb")
dfa = pickle.load(_f)
        """
        )

    def evaluate(self):
        self.file.write(
        """
tokens = dfa.get_tokens(stream)
        """
        )

    def result(self):
        self.file.write(
        """
for i in tokens:
    print(i)
        """
        )

    
    def close_file(self):
        self.file.close()

    
    def generate_file(self):
        self.write_imports()
        self.write_read_file()
        self.create_automata()
        self.evaluate()
        self.result()
        self.close_file()


class ParserCodeGenerator:

    def __init__(self, file_name) -> None:
        self.file = open(file_name, "w")

    def write_imports(self):
        self.file.write(
            """
import pickle
import sys
            """
        )

    def write_read_tokens(self):
        self.file.write(
        """
file_name = sys.argv[1]
_file = None
try:
    f = open(file_name, "r")
    _file = f.readlines()
    f.close()
except:
    raise("No se pudo leer el archivo, revise al archivo y/o el path: ", file_name)

stream = []
for i in _file:
    for j in i:
        stream.append(str(ord(j)))

        """
        )

    def close_file(self):
        self.file.close()
    
    def read_file(self):
        pass

s = """
class MyParser:

    def __init__(self, tokenStream : list, inputFile) -> None:

        self.token_stream = iter(tokenStream)
        self.file = inputFile
        self.read_file()
        self.prev_token = None
        self.current_token = None
        self.prev_char = None
        self.current_char = None
        self.pos = 0
    

    def read_tokens(self):
        # TODO: Consider if pickle tokens
        pass
        
    def read_file(self):
        try:
            f = open(self.file, "r")
            self.file_stream = f.read()
            self.file_stream = iter(self.file_stream)
            f.close()
        except:
            raise("No se pudo leer el archivo, revise al archivo y/o el path: ", file_name)


    def next_token(self):

        try:
            self.prev_token = self.current_token
            self.current_token = next(self.token_stream)
            self.pos += 1
        except StopIteration:
            self.current_val = None

    
    def next_char(self):

        try:
            self.prev_char = self.current_char
            self.current_char = next(self.file_stream)
        
        except StopIteration:
            self.current_char = None

    def expect(self, char):
        if char:
            if self.current_token.ident == char or self.current_token.value == char:
                self.next_token()
                return True
        print(f"Error cerca del caracter {self.pos} esperaba {char} encontre {self.current_token.value} ;(")
        self.next_token()
        return False

    
"""
