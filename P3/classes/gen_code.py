from copyreg import pickle


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
_f.close()
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

    def serialize_tokens(self):
        self.file.write(
"""     
_file = open("tokens", "wb")
pickle.dump(tokens, _file)
_file.close()
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
        self.serialize_tokens()
        self.close_file()


class ParserCodeGenerator:

    #file_name : El archivo donde se esciribra el parser
    def __init__(self, file_name="custom_parser.py", instructions="") -> None:
        self.file = open(file_name, "w")
        self.instructions = instructions

    def write_imports(self):
        self.file.write(
            """
import pickle
import sys
            """
        )

    def write_template(self):
        self.file.write(

"""
class MyParser:

\tdef __init__(self) -> None:
\t\tself.prev_token = None
\t\tself.current_token = None
\t\tself.prev_char = None
\t\tself.current_char = None
\t\tself.pos = 0
\t\tself.read_tokens()
\t\tself.next_token()

\tdef read_tokens(self):
\t\t_f = open("tokens", "rb")
\t\ttokens = pickle.load(_f)
\t\tf_tokens  = []
\t\tfor i in tokens:
\t\t\t\tif i.ident != 'nontoken':
\t\t\t\t\t\tf_tokens.append(i)
\t\tself.token_stream = iter(f_tokens)

\tdef next_token(self):
\t\ttry:
\t\t\tself.prev_token = self.current_token
\t\t\tself.current_token = next(self.token_stream)
\t\t\tself.pos += 1
\t\texcept StopIteration:
\t\t\tself.current_val = None

    
\tdef next_char(self):

\t\ttry:
\t\t\tself.prev_char = self.current_char
\t\t\tself.current_char = next(self.file_stream)

\t\texcept StopIteration:
\t\t\tself.current_char = None

\tdef expect(self, char):
\t\tif char:
\t\t\tif self.current_token.ident == char or self.current_token.value == char:
\t\t\t\tself.next_token()
\t\t\t\treturn True
\t\tprint(f"Error cerca del caracter {self.pos} esperaba {char} encontre {self.current_token.value} ;(")
\t\tself.next_token()
\t\treturn False
"""
        )

    def write_productions(self):
        self.file.write(self.instructions)

    def write_exec_code(self, first_prod):
        self.file.write(
f"""
parser = MyParser()
parser.{first_prod}
print("Success Parsing!")
""")



    def close_file(self):
        self.file.close()
    
    def generate_file(self,first_prod):
        self.write_imports()
        self.write_template()
        self.write_productions()
        self.write_exec_code(first_prod)
        self.close_file()
    
