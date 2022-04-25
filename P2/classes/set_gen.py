from cv2 import sepFilter2D
from numpy import var
from classes.dtypes import VarType


class SetGeneator:
    
    def __init__(self, _set, prev_defs) -> None:
        self._set = iter(_set)
        self.defs = prev_defs
        self.current_val = None
        self.prev_val = None
        self.final_set = set()
        self.get_next()

    
    def get_next(self):

        try:
            self.prev_val = self.current_val
            self.current_val = next(self._set)
        
        except StopIteration:
            self.current_val = None



    def parse(self):

        while self.current_val != None:

            if self.current_val.type == VarType.IDENT:
                self.gen_ident()
                self.get_next()
            
            elif self.current_val.type == VarType.STRING:
                self.gen_string()
                self.get_next()
            
            elif self.current_val.type == VarType.CHARDF:
                self.gen_char()
                self.get_next()
            
            elif self.current_val.type == VarType.UNION:
                self.gen_union()
                self.get_next()

            # elif self.current_val.type == VarType.DIFFERENCE:
            #     self.gen_diff()
            #     self.get_next()

        

    
    def gen_union(self):

        self.next()
        
        if self.current_val.type == VarType.IDENT:
            self.gen_ident()
        
        if self.current_val.type == VarType.CHARDF:
            self.gen_char()
        
        if self.current_val.type == VarType.STRING:
            self.gen_string()
        

                

    def gen_ident(self):
        
        set_id = [s for s in self.defs if s.value == self.current_val.value] 
        if len(set_id) < 1:
            raise Exception(f"{self.current_val} is not defined")
        
        set_id = set_id[0]
        
        [self.final_set.add(i) for i in set_id.value]


    def gen_string(self):
        self.current_val.value = self.current_val.value.strip('"')
        for char in self.current_val.value:
            self.final_set.add(str(ord(char)))

    def gen_char(self):
        
        self.get_next()
        expect_number = self.current_val
        self.get_next()
        expect_rpar = self.current_val

        if expect_number.type != VarType.NUMBER:
            raise Exception(f"Error in CHR declaration, expected number found: {expect_number}")
        
        if expect_rpar.type != VarType.RPAR:
            raise Exception(f"Error in CHR declaration, expected close parenthesis found: {expect_rpar}")

        self.final_set.add(expect_number)





    