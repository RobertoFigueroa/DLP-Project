# Ref: https://github.com/aixp/pycoco
# Ref:https://github.com/OJP98/py-scanner-generator

from classes.scanner import Scanner
from classes.parser import Parser
from classes.expression import Expression
from classes.cocol_tokens import CocolParser
from classes.gen_code import GenCode, ParserCodeGenerator
from classes.prodNode import ProdNode


import pickle
import sys

import string

def main(file_name : str) -> int:

    # Lectura del archivo COCOL
    sc = Scanner(file_name)
    # Análisis de la lectura de cocol
    file_analyzed = sc.analyze_file()
    # print("This is analyzed analyzzed file ***")
    # print(file_analyzed)
    # print("************************************")

    # Parseo de los Tokens encontrados en
    # el archivo COCOL
    p = Parser(
        file_analyzed.characters,
        file_analyzed.keyword,
        file_analyzed.tokens,
        file_analyzed.ignore,
        file_analyzed.productions
    )

    # ---------- SCANNER ---------------

    # Parseo de los tokens encontrados en 
    # las secciones diferentes a PRODUCCIONES
    p.parse()
    cocol_parser = CocolParser(p.get_result(), p.ignore, p.raw_keywords)
    cocol_parser.generate_dfas()
    dfa = cocol_parser.dfa
    dfa.special_tokens = file_analyzed.special_tokens

    # Serializción del DFA para
    # reconcer tokens
    _file = open("dfa", "wb")
    pickle.dump(dfa, _file)
    _file.close()

    # Generar código para leer archivo de entrada
    code = GenCode()
    code.generate_file()



    # -------------- PARSEO ----------------

    # Parseo de los tokens encontrados en
    # la sección de PRODUCCIONES
    p.parseProductions()
    pnodes = []
    n_terminals = []

    print(p.productions)
    # Generacion de árboles por producciones
    for p in p.productions[::-1]:
        pr = ProdNode(p)
        root = pr.anlyze_build_tree()
        print("in order ***")
        root.in_order(root)
        n_terminals.append(root.value)
        l, _ = root.build_null_first(pnodes)
        root.leafs = l
        root.is_root = True
        root.firstpos_ = root.left.firstpos_
        pnodes.append(root)
    
    print("first is",pnodes[5].firstpos_)

    # Listar instrucciones de las producciones
    instructions = ""
    for r in pnodes[::-1]:
        r.build_instructions(n_terminals)
        instructions = instructions + r.instruction 
    first_instruction = pnodes[-1].value + "()"
    # Generate parser code
    parserCode = ParserCodeGenerator(file_name="custom_parser.py", instructions=instructions)
    parserCode.generate_file(first_instruction)
    
    
    # Fin
    print("Files are ready!!!")





if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print("No file detected")
    else:
        main(sys.argv[1])
