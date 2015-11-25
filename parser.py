binary_operators = sorted(["==","=",">=","<=",">","<","&&","||","+","-","*","/","**","!!","%"],key=len,reverse=True)
unary_operators = sorted(["!"],key=len,reverse=True)
keywords = sorted(["return","if","else","end","func"],key=len,reverse=True)
def tokenize(source):
	source = list(map(list,source.split("\n")))
	tokens = []
	for linenum,line in enumerate(source):
		lineTokens = []
		def eat(n=1):
			nonlocal line
			chars,line=line[:n],line[n:]
			return chars[0] if len(chars) == 1 else ''.join(chars)
		def peek(n=1):
			nonlocal line
			return line[:n][0] if len(line[:n]) == 1 else ''.join(line[:n])
		def eats(string):
			if peek(len(string)) == string:
				return eat(len(string))
			return False
		def peek1(arr):
			for s in arr:
				if peek(len(s)) == s:
					return True
			return False
		def eat1(arr):
			for s in arr:
				x = eats(s)
				if x:
					return x
		curTok = ""
		while len(line):
			if peek().isnumeric() or peek() == ".": #parse number
				num = ""
				if eats("."): #parse float beginning with .
					while len(line) and peek().isnumeric():
						num += eat()
					num = float("0."+num+"0")
				elif peek().isnumeric(): #parse int/float
					fp = ""
					while len(line) and peek().isnumeric():
						fp += eat()
					fp = int(fp) #assume int
					if eats("."): #parse float
						dp = ""
						while len(line) and peek().isnumeric():
							dp += eat()
						fp = fp + float("0."+dp+"0")
					num = fp
				lineTokens.append((('int' if isinstance(num,int) else 'float'),num))
			elif peek() == '"' or peek() == "'": #parse string
					terminator = eat()
					ls = ""
					while len(line) and peek() != terminator:
						ls += eat()
					eat()
					lineTokens.append(('string',ls))
			elif eats("["): #parse array
				la = []
				curTok = ""
				depth = 1
				while len(line) and depth:
					s = eat()
					if s == "[":
						depth += 1
						curTok += "["
					elif s == "]":
						depth -= 1
						if depth > 0:
							curTok += "]"
					elif s == "," and depth == 1:
						if curTok != "":
							la.append(curTok)
							curTok = ""
					else:
						curTok += s
				if curTok != "":
					la.append(curTok)
				la = list(map(lambda x: x[0],map(tokenize,la)))
				lineTokens.append(('array',la))
			elif eats("("):
				lineTokens.append(('paren','open'))
			elif eats(")"):
				lineTokens.append(('paren','close'))
			elif peek1(binary_operators):
				lineTokens.append(('binary_operator',eat1(binary_operators)))
			elif peek1(unary_operators):
				lineTokens.append(('unary_operator',eat1(unary_operators)))
			elif peek1(keywords):
				lineTokens.append(('keyword',eat1(keywords)))
			elif eat1(["\t"," "]):
				if curTok != "":
					lineTokens.append(('symbol',curTok))
					curTok = ""
			else:
				curTok += eat()
		if curTok != "" and curTok[0] != "[":
			lineTokens.append(('symbol',curTok))
			curTok = ""
		if lineTokens != []:
			tokens.append(lineTokens)
	newtoks = []
	for line in tokens:
		for token in line:
			newtoks.append(token)
		newtoks.append(('control','newline'))
	return newtoks[:-1]

def lexer(tokens):
	ast = []
	while len(tokens):
		def ttype():
			nonlocal tokens
			return tokens[0][0]
		def tvalue():
			nonlocal tokens
			return tokens[0][1]
		def peek():
			nonlocal tokens
			return tokens[0]
		def eat():
			nonlocal tokens
			token,tokens = tokens[0],tokens[1:]
			return token 
		if ttype() == "binary_operator":
			operand_a = ast[-1]
			cur = eat()
			operand_b = eat()
			if operand_b[0] == "paren":
				if operand_b[1] == "close":
					raise ParseFail()
				toks = []
				depth = 1
				while depth:
					token = eat()
					if token == ('paren','close'):
						depth -= 1
					elif token == ('paren','open'):
						depth += 1
					toks.append(token)
				operand_b = ('bracket',lexer(toks[:-1]))
			ast[-1] = ('binary_operation',cur[1],operand_a,operand_b)
		elif ttype() == "unary_operator":
			operand = tokens[1]
			ast.append(('unary_operation',tvalue(),operand))
			eat()
			eat()
		elif ttype() == "paren":
			if tvalue() == "close":
				raise ParseFail()
			eat()
			toks = []
			depth = 1
			while depth:
				token = eat()
				if token == ('paren','close'):
					depth -= 1
				elif token == ('parent','open'):
					depth += 1
				toks.append(token)
			ast.append(('bracket',lexer(toks[:-1])))
		elif ttype() == "keyword":
			if tvalue() == "func":
				eat()
				name = eat()
				if peek() == ('control','newline'):
					eat()
				else:
					raise ParseFail()
				statements = []
				depth = 1
				while depth:
					s = eat()
					if s[0] == "keyword" and s[1] in ["if","func"]:
						depth += 1
					elif s == ('keyword','end'):
						depth -= 1
					statements.append(s)
				statments = lexer(statements[:-2])
				ast.append(('function',name[1],statments))
			elif tvalue() == "if":
				eat()
				cond = []
				while peek() != ('control','newline'):
					cond.append(eat())
				eat()
				ifstatements = []
				depth = 1
				haselse = False
				while depth:
					s = eat()
					if s[0] == "keyword" and s[1] in ["if","func"]:
						depth += 1
					elif s == ('keyword','end'):
						depth -= 1
					elif s == ('keyword','else') and depth == 1:
						haselse = True
						break
					ifstatements.append(s)
				ifstatements = lexer(ifstatements[:(-1 if haselse else -2)])

				elsestatements = []
				while depth:
					s = eat()
					if s[0] == "keyword" and s[1] in ["if","func"]:
						depth += 1
					elif s == ('keyword','end'):
						depth -= 1
					else:
						elsestatements.append(s)
				if len(elsestatements):
					elsestatements = lexer(elsestatements[1:-1])

				ast.append(('if',lexer(cond),ifstatements,elsestatements))	
		else:
			ast.append(eat())
	return ast

class ParseFail(Exception):
	pass