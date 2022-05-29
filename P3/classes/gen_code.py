




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
print(tokens)
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


