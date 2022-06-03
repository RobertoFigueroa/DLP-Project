
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
		f_tokens  = []
		for i in tokens:
				if i.ident != 'nontoken':
						f_tokens.append(i)
		self.token_stream = iter(f_tokens)

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

	def MyCOCOR(self):	
		CompilerName = ""
		
		EndName = ""
		
		self.expect("COMPILER")
		
		CompilerName=self.Ident(CompilerName)
		
		print("Nombre Inicial del Compilador: ",CompilerName)
		
		
		if self.current_token.value in ['startcode'] or self.current_token.ident in ['startcode']:
			self.Codigo()
		
		self.Body()
		
		self.expect("END")
		
		EndName=self.Ident(EndName)
		print("Nombre Final del Compilador: ",EndName)	
		return None
	def Body(self):	
		self.Characters()
		
		
		if self.current_token.value in ['KEYWORDS'] or self.current_token.ident in ['KEYWORDS']:
			self.Keywords()
		
		self.Tokens()
		self.Productions()	
		return None
	def Characters(self):	
		CharName = ""
		
		Counter = 0
		
		self.expect("CHARACTERS")
		
		print("LEYENDO CHARACTERS")
		
		while self.current_token.value in ['ident'] or self.current_token.ident in ['ident']:
			
			CharName=self.Ident(CharName)
			
			Counter+=1
			
			print("Char Set {}: {}".format(Counter,CharName))
			
			self.expect("=")
			
			self.CharSet()
			
			while self.current_token.value in ['-', '+'] or self.current_token.ident in ['-', '+']:
				
				if self.current_token.value in ['+'] or self.current_token.ident in ['+']:
					
					self.expect("+")
					self.CharSet()
				elif self.current_token.value in ['-'] or self.current_token.ident in ['-']:
					
					self.expect("-")
					self.CharSet()
				else:
					print('Error sintáctico')
					return 0	
		return None
	def Keywords(self):	
		KeyName = ""
		
		StringValue = ""
		
		Counter = 0
		
		self.expect("KEYWORDS")
		
		print("LEYENDO KEYWORDS")
		
		while self.current_token.value in ['ident'] or self.current_token.ident in ['ident']:
			
			KeyName=self.Ident(KeyName)
			
			Counter+=1
			
			print("KeyWord {}: {}".format(Counter,KeyName))
			
			self.expect("=")
			
			StringValue=self.String(StringValue)
			self.expect(".")	
		return None
	def Tokens(self):	
		TokenName = ""
		
		Counter = 0
		
		self.expect("TOKENS")
		
		print("LEYENDO TOKENS")
		
		while self.current_token.value in ['ident'] or self.current_token.ident in ['ident']:
			
			TokenName=self.Ident(TokenName)
			
			Counter+=1
			
			print("Token {}: {}".format(Counter,TokenName))
			
			self.expect("=")
			
			self.TokenExpr()
			
			
			if self.current_token.value in ['EXCEPT'] or self.current_token.ident in ['EXCEPT']:
				self.ExceptKeyword()
			self.expect(".")	
		return None
	def Productions(self):	
		Counter = 0
		
		self.expect("PRODUCTIONS")
		
		ProdName = ""
		
		print("LEYENDO PRODUCTIONS")
		
		while self.current_token.value in ['ident'] or self.current_token.ident in ['ident']:
			
			ProdName=self.Ident(ProdName)
			
			Counter+=1
			
			print("Production {}: {}".format(Counter,ProdName))
			
			
			if self.current_token.value in ['<'] or self.current_token.ident in ['<']:
				self.Atributos()
			
			self.expect("=")
			
			
			if self.current_token.value in ['startcode'] or self.current_token.ident in ['startcode']:
				self.Codigo()
			
			self.ProductionExpr()
			self.expect(".")	
		return None
	def ExceptKeyword(self):	
		self.expect("EXCEPT")
		self.expect("KEYWORDS")	
		return None
	def ProductionExpr(self):	
		self.ProdTerm()
		
		while self.current_token.value in ['|'] or self.current_token.ident in ['|']:
			
			self.expect("|")
			self.ProdTerm()	
		return None
	def ProdTerm(self):	
		self.ProdFactor()
		
		while self.current_token.value in ['char', '(', 'ident', '{', '[', 'string'] or self.current_token.ident in ['char', '(', 'ident', '{', '[', 'string']:
			self.ProdFactor()	
		return None
	def ProdFactor(self):	
		
		if self.current_token.value in ['char', 'ident', 'string'] or self.current_token.ident in ['char', 'ident', 'string']:
			self.SymbolProd()
		elif self.current_token.value in ['{', '[', '('] or self.current_token.ident in ['{', '[', '(']:
			
			if self.current_token.value in ['('] or self.current_token.ident in ['(']:
				
				self.expect("(")
				
				self.ProductionExpr()
				self.expect(")")
			elif self.current_token.value in ['{', '['] or self.current_token.ident in ['{', '[']:
				
				if self.current_token.value in ['['] or self.current_token.ident in ['[']:
					
					self.expect("[")
					
					self.ProductionExpr()
					self.expect("]")
				elif self.current_token.value in ['{'] or self.current_token.ident in ['{']:
					
					self.expect("{")
					
					self.ProductionExpr()
					self.expect("}")
				else:
					print('Error sintáctico')
					return 0
			else:
				print('Error sintáctico')
				return 0
		else:
			print('Error sintáctico')
			return 0
		
		if self.current_token.value in ['startcode'] or self.current_token.ident in ['startcode']:
			self.Codigo()	
		return None
	def SymbolProd(self):	
		SV = ""
		
		IN = ""
		
		if self.current_token.value in ['string'] or self.current_token.ident in ['string']:
			
			SV=self.String(SV)
			print("String en Production: {}".format(SV))
		elif self.current_token.value in ['char', 'ident'] or self.current_token.ident in ['char', 'ident']:
			
			if self.current_token.value in ['char'] or self.current_token.ident in ['char']:
				self.expect('char')
			elif self.current_token.value in ['ident'] or self.current_token.ident in ['ident']:
				
				IN=self.Ident(IN)
				
				print("Identificador en Production: {}".format(IN))
				
				if self.current_token.value in ['<'] or self.current_token.ident in ['<']:
					self.Atributos()
			else:
				print('Error sintáctico')
				return 0
		else:
			print('Error sintáctico')
			return 0	
		return None
	def Codigo(self):	
		self.expect('startcode')
		
		
		while self.current_token.value in ['ANY'] or self.current_token.ident in ['ANY']:
			self.expect('ANY')
		self.expect('endcode')	
		return None
	def Atributos(self):	
		self.expect("<")
		
		
		while self.current_token.value in ['ANY'] or self.current_token.ident in ['ANY']:
			self.expect('ANY')
		self.expect(">")	
		return None
	def TokenExpr(self):	
		self.TokenTerm()
		
		while self.current_token.value in ['|'] or self.current_token.ident in ['|']:
			
			self.expect("|")
			self.TokenTerm()	
		return None
	def TokenTerm(self):	
		self.TokenFactor()
		
		while self.current_token.value in ['char', '{', 'ident', '[', '(', 'string'] or self.current_token.ident in ['char', '{', 'ident', '[', '(', 'string']:
			self.TokenFactor()	
		return None
	def TokenFactor(self):	
		if self.current_token.value in ['char', 'ident', 'string'] or self.current_token.ident in ['char', 'ident', 'string']:
			self.SimbolToken()
		elif self.current_token.value in ['(', '{', '['] or self.current_token.ident in ['(', '{', '[']:
			
			if self.current_token.value in ['('] or self.current_token.ident in ['(']:
				
				self.expect("(")
				
				self.TokenExpr()
				self.expect(")")
			elif self.current_token.value in ['{', '['] or self.current_token.ident in ['{', '[']:
				
				if self.current_token.value in ['['] or self.current_token.ident in ['[']:
					
					self.expect("[")
					
					self.TokenExpr()
					self.expect("]")
				elif self.current_token.value in ['{'] or self.current_token.ident in ['{']:
					
					self.expect("{")
					
					self.TokenExpr()
					self.expect("}")
				else:
					print('Error sintáctico')
					return 0
			else:
				print('Error sintáctico')
				return 0
		else:
			print('Error sintáctico')
			return 0	
		return None
	def SimbolToken(self):	
		IdentName = ""
		
		StringValue = ""
		
		if self.current_token.value in ['string'] or self.current_token.ident in ['string']:
			StringValue=self.String(StringValue)
		elif self.current_token.value in ['char', 'ident'] or self.current_token.ident in ['char', 'ident']:
			
			if self.current_token.value in ['char'] or self.current_token.ident in ['char']:
				self.expect('char')
			elif self.current_token.value in ['ident'] or self.current_token.ident in ['ident']:
				
				IdentName=self.Ident(IdentName)
				print("Identificador en Token: {}".format(IdentName))
			else:
				print('Error sintáctico')
				return 0
		else:
			print('Error sintáctico')
			return 0	
		return None
	def CharSet(self):	
		IdentName = ""
		
		StringValue = ""
		
		if self.current_token.value in ['string'] or self.current_token.ident in ['string']:
			StringValue=self.String(StringValue)
		elif self.current_token.value in ['ANY', 'ident', 'charinterval', 'charnumber', 'char'] or self.current_token.ident in ['ANY', 'ident', 'charinterval', 'charnumber', 'char']:
			
			if self.current_token.value in ['charinterval', 'charnumber', 'char'] or self.current_token.ident in ['charinterval', 'charnumber', 'char']:
				self.Char()
			elif self.current_token.value in ['ANY', 'ident'] or self.current_token.ident in ['ANY', 'ident']:
				
				if self.current_token.value in ['ANY'] or self.current_token.ident in ['ANY']:
					self.expect("ANY")
				elif self.current_token.value in ['ident'] or self.current_token.ident in ['ident']:
					
					IdentName=self.Ident(IdentName)
					print("Identificador en CharSet: {}".format(IdentName))
				else:
					print('Error sintáctico')
					return 0
			else:
				print('Error sintáctico')
				return 0
		else:
			print('Error sintáctico')
			return 0	
		return None
	def Char(self):	
		if self.current_token.value in ['char'] or self.current_token.ident in ['char']:
			self.expect('char')
		elif self.current_token.value in ['charnumber', 'charinterval'] or self.current_token.ident in ['charnumber', 'charinterval']:
			
			if self.current_token.value in ['charnumber'] or self.current_token.ident in ['charnumber']:
				self.expect('charnumber')
			elif self.current_token.value in ['charinterval'] or self.current_token.ident in ['charinterval']:
				self.expect('charinterval')
			else:
				print('Error sintáctico')
				return 0
		else:
			print('Error sintáctico')
			return 0	
		return None
	def String(self ,S):	
		self.expect('string')
		S = self.prev_token.value	
		return S
	def Ident(self ,S):	
		self.expect('ident')
		S = self.prev_token.value	
		return S
parser = MyParser()
parser.MyCOCOR()
print("Success Parsing!")
