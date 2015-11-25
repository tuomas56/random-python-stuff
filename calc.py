from collections import namedtuple
import sys
import operator
import argparse

tok_map = {'+': 'ADD', '-': 'MINUS','*': 'MULTIPLY','/': 'DIVIDE', '**': 'EXPONENTIATION', '(': 'LEFT_PAREN', ')': 'RIGHT_PAREN'}
tok_map_inv = dict(zip(list(tok_map.values()),list(tok_map.keys())))

op_func = {'ADD': operator.add, 'MINUS': operator.sub, 'MULTIPLY': operator.mul, 'DIVIDE': operator.truediv, 'EXPONENTIATION': operator.pow}

op_precendence = ['EXPONENTIATION', 'MULTIPLY', 'DIVIDE', 'ADD', 'MINUS']

Token = namedtuple('Token','name value')

def tokenize(source):
	tokens = []
	curtok = ""

	while source:
		token, *source = source
		if token in tok_map:
			if curtok:
				tokens.append(Token('NUM',float(curtok)))
				curtok = ""
			if token == "*" and len(source) and source[0] == "*":
				_, *source = source
				token = "**"
			tokens.append(Token(tok_map[token],None))
		elif token in '\t\n ':
			if curtok:
				tokens.append(Token('NUM',float(curtok)))
				curtok = ""
		else:
			curtok += token
	if curtok:
		tokens.append(Token('NUM',float(curtok)))
	return tokens

class Bracket:
	def __init__(self, value):
		self.value = value

	def __repr__(self):
		return "(%s)" % self.value

	def eval(self):
		return self.value[0].eval()

def parse_brackets(tokens):
	ast = []

	while tokens:
		node, *tokens = tokens
		if node == Token('LEFT_PAREN', None):
			depth = 1
			ls = []
			while True:
				node, *tokens = tokens
				if node == Token('RIGHT_PAREN', None):
					depth -= 1
					if not depth:
						break
				elif node == Token('LEFT_PAREN', None):
					depth += 1
				ls.append(node)
			ast.append(Bracket(parse_brackets(ls)))
		else:
			ast.append(node)
	return ast

class BinOp:
	def __init__(self, left, op, right):
		self.left, self.op, self.right = left, op, right

	def __repr__(self):
		return '%s %s %s' % (self.left, tok_map_inv[self.op], self.right)

	def eval(self):
		return op_func[self.op](self.left.eval(), self.right.eval())

class Number:
	def __init__(self, value):
		self.value = value

	def __repr__(self):
		return "%s" % self.value

	def eval(self):
		return self.value

def parse_binops(tokens):
	ast = []

	for operator in op_precendence:
		while tokens:
			node, *tokens = tokens
			if isinstance(node, Token) and node.name == operator:
				right, *tokens = tokens
				if isinstance(right, Bracket):
					right = Bracket(parse_binops(node.value))
				elif isinstance(right, Token) and right.name == 'NUM':
					right = Number(right.value)
				ast[-1] = BinOp(ast[-1], node.name, right)
			elif isinstance(node, Token) and node.name == 'NUM':
				ast.append(Number(node.value))
			elif isinstance(node, Bracket):
				ast.append(Bracket(parse_binops(node.value)))
			else:
				ast.append(node)
		tokens = ast
		ast = []

	return tokens

def eval_exp(ast):
	results = []

	for node in ast:
		results.append(node.eval())

	if len(results) != 1:
		raise SyntaxError('One statement per line only!')

	return results[0]

def repl():
	hist = ""
	while True:
		value = input('>>> ')
		value = value.replace('_',str(hist))
		hist = eval_exp(parse_binops(parse_brackets(tokenize(value))))
		print(hist)

def from_file(filename):
	with open(filename, 'r') as f:
		print(eval_exp(parse_binops(parse_brackets(tokenize(f.read())))))

def from_stdin():
	print(eval_exp(parse_binops(parse_brackets(tokenize(sys.stdin.read())))))

parser = argparse.ArgumentParser(description="A simple calculator.")
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('--repl', action='store_true')
group.add_argument('--stdin', action='store_true')
group.add_argument('--file', metavar='FILE')

flags = parser.parse_args(sys.argv[1:])

if flags.repl == True:
	repl()
elif flags.stdin == True:
	from_stdin()
else:
	from_file(flags.file)