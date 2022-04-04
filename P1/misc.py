from structures.Stack import Stack

DIGIT = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def _precedence(op):
	if op == '|':
		return 1
	if op == '*':
		return 2

def precedence(op):
	if (op == '+' or op == '-'):
		return 1
	if (op == '*' or op == '/'):
		return 2
	return 0

def calc(a, b, op):
	if op == '+':
		return a + b
	elif op == '-':
		return a - b
	elif op == '*':
		return a * b
	elif op == '/':
		return a / b

def analyse(word):

	digits = Stack()
	ops = Stack()
	word_size = len(word)
	i = 0
	while i < word_size:
		if word[i] == " ":
			i +=1
			continue
		elif word[i] in DIGIT:
			number = 0
			while i < word_size and word[i] in DIGIT:
				number = (number * 10) + int(word[i])
				i += 1	
			digits.push(number)
			i -= 1
		elif word[i] == '(':
			ops.push(word[i])
		elif word[i] == ')': # encontramos un patron ()
			while not ops.is_empty() and ops.top() != '(':
				val2 = digits.pop()
				val1 = digits.pop()
				op = ops.pop()
				digits.push(calc(val1, val2, op))
			if not ops.is_empty():
				ops.pop()
		else:
			while not ops.is_empty() and (precedence(ops.top()) > precedence(word[i])):
				val2 = digits.pop()
				val1 = digits.pop()
				op = ops.pop()
				digits.push(calc(val1, val2, op))
			ops.push(word[i])
		i += 1
	while not ops.is_empty():
		val2 = digits.pop()
		val1 = digits.pop()
		op = ops.pop()
		digits.push(calc(val1, val2, op))
	return digits.top()




exp = ''
while exp != "!":
	exp = input("Ingrese la expresión matemática >> ")
	print(f"Result: {analyse(exp)}")

