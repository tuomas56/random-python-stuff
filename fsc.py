#FailSafe
#"The code will not blow up in your face iff you write it perfectly."
#a pythonic/ruby-like language.
#a great example of how not to do parsing. or a cli. especially parsing.
#The syntax is sometimes a little ugly and sometimes fairly nice.

import operator
from functools import partial
import platform
import sys
import argparse
from collections import defaultdict

VERSION = "b0.2.0"



#REGION HELPERS

compose = lambda f,g: lambda *args,**kwargs: f(g(*args,**kwargs))
def split(ls,elem):
	result = []
	cur = []
	for el in ls:
		if el == elem:
			if cur != []:
				result.append(cur)
				cur = []
		else:
			cur.append(el)
	if cur != []:
		result.append(cur)
	return result

def key_by_value(d, value):
	return dict(zip(list(d.values()), list(d.keys())))[value]
#ENDREGION HELPERS
#REGION TOKENIZER

			#(operator symbol(s)),arity,precedence
operators = sorted(sorted(
			[(("!!",),2,2),
			 (("**",),2,3),
			 (("~",),1,4),
			 (("*",),2,5),
			 (("/",),2,5),
			 (("//",),2,5),
			 (("%",),2,5),
			 (("+",),2,6),
			 (("-",),2,6),
			 ((">>",),2,7),
			 (("<<",),2,7),
			 (("&",),2,8),
			 (("^",),2,9),
			 (("|",),2,10),
			 (("in",),2,11),
			 (("not in",),2,11),
			 (("<",),2,11),
			 ((">",),2,11),
			 (("<=",),2,11),
			 ((">=",),2,11),
			 (("!=",),2,11),
			 (("==",),2,11),
			 (("not",),1,12),
			 (("and",),2,13),
			 (("or",),2,14),
			 (("?",":"),3,15),
			 (("=",),2,16)],
			 key=compose(len,compose(partial(max,key=len),operator.itemgetter(0))),
			 reverse=True),
			 key=operator.itemgetter(2))

keywords = sorted(
			["if",
			 "else",
			 "def",
			 "return",
			 "end",
			 "for",
			 "while",
			 "of",
			 "do",
			 "unless"],
			 key=len)

def tokenize(source):
	source = source+" "
	while len(source):
		if source[0] == "." or source[0].isnumeric():
			ln = 0
			ls = ""
			while len(source) and source[0].isnumeric():
				source,ls = source[1:],ls + source[0]
			if ls != "":
				ln += int(ls)

			if len(source) and source[0] == ".":
				ln = float(ln)
				source = source[1:]
				ls = ""
				while len(source) and source[0].isnumeric():
					source,ls = source[1:],ls + source[0]
				if ls != "":
					ln += int(ls) / 10**(len(ls))

			yield "float" if isinstance(ln,float) else "int",ln
		elif any([len(source) >= len(op) and source[:len(op)] == op for op in sum(map(operator.itemgetter(0),operators),tuple())]): #matches an operator
			op = next(filter(lambda x: len(source) >= len(x) and source[:len(x)] == x,sum(map(operator.itemgetter(0),operators),tuple())))
			#since operators are unique we only need the first one in the filter.
			source = source[len(op):]
			yield "operator",op
		elif source[0] == "(":
			ls = ""
			depth = 1
			try:
				while True:
					source = source[1:]
					if source[0] == ")":
						depth -= 1
						if depth == 0:
							source = source[1:]
							break
					elif source[0] == "(":
						depth += 1
					ls += source[0]
			except:
				raise SyntaxError("Unexpected EOF while scanning bracket expression - maybe missing close paren.")

			els = list(tokenize(ls))
			if ("comma",None) in els:
				yield "tuple",split(els,("comma",None))
			else:
				yield "bracket",els
		elif source[0] == "[":
			ls = ""
			depth = 1
			try:
				while True:
					source = source[1:]
					if source[0] == "]":
						depth -= 1
						if depth == 0:
							source = source[1:]
							break
					elif source[0] == "[":
						depth += 1
					ls += source[0]
			except:
				raise SyntaxError("Unexpected EOF while scanning list literal - maybe missing close square bracket.")
			yield "list",split(list(tokenize(ls)),("comma",None))
		elif source[0] in ('"',"'"):
			terminator = source[0]
			source = source[1:]
			ls = ""
			try:
				while source[0] != terminator:
					ls += source[0]
					source = source[1:]
				source = source[1:] #chomp terminator
			except:
				raise SyntaxError("Unexpected EOF while scanning string literal - maybe missing string terminator.")
			yield "string",ls
		elif any([len(source) >= len(keywords) and source[:len(keyword)] == keyword and source[len(keyword)] in """("'), \n\t""" for keyword in keywords]):
			keyword = next(filter(lambda x: len(source) >= len(x) and source[:len(x)] == x and source[len(x)] in """("'), \n\t""",keywords))
			source = source[len(keyword):]
			#again, keywords are unique so we only need the first one.
			yield "keyword",keyword
		elif source[0] in (" ","\n","\t"):
			source = source[1:]
		elif source[0] == ",":
			source = source[1:]
			yield ("comma",None)
		else:
			curTok = source[0]
			source = source[1:]
			while len(source) and source[0] not in sum(map(operator.itemgetter(0),operators),tuple()) and source[0] not in """("'), \n\t""":
				curTok += source[0]
				source = source[1:]

			if len(source) and source[0] == "(":
				ls = ""
				depth = 1
				try:
					while True:
						source = source[1:]
						if source[0] == ")":
							depth -= 1
							if depth == 0:
								source = source[1:]
								break
						elif source[0] == "(":
							depth += 1
						ls += source[0]
				except:
					raise SyntaxError("Unexpected EOF while scanning function call - maybe missing close paren.")
				yield "function",curTok,split(list(tokenize(ls)),("comma",None))
			else:
				yield ("keyword" if curTok in keywords else "symbol"),curTok

