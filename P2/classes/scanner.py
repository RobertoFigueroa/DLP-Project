from xml.dom.pulldom import CHARACTERS
from classes.buffer import Buffer

EOL = '\n'
EOF = None

COCOR_SPECIFICATIONS = ['COMPILER', 'CHARACTERS', 'KEYWORDS',
                        'IGNORE', 'TOKENS', 'END', 'PRODUCTIONS']

class Cocol:
    def __init__(self) -> None:
        self.name = None
        self.characters = []
        self.keyword = []
        self.tokens = []
        self.ignore = {}

    def __str__(self) -> str:
        return f"""
        Coco File 
        ->Name: {self.name}
        ->Characters: {self.characters}
        ->Keywords: {self.keyword}
        ->Tokens: {self.tokens}
        ->Ignore: {self.ignore}"""


class Scanner:

    def __init__(self, file_name : str) -> None:
        
        self.buffer = Buffer(file_name)
        self.pos = 0 #pos de la línea actual
        self.line = 1 #linea que va leyendo
        self.col = 0 #columna que va leyendo
        self.char_pos = 0
        self.next_line()

    def next_line(self) -> None:
        # posicion actual    
        self.pos = self.buffer.get_pos()
        # caracter actual
        self.current_line = self.buffer.read()
        # NOTE: La posición del buffer va una adelante que la del caracter actual

    def analyze_file(self):
        
        coco_file = Cocol()
        # Reads whole file
        while self.current_line != None:

            if any(word in COCOR_SPECIFICATIONS for word in self.current_line):

                if "COMPILER" in self.current_line:
                    coco_file.name = self.current_line[self.current_line.index("COMPILER") +1]
                    self.next_line()
                
                elif "CHARACTERS" in self.current_line:
                    self.next_line()


        return coco_file

    
    def read_section(self, section):

        if not any(word in COCOR_SPECIFICATIONS for word in self.current_line):

            

                    
                





        # leer compiler

        # Crear DFA para compiler
        # expect("COMPILER")
        # expect("blankspaces")
        # expect("id")



