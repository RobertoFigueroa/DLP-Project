from classes.dtypes import VarType
from classes.dtypes import Token

class Parser:

    def __init__(self, characters, keywords, tokens) -> None:
        self.raw_characters = characters
        self.characters = []
        self.raw_keywords = keywords
        self.keywords = []
        self.tokens = tokens
        self.dfas = []
        self.nfa = None
        self.result = ''
        self.format_characters()
        self.format_keywords()
        self.parse_tokens = []

    def format_(self, iterable):
        result = ''
        for element in iterable:
            result += f'{element}|'
        result = result.strip('|')
        result = "(" + result + ")"
        return result


    def format_characters(self):
        
        for char_set in self.raw_characters:
            result = ''
            for element in char_set.value:
                result += f'{element}|'
            result = result.strip('|')
            result = "(" + result + ")"
            self.characters.append(Token(char_set.ident, result))

    def format_keywords(self):

        for char_set in self.raw_keywords:
            result = ''
            for element in char_set.value:
                result += f'{str(ord(element))}|'
            result = result.strip("|")
            result = "(" + result + ")"
            self.keywords.append(Token(char_set.ident, result))

    def get_result(self):
        return [i for i in self.result]

    def parse(self):

        for token in self.tokens:
            for _def in token.value:

                if _def.ident == VarType.IDENT:
                    to_append = self.get_value(self.characters, _def.value)
                    if to_append != None:
                        self.append_2_result(to_append)
                    else:
                        raise Exception(f"Error en definicion de token, conjunto no encontrado")
                
                elif _def.ident == VarType.STRING:
                    to_append = self.format_(_def.value)
                    self.append_2_result(to_append)
                
                elif _def.ident == VarType.RKLEENE:
                    self.append_2_result(")*")

                elif _def.ident == VarType.LKLEENE:
                    self.append_2_result("(")
                
                elif _def.ident == VarType.RBRACKET:
                    self.append_2_result(")?")
                
                elif _def.ident == VarType.LBRACKET:
                    self.append_2_result("(")
                
                elif _def.ident == VarType.OR:
                    self.append_2_result("|")

        for keyword in self.keywords:

            self.append_2_result(keyword.value)

    def get_value(self, definitions, value_2_search):

        for _def in definitions:

            if _def.ident == value_2_search:

                return _def.value
        
        return None


    def append_2_result(self, value):

        if len(self.result) == 0:

            self.result = self.result + value
        
        else:
            if value not in ["(", ")*", "|", ")?"]:
                if self.result[-1] in  ["(", ")*", "|", ")?"]:
                    self.result = self.result + value
                else:
                    self.result = self.result + f"|{value}"
            else:
                self.result = self.result + value

        
        