#ENGREDION TOKENIZER
#REGION PARSER

def parse_ops(tokens):
	tokens = list(tokens)
	ast = []

	for token in tokens:
		if token[0] in ["list","tuple"]:
			ast.append((token[0],[parse_ops(x)[0] for x in token[1]]))
		elif token[0] == "bracket":
			ast.append((token[0],parse_ops(token[1])))
		elif token[0] == "function":
			ast.append((token[0],token[1],[parse_ops(x)[0] for x in token[2]]))
		else:
			ast.append(token)

	tokens = ast
	ast = []

	#scan through operators in order of precedence
	for operator in operators:
		while len(tokens):
			if tokens[0][0] == "operator" and tokens[0][1] in operator[0] and operator[1] != 1:
				ast[-1] = ("operation",tokens[0][1],operator[1],ast[-1]) + ((tokens[1],) if operator[1] == 2 else (tokens[1],tokens[3]) if operator[1] == 3 else tuple())
				tokens = tokens[operator[1]*2-2:]
			elif tokens[0][0] == "operator" and tokens[0][1] in operator[0] and operator[1] == 1:
				ast.append(("operation",tokens[0][1],operator[1],tokens[1]))
				tokens = tokens[2:]
			else:
				ast.append(tokens[0])
				tokens = tokens[1:]
		tokens = ast
		ast = []

	return tokens

def parse_structures(tokens):
	tokens = list(tokens)
	ast = []
	#
	while len(tokens):
		if tokens[0] == ("keyword","do"):
			ls = []
			depth = 1
			try:
				while True:
					tokens = tokens[1:]
					if tokens[0] == ("keyword","end"):
						depth -= 1
						if depth == 0:
							tokens = tokens[1:]
							break
					elif tokens[0] == ("keyword","do"):
						depth += 1
					ls.append(tokens[0])
			except:
				raise SyntaxError("Unexpected EOF while scanning block - maybe missing end keyword.")
			ast.append(("block",parse_structures(ls)))
		else:
			ast.append(tokens[0])
			tokens = tokens[1:]

	tokens = ast
	ast = []

	while len(tokens):
		if tokens[0] == ("keyword","for"):
			try:
				var = tokens[1] 
				iterable = tokens[3]
				loop = tokens[4]
				if loop[0] != "block":
					loop = ("block",[loop])
				ast.append(("for",var,iterable,loop))
			except:
				raise SyntaxError("Malformed for statement.")
			tokens = tokens[5:]
		elif tokens[0] == ("keyword","while"):
			try:
				pred = tokens[1]
				loop = tokens[2]
				ast.append(("while",pred,loop))
			except:
				raise SyntaxError("Malformed while statement.")
			tokens = tokens[3:]
		elif tokens[0] == ("keyword","def"):
			try:
				defn = tokens[1]
				body = tokens[2]
				ast.append(("def",defn,body))
			except:
				raise SyntaxError("Malformed function definition.")
			tokens = tokens[3:]
		elif tokens[0] == ("keyword","return"):
			try:
				ast.append(("return",tokens[1]))
			except:
				raise SyntaxError("Unexpected EOF while parsing return statement - maybe missing return value.")
			tokens = tokens[2:]
		elif tokens[0] == ("keyword","unless"):
			try:
				pred = tokens[1]
				body = tokens[2]
				if body[0] != "block":
					body = ("block",[body])
				if len(tokens) >= 5 and tokens[3] == ("keyword","else"):
					elsebody = tokens[4]
					if elsebody[0] != "block":
						elsebody = ("block",[elsebody])
					ast.append(("unlesselse",pred,body,elsebody))
					tokens = tokens[5:]
				else:
					ast.append(("unless",pred,body))
					tokens = tokens[3:]
			except:
				raise SyntaxError("Malformed unless statement.")
		elif tokens[0] == ("keyword","if"):
			try:
				pred = tokens[1]
				body = tokens[2]
				if body[0] != "block":
					body = ("block",[body])
				if len(tokens) >= 5 and tokens[3] == ("keyword","else"):
					elsebody = tokens[4]
					if elsebody[0] != "block":
						elsebody = ("block",[elsebody])
					ast.append(("ifelse",pred,body,elsebody))
					tokens = tokens[5:]
				else:
					ast.append(("if",pred,body))
					tokens = tokens[3:]
			except:
				raise SyntaxError("Malformed if statement.")
		elif not isinstance(tokens[0],tuple):
			ast.append(tokens[0])
			tokens = tokens[1:]
		elif tokens[0][0] in ["tuple","list"]:
			ast.append((tokens[0][0],[tuple(parse_structures(x)) for x in tokens[0][1]]))
			tokens = tokens[1:]
		elif tokens[0][0] == "bracket":
			ast.append(("bracket",parse_structures(tokens[0][1])[0]))
			tokens = tokens[1:]
		elif tokens[0][0] == "function":
			ast.append(("function",tokens[0][1],[tuple(parse_structures(x)) for x in tokens[0][2]]))
			tokens = tokens[1:]	
		else:
			ast.append(tokens[0])
			tokens = tokens[1:]


	return ast

