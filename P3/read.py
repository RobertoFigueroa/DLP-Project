import pickle

_f = open("tokens", "rb")
tokens = pickle.load(_f)
_f.close()

print(tokens)