from classes.expression import Expression

def main(reg_exp : str, word : str) -> int:

    exp = Expression(reg_exp)
    
    if not exp.balanced():
        print("La expresion no esta balanceada, revisar parentesis")
        return 0
    
    print(f"El alfabeto detectado es {exp.alphabet}")

    print(exp.anlyze_build_tree())

if __name__ == '__main__':

    reg_exp = input("Ingrese una expresión regular >> ")
    word = input("Ingrese una palabra a validar >> ")
    #TODO: VALIDATE INPUT
    main(reg_exp, word)