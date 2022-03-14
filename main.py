from classes.expression import Expression

def main(reg_exp : str, word : str) -> int:

    exp = Expression(reg_exp)
    
    if not exp.balanced():
        print("La expresion no esta balanceada, revisar parentesis")
        return 0

    # TODO: Check for empty expresion
    
    print(f"El alfabeto detectado es {exp.alphabet}")

    # -- Build FNA by Thompson and subsets ---

    root = exp.anlyze_build_tree()
    root.build_NFA() #
    nfa = root.nfa
    # print("This is nfa")
    # print(nfa)
    # nfa.get_image()
    # dfa = nfa.build_DFA()
    # dfa.get_image()
    # print("This is DFA")
    # print(dfa)

    # --- Build direct DFA ---
    exp = Expression(reg_exp, is_extended=True)
    root = exp.anlyze_build_tree()
    leafs, nodes = root.build_firstlast_pos()
    followpos = root.followpos(leafs, nodes)
    print(followpos)
    directed_dfa = root.build_direct_DFA(exp.alphabet.get_alphabet(), followpos, leafs)
    print(directed_dfa)

if __name__ == '__main__':

    reg_exp = input("Ingrese una expresión regular >> ")
    word = input("Ingrese una palabra a validar >> ")
    #TODO: VALIDATE INPUT
    main(reg_exp, word)