def parse(code):
	return parse_structures(parse_ops(tokenize(code)))

#ENDREGION PARSER
#REGION INTERPRETER

OP_TABLE = {
	'!!': lambda a, b: a[b],
	'**': lambda a, b: a ** b,
	'~': lambda a: ~a,
	'*': lambda a, b: a * b,
	'/': lambda a, b: a / b,
	'//': lambda a, b: a // b,
	'%': lambda a, b: a % b,
	'+': lambda a, b: a + b,
	'-': lambda a, b: a - b,
	'>>': lambda a, b: a >> b,
	'<<': lambda a, b: a << b,
	'&': lambda a, b: a & b,
	'^': lambda a, b: a ^ b,
	'|': lambda a, b: a | b,
	'in': lambda a, b: a in b,
	'not in': lambda a, b: a not in b,
	'<': lambda a, b: a < b,
	'>': lambda a, b: a > b,
	'<=': lambda a, b: a <= b,
	'>=': lambda a, b: a >= b,
	'!=': lambda a, b: a != b,
	'==': lambda a, b: a == b,
	'not': lambda a: not a,
	'and': lambda a, b: a and b,
	'or': lambda a, b: a or b,
	'?': lambda a, b, c: b if a else c
}

def interpret_one(ast, env):
	if ast[0] == 'symbol':
		return env, env[ast[1]]
	elif ast[0] in ('int', 'float', 'string'):
		return env, ast[1]
	elif ast[0] == 'tuple':
		return env, tuple(map(lambda x: interpret_one(x, env)[1], ast[1]))
	elif ast[0] == 'list':
		return env, list(map(lambda x: interpret_one(x, env)[1], ast[1]))
	elif ast[0] == 'bracket':
		return interpret_one(ast[1], env)
	elif ast[0] == 'operation' and ast[1] == '=':
		assert ast[3][0] == 'symbol'
		env[ast[3][1]] = interpret_one(ast[4], env)[1]
		return env, env[ast[3][1]]
	elif ast[0] == 'operation':
		return env, OP_TABLE[ast[1]](*list(map(lambda x: interpret_one(x, env)[1], ast[3:])))

def interpret(ast, env):
	results = defaultdict(lambda: [])
	for node in ast:
		env, results[len(results)] = interpret_one(node, env)
	return env, sorted(list(results.values()), key=partial(key_by_value, results))

def new_env():
	return dict()



#ENDREGION INTERPRETER
#REGION CLI

def compilerepl():
	print("FailSafe compiler/transliterator version:",VERSION)
	print("Running on platform:",platform.system(),platform.release(),platform.machine(),platform.architecture()[0])
	print("Underlying Python interpreter:",platform.python_implementation(),platform.python_version())
	print("\nEnter your code - line breaks allowed,\nand then enter an empty line to execute the code.")
	print("Use 'quit' to exit.\n")
	env = new_env()
	while True:
		code = ""
		line = input(">>> ")
		while True:
			if line == "":
				break
			elif line == "quit":
				sys.exit()
			else:
				code += "\n"+line
			line = input("... ")
		print(interpret(parse(code), env))
		#env, results = execute(code, env)
		#print(results)

def compileload():
	with open(file,"r") as f:
		print(execute('\n'.join(f.readlines())))

def compilestdin():
	print(execute('\n'.join(sys.stdin.readlines())))

def main():
	parser = argparse.ArgumentParser(description="A pythonic/ruby-like scripting language. Version: "+VERSION)
	inputmodes = parser.add_mutually_exclusive_group()
	inputmodes.add_argument("-repl","-r",help="Start the interactive shell.",action="store_true")
	inputmodes.add_argument("-load","-l",help="Load some code from file.",metavar="FILE")
	inputmodes.add_argument("-stdin","-s",help="Accept input from stdin.",action="store_true")
	args = parser.parse_args()
	if args.repl:
		compilerepl()
	elif args.load:
		compileload()
	elif args.stdin:
		compilestdin()

	if len(sys.argv) < 2:
		parser.print_help()
		sys.exit(1)

if __name__ == "__main__":
	main()

#ENDREGION CLI