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
