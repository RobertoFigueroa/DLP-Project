from classes.expression import Expression
from prettytable import PrettyTable

def main(reg_exp : str, word : str) -> int:

    exp = Expression(reg_exp)
    
    if not exp.balanced():
        print("La expresion no esta balanceada, revisar parentesis")
        return 0

    if not len(exp.string):
        print("La expresion no contiene caracteres")
        return 0
    
    # -- Build FNA by Thompson and subsets ---

    print(r"""
                                                _______                          
        _..._                                   \  ___ `'.                       
        .'     '.      _.._                        ' |--.\  \       _.._           
        .   .-.   .   .' .._|                       | |    \  '    .' .._|          
        |  '   '  |   | '       __    ,.----------. | |     |  '   | '       __     
        |  |   |  | __| |__  .:--.'. //            \| |     |  | __| |__  .:--.'.   
        |  |   |  ||__   __|/ |   \ |\\            /| |     ' .'|__   __|/ |   \ |  
        |  |   |  |   | |   `" __ | | `'----------' | |___.' /'    | |   `" __ | |  
        |  |   |  |   | |    .'.''| |              /_______.'/     | |    .'.''| |  
        |  |   |  |   | |   / /   | |_             \_______|/      | |   / /   | |_ 
        |  |   |  |   | |   \ \._,\ '/                             | |   \ \._,\ '/ 
        '--'   '--'   |_|    `--'  `"                              |_|    `--'  `"  
    """)
    print('*'*20)
    print("NFA")
    print('*'*20)
    root = exp.anlyze_build_tree()
    root.build_NFA()
    nfa = root.nfa
    print("This is NFA")
    print(nfa)
    nfa.get_image()
    print('*'*20)
    print("DFA with NFA")
    print('*'*20)
    dfa = nfa.build_DFA()
    dfa.get_image()
    print("This is DFA")
    print(dfa)

    # --- Build direct DFA ---
    exp = Expression(reg_exp, is_extended=True)
    root = exp.anlyze_build_tree()
    leafs, nodes = root.build_firstlast_pos()
    followpos = root.followpos(leafs, nodes)
    directed_dfa = root.build_direct_DFA(exp.alphabet.get_alphabet(), followpos, leafs)
    directed_dfa.get_image()
    print("This is DFA (direct cons)")
    print(directed_dfa)

    #--- Simulation ---
    print("Simulating... ")
    nfa_status, nfa_time = nfa.simulate(word)
    dfa_status, dfa_time = dfa.simulate(word)
    dfad_status, dfad_time = dfa.simulate(word)

    table = PrettyTable()
    table.field_names = ["FA", "Status", "Time"]
    table.add_rows(
        [
            ["NFA", "Si" if nfa_status else "No", nfa_time],
            ["DFA", "Si" if dfa_status else "No", dfa_time],
            ["DFA direct", "Si" if dfad_status else "No", dfad_time]
        ]
    )

    print(table)

    
if __name__ == '__main__':

    reg_exp = input("Ingrese una expresión regular >> ")
    word = input("Ingrese una palabra a validar >> ")
    #TODO: VALIDATE INPUT
    main(reg_exp, word)