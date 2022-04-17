from utils import (
    GetCharValue,
    GetElementType
)

from dtypes import (
    VarType,
    Variable,
    Character
)


CONTEXT_WORDS = ['ANY']
ANY_SET = set([chr(char) for char in range(0, 256)])

class DefSet:

    def __init__(self, _set, idents) -> None:
        self.set = iter(_set)
        self.idents = idents
        self.curr_char = None
        self.curr_set = _set
        self.valid_alnum = ['(', ')']
        self.Next()


    def Next(self):
        try:
            self.curr_char = next(self.set)
        except StopIteration:
            self.curr_char = None
    
    def Set(self):
        while self.curr_char != None:

            if self.curr_char.isalpha():

                yield self.GenerateWord()

            elif self.curr_char == '\'' or self.curr_char == '"':

                yield self.GenereateVar(self.curr_char)

            elif self.curr_char == '+':
                self.Next()
                yield Variable(VarType.UNION)
            
            elif self.curr_char == '-':
                self.Next()
                yield Variable(VarType.DIFFERENCE)

            elif self.curr_char == '.':
                self.Next()
                if self.curr_char == '.':
                    self.Next()
                    yield Variable(VarType.RANGE)
                else:
                    raise Exception(f"Invalid dot {self.curr_set}")

            elif self.curr_char == ' ':
                self.Next()


    def GenerateVar(self, symbol_type):

        var = self.curr_char
        self.Next()

        while self.curr_char != None:

            var += self.curr_char
            self.Next()

            if self.curr_char == symbol_type:

                var += self.curr_char
                self.Next()
                break
                
        if var.count(symbol_type) != 2:
            raise Exception(f"Expected {symbol_type}")
        
        res = GetElementType(var, self.idents)

        if not res:
            raise Exception(f"Invalid var: {var}")
        
        return res

    def GenerateWord(self):

        word = self.curr_char
        self.Next()

        while self.curr_char != None \
            and (self.curr_char.isalnum() or self.curr_char in self.valid_alnum) \
            and self.curr_char != " ":

            word += self.curr_char
            self.Next()

            if 'CHR(' in word:
                res = GetCharValue(word)
                res = Variable(VarType.CHAR, set(res))
            
            else:

                res = GetElementType(word, self.idents)
            
            if not res:

                raise Exception(
                    f"Invalid ident: {word} in {self.curr_set}"
                )

            return res

    

class GenSet:

    def __init__(self, set_, idents) -> None:
        self.set = iter(set_)
        self.idents = idents
        self.curr_var = None
        self.prev_var =  None
        self.res_set = None
        self.curr_set = set_
        self.Next()

    
    def Next(self):

        try:

            self.prev = self.curr_var
            self.curr_var = next(self.set)
        
        except StopIteration:
            self.curr_var = None
        
    
    def GenerateSet(self):

        while self.curr_var != None:

            if self.curr_var.type == VarType.UNION:
                self.NewSet('UNION')
                self.Next()
            
    

    def NewSet(self, op):

        self.Next()

        if self.curr_var.value == None:
            Exception(f"Invalid set definition")
        
        curr_set = self.curr_var.value

        if op == 'UNION':
            self.res_set = self.res_set.union(curr_set)
        elif op == 'DIFFERENCE':
            self.res_set = self.res_set.difference(curr_set)
        
    
    def NewRange(self):
        char1=self.prev_var
        self.Next()
        char2=self.curr_var

        if char1.type != VarType.CHAR or char2.type != VarType.CHAR:
            raise Exception(
                f"Unvalid char range found in {self.curr_set}"
            )
        
        range1 = ord(char1.value.pop())
        range2 = ord(char2.value.pop())

        if range1 > range2:
            range1, range2 = range2, range1
        
        char_range=set([chr(char) for char in range(range1, range2+1)])


        self.res_set.update(char_range)

         
    
