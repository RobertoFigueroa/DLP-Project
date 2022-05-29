# Ref: https://github.com/aixp/pycoco
# Ref:https://github.com/OJP98/py-scanner-generator

from classes.scanner import Scanner
from classes.parser import Parser
from classes.expression import Expression
from classes.cocol_tokens import CocolParser
from classes.gen_code import GenCode

import pickle
import sys

import string 

def main(file_name : str) -> int:
    
    sc = Scanner(file_name)

    file_analyzed = sc.analyze_file()

    # print(file_analyzed)

    p = Parser(
        file_analyzed.characters,
        file_analyzed.keyword,
        file_analyzed.tokens,
        file_analyzed.ignore

    )

    
    p.parse()
    p.sort()

    # print("*"*20)
    # print("Result is: ", p.get_result())
    # print("*"*20)


    cocol_parser = CocolParser(p.get_result(), p.ignore, p.raw_keywords)
    cocol_parser.generate_dfas()
    dfa = cocol_parser.dfa
    # dfa.get_image()

    # file_name = "test.txt"
    # f = open(file_name)
    # _file = f.readlines()
    # stream = []
    # for i in _file:
    #     for j in i:
    #         stream.append(str(ord(j)))

    # tokens = dfa.get_tokens(stream)
    # print("Tokens encontrados \n", tokens)


    _file = open("dfa", "wb")
    pickle.dump(dfa, _file)
    _file.close()


    code = GenCode()
    code.generate_file()

    print("File ready")

        # --- Build direct DFA ---
    # exp = Expression(p.get_result(), is_extended=True)
    # root = exp.anlyze_build_tree()
    # leafs, nodes = root.build_firstlast_pos()
    # followpos = root.followpos(leafs, nodes)
    # directed_dfa = root.build_direct_DFA(exp.alphabet.get_alphabet(), followpos, leafs)
    # # directed_dfa.get_image()
    # print('*'*20)
    # print("DFA (direct)")
    # print('*'*20)
    # print(directed_dfa)




    # buf = [str(ord("1"))]
    # t = directed_dfa.get_tokens(buf)
    # print(t)

    # ascii_printable = string.printable
    # any_but_quote = "|".join([s for s in ascii_printable.replace('"', "")])
    # any_but_apostrophe = "|".join([s for s in ascii_printable.replace("'", "")])
    # open_quote_mark = "«"
    # open_par = "܆"
    # close_par = "܇"
    # plus = "܀"
    # CHR = "¶"
    # letter = "|".join([ch for ch in string.ascii_letters])
    # any_but_quote = letter
    # any_but_apostrophe = letter
    # digit = "0|1|2|3|4|5|6|7|8|9"
    # String = f'"({any_but_quote})*"'
    # char = f"\\'({any_but_apostrophe})\\'"
    # char = char.replace("\\'", open_quote_mark)
    # number = f'(({digit})({digit})*)'
    # ident = f'({letter})({letter}|{digit})*'

    # Char = f'(({char})|(CHR{open_par}{number}{close_par}))'
    # BasicSet = f'({String})|({ident})|({Char}(..{Char})?)'
    # Set = f'({BasicSet})(({plus}|-)({BasicSet}))*'
    # SetDecl = f'({ident})=({Set})'

    # print(SetDecl)
    # print(SetDecl)

            # --- Build direct DFA ---
    # exp = Expression(SetDecl, is_extended=True)
    # root = exp.anlyze_build_tree()
    # leafs, nodes = root.build_firstlast_pos()
    # followpos = root.followpos(leafs, nodes)
    # directed_dfa = root.build_direct_DFA(exp.alphabet.get_alphabet(), followpos, leafs)
    # #directed_dfa.get_image()
    # print('*'*20)
    # print("DFA (direct)")
    # print('*'*20)
    # print(directed_dfa)
    # while True:
    #     word = input("Type word: ")
    #     result = directed_dfa.analyze(word)
    #     print(result)

if __name__ == '__main__':

    #file_name = input("Ingrese el nombre del archivo >> ")
    # file_name = "test.cocol"
    #TODO: VALIDATE INPUT
    if len(sys.argv) <= 1:
        print("No file detected")
    else:
        main(sys.argv[1])
