from classes.scanner import Scanner

def main(file_name : str) -> int:
    
    sc = Scanner(file_name)

    file_analyzed = sc.analyze_file()

    print(file_analyzed)

    
if __name__ == '__main__':

    file_name = input("Ingrese el nombre del archivo >> ")
    #TODO: VALIDATE INPUT
    main(file_name)