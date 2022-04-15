from utils import (
    GetCharValue
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
                res = Variable(Vart)
            

    



