from lib2to3.refactor import get_all_fix_names

from numpy import var
from classes.dtypes import VarType


class SetGeneator:
    
    def __init__(self, _set, prev_defs) -> None:
        self._set = iter(_set)
        self.raw_set = _set
        self.defs = prev_defs
        self.current_val = None
        self.prev_val = None
        self.final_set = set()
        self.get_next()

    def peek(self):

        curr = self.current_val
        prev = self.prev_val

        # self.get_next()
        idx = self.raw_set.index(curr)
        if idx+1 < len(self.raw_set):
            return self.raw_set[idx+1], None
        
        return None, None

    
    def get_next(self):

        try:
            self.prev_val = self.current_val
            self.current_val = next(self._set)
            # print("in next funciton",self.current_val)
        
        except StopIteration:
            self.current_val = None



    def parse(self):

        while self.current_val != None:
            # print("next is", self.current_val)

            if self.current_val.ident == VarType.IDENT:
                self.gen_ident()
                self.get_next()
            
            elif self.current_val.ident == VarType.STRING:
                self.gen_string()
                self.get_next()
            
            elif self.current_val.ident == VarType.CHARDF:
                self.gen_char()
                self.get_next()
            
            elif self.current_val.ident == VarType.UNION:
                self.gen_union()
                self.get_next()

            elif self.current_val.ident == VarType.DIFFERENCE:
                self.gen_diff()
                self.get_next()

            elif self.current_val.ident == VarType.CHAR:
                self.gen_ch()
                self.get_next()
        
    def gen_ch(self, ret_val=False):
        
        val = self.current_val.value.strip("\\'")
        val = str(ord(val))

        _next, _prev = self.peek()


        if _next != None:
            if _next.ident == VarType.RANGE:
                self.get_next() #range
                self.get_next() #ch
                to = self.current_val.value
                to = to.strip("\\'")
                if ret_val:
                    return [str(i) for i in range(int(val), ord(to)+1)]

                [self.final_set.add(str(i)) for i in range(int(val), ord(to)+1)]
                return 
        
        if ret_val:
            return [val]
        
        self.final_set.add(val)

    def gen_diff(self):
        
        self.get_next()
    

        if self.current_val.ident == VarType.IDENT:
            diff = self.gen_ident(ret_val=True)
            self.final_set.difference_update(diff)
        
        elif self.current_val.ident == VarType.CHARDF:
            diff = self.gen_char(ret_val=True)
            self.final_set.difference_update(diff)
        
        elif self.current_val.ident == VarType.STRING:
            diff = self.gen_string(ret_val=True)
            self.final_set.difference_update(diff)

        elif self.current_val.ident == VarType.CHAR:
            diff = self.gen_ch(ret_val=True)
            self.final_set.difference(diff)
        

    def gen_union(self):

        self.get_next()
        
        if self.current_val.ident == VarType.IDENT:
            self.gen_ident()
        
        if self.current_val.ident == VarType.CHARDF:
            self.gen_char()
        
        if self.current_val.ident == VarType.STRING:
            self.gen_string()
        

    


    def gen_ident(self, ret_val = False):

        
        set_id = [s for s in self.defs if s.ident == self.current_val.value] 
        if len(set_id) < 1:
            raise Exception(f"{self.current_val} is not defined")
        
        set_id = set_id[0]
        
        if ret_val:
            return [i for i in set_id.value]
        else:
            [self.final_set.add(i) for i in set_id.value]


    def gen_string(self, ret_val=False):
        string_set = self.current_val.value.strip('"')
        _next, prev = self.peek()
        if _next:
            if _next.ident == VarType.RANGE:
                self.get_next() #range
                to = self.current_val # espero in stringde un caracter como el archivo sera si errors se puede asumir que así lo será
                if not ret_val:
                    [self.final_set.add(str(i)) for i in range(ord(string_set), ord(to.value.strip('"'))+1)]
                    return
                else:
                    return [str(i) for i in range(ord(string_set), ord(to.value.strip('"'))+1)]
        if ret_val:
            list_ = []
            for char in string_set:
                list_.append(str(ord(char)))
            return list_
        else:
            for char in string_set:
                self.final_set.add(str(ord(char)))
             
    def gen_char(self, ret_val =  False):
        self.get_next()
        expect_number = self.current_val
        self.get_next()
        expect_rpar = self.current_val

        
        _next, _prev = self.peek()
        # print("current", self.current_val)

        if expect_number.ident != VarType.NUMBER:
            raise Exception(f"Error in CHR declaration, expected number found: {expect_number}")
        
        if expect_rpar.ident != VarType.RPAR:
            raise Exception(f"Error in CHR declaration, expected close parenthesis found: {expect_rpar}")

        if _next != None:
            if _next.ident == VarType.RANGE:
                self.get_next() #chr
                self.get_next() #number
                to = self.current_val
                self.get_next() #rpar
                if ret_val:
                    return [str(i) for i in range(int(expect_number.value), int(to.value)+1)]

                [self.final_set.add(str(i)) for i in range(int(expect_number.value), int(to.value)+1)]
                return 
        
        if ret_val:
            return [str(expect_number.value)]
        
        self.final_set.add(expect_number.value)





    