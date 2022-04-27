from classes.dtypes import VarType
from classes.dtypes import Token
from classes.expression import Expression

class Parser:

    def __init__(self, characters, keywords, tokens, ignore) -> None:
        self.raw_characters = characters
        self.characters = []
        self.raw_keywords = keywords
        self.keywords = []
        self.tokens = tokens
        self.dfas = []
        self.nfa = None
        self.result = []
        self.format_characters()
        self.format_keywords()
        self.parse_tokens = []
        self.iter = None
        self.temp_res = []
        self.ignore = ignore

    def format_(self, iterable):
        result = []
        for element in iterable:
            result.append(element)
            result.append('|')
        result = result[:-1]
        result = ["("] + result + [")"]
        return result


    def format_characters(self):
        for char_set in self.raw_characters:
            result = self.format_(char_set.value)
            self.characters.append(Token(char_set.ident, result))

    def format_keywords(self):
        for char_set in self.raw_keywords:
            vals = []
            for i in char_set.value:
                vals.append(str(ord(i)))
            self.keywords.append(Token(char_set.ident, vals))

    def get_result(self):
        
        return self.result
        # result = []
        # size = len(self.result)
        # idx = 0
        # while idx < size:
        #     if self.result[idx] in ['(', ')', '?', '*', '|']:
        #         result.append(self.result[idx])
        #         idx += 1
        #     else:
        #         temp_res = ''
        #         while self.result[idx].isdigit():
        #             temp_res += self.result[idx]
        #             idx += 1
        #         result.append(temp_res)
        # return result

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
                    to_append = [i for i in to_append if i != '|']
                    self.append_2_result(to_append)
                
                elif _def.ident == VarType.RKLEENE:
                    self.append_2_result([")", "*"])

                elif _def.ident == VarType.LKLEENE:
                    self.append_2_result(["("])
                
                elif _def.ident == VarType.RBRACKET:
                    self.append_2_result([")", "?"])
                
                elif _def.ident == VarType.LBRACKET:
                    self.append_2_result(["("])
                
                elif _def.ident == VarType.OR:
                    self.append_2_result(["|"])


            self.result.append(
                Token(token.ident, 
                Expression(
                    self.temp_res,
                    is_extended=True
            )))
            self.temp_res = []

        for keyword in self.keywords:

            self.result.append(
                Token(
                    keyword.ident,
                    Expression(keyword.value, 
                    is_extended=True),
                    context=keyword.context
                )
            )

    def get_value(self, definitions, value_2_search):

        for _def in definitions:

            if _def.ident == value_2_search:

                return _def.value
        
        return None


    def append_2_result(self, value):

        if len(self.temp_res) == 0:

            self.temp_res = self.temp_res + value
        
        else:
            if not self.check_op(value):
                if self.check_op(self.temp_res[-1]):
                    self.temp_res = self.temp_res + value
                else:
                    self.temp_res = self.temp_res + ["|"] + value
            else:
                self.temp_res = self.temp_res + value

    
    def check_op(self, value):

        for i in value:
            if i in ["(", ")", "*", "|", ")?"]:
                return True
        return False

