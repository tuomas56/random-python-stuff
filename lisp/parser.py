from funcparserlib.parser import *
from funcparserlib.lexer import make_tokenizer

TOKEN_SPECS = [
	("LB", (r'\(',)),
	("RB", (r'\)',)),
	("WS", (r'\s+',)),
	("STRING", (r'"[^"]*"',)),
	("ATOM", (r'[^"\(\)\s0-9][^"\(\)\s]*',)),
	("NUMBER", (r'[0-9]*\.?[0-9]*',)),
]

lex = lambda x: list(make_tokenizer(TOKEN_SPECS)(x))

class ASTNode:
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return "%s(%s)" % (self.__class__.__name__, str(self.value))

class Number(ASTNode):
	def __init__(self, value):
		try:
			self.value = int(value)
		except:
			self.value = float(value)

class String(ASTNode):
	def __init__(self, value):
		self.value = value[1:-1]

class Atom(ASTNode): pass

class List(ASTNode): pass

ttype = lambda s: some(lambda t: t.type == s)
tokval = lambda t: t.value

ws = skip(maybe(ttype("WS")))

lb = ws + ttype("LB") + ws
rb = ws + ttype("RB") + ws
number = ws + ttype("NUMBER") + ws >> tokval >> Number
string = ws + ttype("STRING") + ws >> tokval >> String
atom = ws + ttype("ATOM") + ws >> tokval >> Atom

literal = number | string

llist = forward_decl()
llist.define(ws + skip(lb) + many(literal | atom | llist) + skip(rb) + ws >> List)

parse = (ws + many(llist | atom | literal) + ws + skip(finished)).parse