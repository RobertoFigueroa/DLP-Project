
import pickle
import sys
            
file_name = sys.argv[1]
_file = None
try:
    f = open(file_name, "r")
    _file = f.readlines()
    f.close()
except:
    raise("No se pudo leer el archivo, revise al archivo y/o el path: ", file_name)

stream = []
for i in _file:
    for j in i:
        stream.append(str(ord(j)))

        
_f = open("dfa", "rb")
dfa = pickle.load(_f)
        
tokens = dfa.evaluate(stream)
        
print(tokens)
        