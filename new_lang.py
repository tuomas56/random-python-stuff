from rply import LexerGenerator, ParserGenerator
from rply.token import BaseBox

def construct_lexer():
	lg = LexerGenerator()

	#Literals
	lg.add('NUMBER',r'\d+(\.\d+)?')
	lg.add('STRING',r'\".*?\"')

	#Tokens
	lg.add('OPEN_PAREN',r'\(')
	lg.add('CLOSE_PAREN',r'\)')
	lg.add('INDEX_OPEN',r'\[')
	lg.add('INDEX_CLOSE',r'\]')
	lg.add('NAME',r'[a-zA-Z0-9_]*')
	lg.add('RANGE',r'\.\.\.')
	lg.add('COMMA',',')

	#Operators
	lg.add('ADD',r'\+')
	lg.add('SUBTRACT',r'-')
	lg.add('MULTIPLY',r'\*')
	lg.add('DIVIDE','/')
	lg.add('EXPONENTIATION',r'\*\*')
	lg.add('AND','and')
	lg.add('OR','or')
	lg.add('NOT','not')
	lg.add('XOR','xor')
	lg.add('SELF_APPLY','!')
	lg.add('SINGLE_ARROW','->')
	lg.add('DOUBLE_ARROW','=>')
	lg.add('DOT',r'\.')
	lg.add('IN','in')
	lg.add('GT','>')
	lg.add('LT','<')
	lg.add('LE','<=')
	lg.add('GE','>=')
	lg.add('EQ','==')
	lg.add('NE','!=')

	#Keywords
	lg.add('IF','if')
	lg.add('ELSE','else')
	lg.add('DO','do')
	lg.add('END','end')
	lg.add('DEF','def')
	lg.add('LET','let')
	lg.add('WHILE','while')
	lg.add('FOR','for')

	#Whitespace
	lg.ignore(r"\s+")

	return lg.build()

class Literal(BaseBox):
	def __init__(self, value):
		self.value = value

class Number(Literal):
	pass

class String(Literal):
	pass

class Sequence(Literal):
	pass

class Index(Literal):
	pass

class BinOp(BaseBox):
	def __init__(self, op, left, right):
		self.op = op
		self.left = left
		self.right = right

class UnaryOp(BaseBox):
	def __init__(self, op, right):
		self.op = op
		self.right = right

class Assign(BaseBox):
	def __init__(self, target, value):
		self.target = target
		self.value = value

class Name(Literal):
	pass

class IfExp(BaseBox):
	def __init__(self, cond, ifbody, elsebody):
		self.cond = cond
		self.ifbody = ifbody
		self.elsebody = elsebody

class WhileExp(BaseBox):
	def __init__(self, cond, body):
		self.cond = cond
		self.body = body

class ForExp(BaseBox):
	def __init__(self, name, iter, body):
		self.name = name
		self.iter = iter
		self.body = body

class DefExp(BaseBox):
	def __init__(self, name, args, body):
		self.name = name
		self.args = args
		self.body = body

pg = ParserGenerator(
	['NUMBER','STRING','OPEN_PAREN','CLOSE_PAREN','INDEX_OPEN','INDEX_CLOSE',
	 'NAME','RANGE','ADD','SUBTRACT','MULTIPLY','DIVIDE','EXPONENTIATION','AND',
	 'OR','NOT','XOR','SELF_APPLY','SINGLE_ARROW','DOUBLE_ARROW','DOT','IN',
	 'IF','ELSE','DO','END','DEF','LET','WHILE','FOR','COMMA','GE','LE','LT','GT','EQ','NE'],

	precedence=[('left',['OR','AND','XOR']),
	 ('left',['NOT','IN','GE','LE','GT','LT','EQ','NE']),
	 ('left',['ADD','SUBTRACT']),
	 ('left',['MULTIPLY','DIVIDE']),
	 ('left',['EXPONENTIATION']),
	 ('left',['NUMBER','STRING'])])

@pg.production('expression : NUMBER')
def expression_number(p):
	return Number(float(p[0].getstr()))

@pg.production('expression : STRING')
def expression_string(p):
	return String(p[0].getstr())

@pg.production('expression : OPEN_PAREN expression CLOSE_PAREN')
def expression_bracket(p):
	return p[1]

@pg.production('expression : expression ADD expression')
@pg.production('expression : expression SUBTRACT expression')
@pg.production('expression : expression MULTIPLY expression')
@pg.production('expression : expression DIVIDE expression')
@pg.production('expression : expression EXPONENTIATION expression')
@pg.production('expression : expression OR expression')
@pg.production('expression : expression AND expression')
@pg.production('expression : expression XOR expression')
@pg.production('expression : expression IN expression')
@pg.production('expression : expression GE expression')
@pg.production('expression : expression LE expression')
@pg.production('expression : expression LT expression')
@pg.production('expression : expression GT expression')
@pg.production('expression : expression NE expression')
@pg.production('expression : expression EQ expression')
@pg.production('expression : expression DOT expression')
@pg.production('expression : expression SINGLE_ARROW expression')
@pg.production('expression : expression DOUBLE_ARROW expression')
def expression_binop(p):
	return BinOp(p[1].gettokentype(), p[0], p[2])

parser = pg.build()
lexer = construct_lexer()

print(list(lexer.lex('1 * 2')))