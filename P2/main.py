from classes.scanner import Scanner

def main(file_name : str) -> int:
    
    sc = Scanner(file_name)

    # file_analyzed = sc.analyze_file()

    # print(file_analyzed)

        # --- Build direct DFA ---
    exp = Expression(reg_exp, is_extended=True)
    root = exp.anlyze_build_tree()
    leafs, nodes = root.build_firstlast_pos()
    followpos = root.followpos(leafs, nodes)
    directed_dfa = root.build_direct_DFA(exp.alphabet.get_alphabet(), followpos, leafs)
    directed_dfa.get_image()
    print('*'*20)
    print("DFA (direct)")
    print('*'*20)
    print(directed_dfa)

    
if __name__ == '__main__':

    file_name = input("Ingrese el nombre del archivo >> ")
    #TODO: VALIDATE INPUT
    main(file_name)