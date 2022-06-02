from distutils.filelist import findall
from classes.dtypes import Variable, VarType

import codecs

from classes.set import ANY_SET, CONTEXT_WORDS



def GetTextInsideSymbols(string, start_symbol, end_symbol):
    start = string.find(start_symbol)
    end = string.find(end_symbol)

    if start == -1 or end == -1:
        return None
    
    if string.count(start_symbol) != 1 or string.count(end_symbol) != 1:
        return None

    return string[start+1:end]

def GetCharValue(char):

    value = GetTextInsideSymbols(char, '(', ')')

    if value == None:
        raise Exception(
            "CHARACTERS BAD DEF: char is not defined correctly: missplaced parenthesis"
        )

    if not value.isdigit():
        raise Exception(
            "CHARACTERS BAD DEF: char is not defined correctly: non-digit CHR value"
        )

    return chr(int(value))

def IdentExists(ident, char_set):
    try:
        next(filter(lambda x: x.ident == ident, char_set))
        return True
    except StopIteration:
        return False

    
def GetTextFromSingleQuotes(string):
    text = findall("'([^']*)'", string)

    if not text:
        return None
    if len(text) > 1:
        return None
    
    return str(text[0])


def getIdentValue(ident, char_set):
    try:
        ident = next(filter(lambda x: x.ident == ident, char_set))
        return ident.value
    except StopIteration:
        return None

def GetElementType(string , char_set):

    if string.count('"') == 2:
        string = string.repalce("\"", '')

        val = set([chr(ord(char)) for char in string])
    
        return Variable(VarType.STRING, val)
    
    if string.count('\'') == 2:

        char = GetTextFromSingleQuotes(string)
        try:
            char = codecs.decode(char, 'unicode_escape')
            ord_ = ord(char)
        except:
            raise Exception(f"Unvalid char in GetElementType: {string}")
        
        new_set = set(chr(ord_))

        return Variable(VarType.CHAR, new_set)

    if string in CONTEXT_WORDS:
        if "ANY" == string:
            return Variable(VarType.NUMBER, ANY_SET)

    if string.isdigit():
        return Variable(VarType.NUMBER, string)
    
    if IdentExists(string, char_set):
        return Variable(VarType.IDENT, getIdentValue(string, char_set), string)
    
    if 'CHR' in string.upper():

        char = set(GetCharValue(string))

        return Variable(VarType.CHAR, char)


