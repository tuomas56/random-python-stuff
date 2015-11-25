import string
from enum import Enum

class Operator(Enum):
	MULTIPLICATION = "*"
	DIVISION = "/"
	ADDITION = "+"
	SUBTRACTION = "-"

class ParseFail(Exception):
	pass

class NumericNode:
	def __init__(operator,a,b):
		self.operator = operator
		self.a = a
		self.b = b

	def generate(self,parent):
		return self.a.generate(self) + self.operator + self.b.generate(self)

class StringLiteralNode:
	def __init__(self,terminator,contents):
		self.t = terminator
		self.c = contents

	def generate(self,parent):
		return self.t + self.c + self.t

class NumLiteralNode:
	def __init__(self,value):
		self.v = float(value)

	def generate(self,parent):
		return str(self.v)

class VariableNode:
	def __init__(self,name):
		self.name = name

	def generate(self,parent):
		return self.name

class AssignmentNode:
	def __init__(self,var,value):
		self.var = var
		self.value = value

	def generate(self,parent):
		return self.var.generate(self)+"="+self.value.generate(self)

class Lexer:
	def __init__(self,code):
		self.code = list(code)

	def peek(self,n=1):
		return ''.join(self.code[:n])

	def eat(self,n=1):
		s = self.peek(n)
		self.code = self.code[n:]
		return s

	def eatif(self,s):
		if self.peek(len(s)) == s:
			self.eat(len(s))
			return True
		return False

	def eats(self,s):
		assert(self.eatif(s))

	def peekmc(self,a):
		return self.peek() in a

class Parser:
	def parse(code):
		code = Lexer(code)

		def StringLiteralStatement():
			s = code.eat()
			cs = ""
			while code.peek() != s:
				cs += code.eat()
			return StringLiteralNode(s,cs)

		def NumLiteralStatement():
			cs = ""
			while code.peekmc(string.digits + "."):
				cs += code.eat()
			if cs == "":
				raise ParseFail()
			if cs.count(".") > 1:
				raise ParseFail()
			return NumLiteralNode(cs)

		def BracketStatement():
			code.eats("(")
			a = Expression()
			code.eats(")")
			return BracketNode(a)

		def MultiplicationStatement():
			try:
				a = NumLiteralStatement()
				code.eats("*")
				b = Expression()
				return NumericNode(Operator.MULTIPLICATION,a,b)
			except: raise ParseFail()

		def DivisionStatement():
			try:
				a = Expression()
				code.eats("/")
				b = Expression()
				return NumericNode(Operator.DIVISION,a,b)
			except: raise ParseFail()

		def AdditionStatement():
			try:
				a = Expression()
				code.eats("+")
				b = Expression()
				return NumericNode(Operator.ADDITION,a,b)
			except: raise ParseFail()

		def SubtractionStatement():
			try:
				a = Expression()
				code.eats("-")
				b = Expression()
				return NumericNode(Operator.SUBTRACTION,a,b)
			except: raise ParseFail()

		def NumericStatement():
			try:
				return BracketStatement()
			except:
				try:
					return MultiplicationStatement()
				except:
					try:
						return DivisionStatement()
					except:
						try:
							return AdditionStatement()
						except:
							try:
								return SubtractionStatement()
							except:
								try:
									return NumLiteralStatement()
								except:
									raise ParseFail()

		def Variable():
			try:
				assert(code.peekmc(string.ascii_letters + "_$@"))
				s = code.eat()
				while code.peekmc(string.ascii_letters + string.digits + "_$@"):
					s += code.eat()
				return VariableNode(s)
			except: raise ParseFail()

		def OperationStatement():
			try:
				return PropertyStatement()
			except:
				try:
					return CallStatement()
				except:
					try:
						return NumericStatement()
					except:
						raise ParseFail()

		def Expression():
			try:
				return StringLiteralStatement()
			except: 
				try:
					return OperationStatement()
				except: 
					try:
						return Variable()
					except:
						raise ParseFail()

		def AssignmentStatement():
			try:
				var = Variable()
				code.eats("=")
				value = Expression()
				return AssignmentNode(var,value)
			except:	raise ParseFail()

		def Statement():
			try:
				return AssignmentStatement()
			except:
				raise ParseFail()

		try:
			return Statement()
		except:
			raise ParseFail()

Parser.parse("x=10*3")