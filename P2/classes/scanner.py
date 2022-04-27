from classes.buffer import Buffer
from classes.cocol_tokens import CocolProcessor, CocolProcessorTokens
from classes.set_gen import SetGeneator
from classes.dtypes import Token, Keyword, VarType

EOL = '\n'
EOF = None

COCOR_SPECIFICATIONS = ['COMPILER', 'CHARACTERS', 'KEYWORDS',
                        'IGNORE', 'TOKENS', 'END', 'PRODUCTIONS']
ANY = [str(i) for i in range(0,256)]
class Cocol:
    def __init__(self) -> None:
        self.name = None
        self.characters = []
        self.characters.append(Token('ANY', set(ANY)))
        self.keyword = []
        self.tokens = []
        self.ignore = []
        self.coco = CocolProcessor()
        self.coco.generate_dfas()
        self.tokens_process = CocolProcessorTokens()
        self.tokens_process.generate_dfas()

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
        
        self.coco_file = Cocol()
        # Reads whole file
        while self.current_line != None:


            if any(word in COCOR_SPECIFICATIONS for word in self.current_line):

                if "COMPILER" in self.current_line:
                    self.coco_file.name = self.current_line[self.current_line.index("COMPILER") +1]
                    self.next_line()
                
                elif "CHARACTERS" in self.current_line:
                    self.next_line()
                    self.read_section("CHARACTERS")

                elif "KEYWORDS" in self.current_line:
                    self.next_line()
                    self.read_section("KEYWORDS")


                elif "TOKENS" in self.current_line:
                    self.next_line()
                    self.read_section("TOKENS")

                elif "PRODUCTIONS" in self.current_line:
                    self.next_line()

                elif "IGNORE" in self.current_line:
                    self.read_ignore()
                    self.next_line()

                elif "END" in self.current_line:
                    # print("Found end of file")
                    self.next_line()

            else:
                self.next_line()

        return self.coco_file

    def read_ignore(self):
        curr_set = ' '.join(self.current_line)
        line = curr_set.split('IGNORE', 1)[1]
        line = line.replace('.', '')
        line = line.strip()
        print("This ignofre", line)
  
        for i in self.coco_file.characters:
            if i.ident == line:
                self.coco_file.ignore += list(i.value)

    def read_section(self, section):

        while not any(word in COCOR_SPECIFICATIONS for word in self.current_line):

            curr_line = " ".join(self.current_line)

            # TODO: Check for other ways to set 
            curr_line = curr_line[:-1]
            self.get_key_value(curr_line, section)
            self.next_line()

                
    def get_key_value(self, line, attr):

        if attr == "CHARACTERS":
            self.define_character(line)

        if attr == "KEYWORDS":
            self.define_keyword(line)

        if attr == "TOKENS":
            self.define_token(line)

    def define_token(self, line):
        ident, value = line.split('=', 1)
        ident = ident.strip()
        value = value.strip()
        context = None

        if 'EXCEPT' in value:
            kwd_index = value.index('EXCEPT')
            context = value[kwd_index:]
            value = value[:kwd_index]

        value = value.strip()

        set_list = self.coco_file.tokens_process.analyze(value)
        
        # print(set_list)

        self.coco_file.tokens.append(
            Token(ident, set_list, context)
        )
        

        # print("cocol characters:", self.coco_file)


    def define_keyword(self, line):

        ident, value = line.split('=', 1)
        ident = ident.strip()
        value = value.replace('"', '')
        value = value.strip()

        keyword = Keyword(ident, value)
        
        # Check if already exists

        self.coco_file.keyword.append(
            keyword
        )

        # print("cocol characters:", self.coco_file)


    def define_character(self, line):

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        value = "".join(value.split(" "))
        print("This is value:", value)
        set_list = self.coco_file.coco.analyze(value)
        
        # print(set_list)

        _set = SetGeneator(set_list, self.coco_file.characters)
        _set.parse()


        self.coco_file.characters.append(
            Token(key, _set.final_set)
        )

        # print("cocol characters:", self.coco_file)


