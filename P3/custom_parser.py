
import pickle
import sys
            
class MyParser:

	def __init__(self) -> None:
		self.prev_token = None
		self.current_token = None
		self.prev_char = None
		self.current_char = None
		self.pos = 0
		self.read_tokens()
		self.next_token()

	def read_tokens(self):
		_f = open("tokens", "rb")
		tokens = pickle.load(_f)
		self.token_stream = iter(tokens)

	def next_token(self):
		try:
			self.prev_token = self.current_token
			self.current_token = next(self.token_stream)
			self.pos += 1
		except StopIteration:
			self.current_val = None

    
	def next_char(self):

		try:
			self.prev_char = self.current_char
			self.current_char = next(self.file_stream)

		except StopIteration:
			self.current_char = None

	def expect(self, char):
		if char:
			if self.current_token.ident == char or self.current_token.value == char:
				self.next_token()
				return True
		print(f"Error cerca del caracter {self.pos} esperaba {char} encontre {self.current_token.value} ;(")
		self.next_token()
		return False

	def Expr(self):	
		
		while self.current_token.value in ['number', '-', '('] or self.current_token.ident in ['number', '-', '(']:
			
			self.Stat()
			self.expect(";")
		self.expect(".")	
		return None
	def Stat(self):	
		value=0
		
		value=self.Expression(value)
		print(value)	
		return None
	def Expression(self ,result):	
		result1=result2=0
		
		result1=self.Term(result1)
		
		
		while self.current_token.value in ['+', '-'] or self.current_token.ident in ['+', '-']:
			
			if self.current_token.value in ['+'] or self.curren_token.ident in ['+']:
				
				self.expect("+")
				
				result2=self.Term(result2)
				result1+=result2
			elif self.current_token.value in ['-'] or self.curren_token.ident in ['-']:
				
				self.expect("-")
				
				result2=self.Term(result2)
				result1-=result2
			else:
				print('Error sintáctico')
				return 0
		result=result1	
		return result
	def Term(self ,result):	
		result1=result2=0
		
		result1=self.Factor(result1)
		
		
		while self.current_token.value in ['/', '*'] or self.current_token.ident in ['/', '*']:
			
			if self.current_token.value in ['*'] or self.curren_token.ident in ['*']:
				
				self.expect("*")
				
				result2=self.Factor(result2)
				result1*=result2
			elif self.current_token.value in ['/'] or self.curren_token.ident in ['/']:
				
				self.expect("/")
				
				result2=self.Factor(result2)
				result1/=result2
			else:
				print('Error sintáctico')
				return 0
		result=result1	
		return result
	def Factor(self ,result):	
		signo=1
		
		
		if self.current_token.value in ['-'] or self.curren_token.ident in ['-']:
			
			self.expect("-")
			signo = -1
		
		
		if self.current_token.value in ['number'] or self.curren_token.ident in ['number']:
			result=self.Number(result)
		elif self.current_token.value in ['('] or self.curren_token.ident in ['(']:
			
			self.expect("(")
			
			result=self.Expression(result)
			self.expect(")")
		else:
			print('Error sintáctico')
			return 0
		result*=signo	
		return result
	def Number(self ,result):	
		self.expect('number')
		result = int(self.current_value.value)	
		return result
parser = MyParser()
parser.Expr()
print("Success Parsing!")
