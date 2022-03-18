# DLP-Project
Proyecto para el curso de diseño de lenguajes de programación.

### Primera entrega: Generación de AFs basados en una expresión regular

**Requerimientos** 

Se utilizó Python 3.8

Las dependencias se listan en requirements.txt y se instalan de la siguiente forma:

```console
pip install -r requirements.txt
```

El programa se ejecuta de la siguiente forma

```console
python3 main.py
```

Se ingresa la expresión y la palabra y ... sucede la magia.


**Demo 👀** 

Utilicemos una expresión clásica del libro del dragón: (a|b)*abb

Con esto obtenemos:

***NFA***

![alt text](https://github.com/RobertoFigueroa/DLP-Project/blob/main/nfa.png?raw=true)

***DFA por NFA***

![alt text](https://github.com/RobertoFigueroa/DLP-Project/blob/main/dfa.png?raw=true)


***DFA directo de la exp reg***

![alt text](https://github.com/RobertoFigueroa/DLP-Project/blob/main/dfa-direct.png?raw=true)


***Un poco de profiling***

![alt text](https://github.com/RobertoFigueroa/DLP-Project/blob/main/profiling.png?raw=true)

