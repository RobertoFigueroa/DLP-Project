# Ref: https://github.com/OJP98/py-scanner-generator

#from classes.scanner import Scanner

from classes.expression import Expression

import string 

def main(file_name : str) -> int:
    
    #sc = Scanner(file_name)

    # file_analyzed = sc.analyze_file()

    # print(file_analyzed)

        # --- Build direct DFA ---
    # exp = Expression(reg_exp, is_extended=True)
    # root = exp.anlyze_build_tree()
    # leafs, nodes = root.build_firstlast_pos()
    # followpos = root.followpos(leafs, nodes)
    # directed_dfa = root.build_direct_DFA(exp.alphabet.get_alphabet(), followpos, leafs)
    # directed_dfa.get_image()
    # print('*'*20)
    # print("DFA (direct)")
    # print('*'*20)
    # print(directed_dfa)



    ascii_printable = string.printable
    # any_but_quote = "|".join([s for s in ascii_printable.replace('"', "")])
    # any_but_apostrophe = "|".join([s for s in ascii_printable.replace("'", "")])
    open_quote_mark = "«"
    open_par = "܆"
    close_par = "܇"
    plus = "܀"
    CHR = "¶"
    letter = "|".join([ch for ch in string.ascii_letters])
    any_but_quote = letter
    any_but_apostrophe = letter
    digit = "0|1|2|3|4|5|6|7|8|9"
    String = f'"({any_but_quote})*"'
    char = f"\\'({any_but_apostrophe})\\'"
    char = char.replace("\\'", open_quote_mark)
    number = f'(({digit})({digit})*)'
    ident = f'({letter})({letter}|{digit})*'

    Char = f'({char}|(CHR{open_par}{number}{close_par}))'
    BasicSet = f'({String})|({ident})|({Char}(..{Char})?)'
    Set = f'({BasicSet})(({plus}|-){BasicSet})*'
    SetDecl = f'{ident}={Set}'

    print(Set)
    # print(SetDecl)

            # --- Build direct DFA ---
    exp = Expression(Set, is_extended=True)
    root = exp.anlyze_build_tree()
    leafs, nodes = root.build_firstlast_pos()
    followpos = root.followpos(leafs, nodes)
    directed_dfa = root.build_direct_DFA(exp.alphabet.get_alphabet(), followpos, leafs)
    #directed_dfa.get_image()
    print('*'*20)
    print("DFA (direct)")
    print('*'*20)
    print(directed_dfa)

    word = input("Type word: ")
    dfad_status, dfad_time = directed_dfa.simulate(word)
    print(dfad_status)
    print(dfad_time)

if __name__ == '__main__':

    file_name = input("Ingrese el nombre del archivo >> ")
    #TODO: VALIDATE INPUT
    main(file_name)
