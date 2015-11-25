class ParseFail(Exception):
	def __init__(self,line,reason):
		self.line = line
		self.reason = reason

	def __str__(self):
		return "Line " + str(self.line) + " - " + str(self.reason)

def tokenize(source):
	source = map(lambda x: (x[0]+1,x[1]),enumerate(source.split("\n")))
	tokens = []
	for linenum,line in source:
		lineTokens = []
		curTok = ""
		while len(line):
			if line[0] == '"' or line[0].isnumeric() or line[0] == '.': #parse literal
				lineTokens.append(("symbol",curTok)) #end current token here and parse literal
				curTok = ""
				if line[0] == '"': #parse string
					line = line[1:] #chomp beginning "
					s = ""
					try:
						while line[0] != '"':
							s += line[0]
							line = line[1:]	
					except:
						raise ParseFail(linenum,"String literal does not terminate.")
					line = line[1:] #chomp ending "
					lineTokens.append(("string",s))
				elif line[0].isnumeric() or line[0] == '.': #parse number
					s = ""
					while len(line) and (line[0].isnumeric() or line[0] == '.'):
						s += line[0]
						line = line[1:]
					try:
						lineTokens.append(("int" if s.isnumeric() else "float",int(s) if s.isnumeric() else float(s)))
					except:
						raise ParseFail(linenum,"Invalid float literal.")
			elif line[0] == '(': #parse bracket expression
				line = line[1:]
				s = ""
				while line[0] != ')':
					s += line[0]
					line = line[1:]
				line = line[1:]
				lineTokens.append(("bracket",tokenize(s)[0]))
			elif line[0] == ' ': #split
				line = line[1:]
				lineTokens.append(("keyword" if curTok in ["if","else","end","sub"] else "symbol",curTok))
				curTok = ""
			elif line[0] in ["+","-","/","*",">","<","%"] + ["==",">=","<=","**","&&","||"]:
				lineTokens.append(("binary_operator",line[0]))
				line = line[1:]
			elif line[0] in ["!"]:
				lineTokens.append(("unary_operator",line[0]))
				line = line[1:]
			else:
				curTok += line[0]
				line = line[1:]
		lineTokens.append(("keyword" if curTok in ["if","else","end","sub"] else "symbol",curTok))
		tokens.append((linenum,list(filter(lambda x: x[1] != '',lineTokens))))
	return tokens

def ttype(token):
	return token[0]

def tvalue(token):
	return token[1]

def parse(tokens):
	ast = []
	while len(tokens):
		(linenum,line),tokens = tokens[0],tokens[1:]
		while len(line):
			if ttype(line[0]) == "keyword":
				if tvalue(line[0]) == "if":
					line = line[1:]
					cond = line
					depth = 1
					ifblock = []
					hasElse = False
					try:
						(linenum,line),tokens = tokens[0],tokens[1:]
					except:
						raise ParseFail(linenum,"Expected statment block.")
					try:
						while True:
							lineblock = []
							while len(line):
								if line[0][1] in ["if","sub"]:
									depth += 1
								elif line[0][1] == "end":
									depth -= 1
								elif line[0][1] == "else":
									hasElse = True
									break
								print
								if depth == 0:
									break
								lineblock.append(line[0])
								line = line[1:]
							if hasElse or depth == 0:
								break
							ifblock.append(lineblock)
							(linenum,line),tokens = tokens[0],tokens[1:]
					except:
						raise ParseFail(linenum,"Expected 'end' keyword.")
					elseblock = []
					depth = 1
					if hasElse:
						try:
							while True:
								lineblock = []
								while len(line):
									if line[0][1] in ["if","sub"]:
										depth += 1
									elif line[0][1] == "end":
										depth -= 1
									if depth == 0:
										break
									lineblock.append(line[0])
									line = line[1:]
								elseblock.append(lineblock)
								(linenum,line),tokens = tokens[0],tokens[1:]
						except:
							raise ParseFail(linenum,"Expected 'end' keyword.")
					return ("if",parse([(linenum,cond)])[0][1],list(map(lambda x: x[1],parse(list(map(lambda x: ((x[0]+linenum+1),x[1]),enumerate(ifblock)))))),list(map(lambda x: x[1],parse(list(map(lambda x: ((x[0]+linenum+1),x[1]),enumerate(elseblock)))))))
				elif tvalue(line[0]) == "else":
					raise ParseFail(linenum,"Unexpected 'else' keyword.")
				elif tvalue(line[0]) == "end":
					raise ParseFail(linenum,"Unexpected 'end' keyword.")
				elif tvalue(line[0]) == "sub":
					name = line[1]
					try:
						(linenum,line),tokens = tokens[0],tokens[1:]
					except:
						raise ParseFail(linenum,"Expected statement block.")
					depth = 1
					block = []
					try:
						while len(tokens):
							lineblock = []
							while len(line):
								if line[0][1] in ["if","sub"]:
									depth += 1
								elif line[0][1] == "end":
									depth -= 1
								if depth == 0:
									break
								lineblock.append(line[0])
								line = line[1:]
							block.append(lineblock)
							(linenum,line),tokens = tokens[0],tokens[1:]
					except:
						raise ParseFail(linenum,"Expected 'end' keyword.")
					ast.append(("sub",name,list(map(lambda x: x[1],parse(list(map(lambda x: ((x[0]+linenum+1),x[1]),enumerate(block))))))))
			elif ttype(line[0]) == "binary_operator":
				ast[-1] = ("binary_operator",tvalue(line[0]),ast[-1],parse([(linenum,[line[1]])])[0][1])
				line = line[2:]
			elif ttype(line[0]) == "unary_operator":
				ast.append(("unary_operator",tvalue(line[0]),parse([(linenum,[line[1]])])[0][1]))
				line = line[2:]
			elif ttype(line[0]) == "symbol":
				print(line[1:])
				if len(line)-1 and ttype(line[1]) == "bracket":
					ast.append(("call",tvalue(line[0]),parse([(linenum,line[1])])[0][1]))
				else:
					ast.append(line[0])
				break
			elif ttype(line[0]) == "bracket":
				ast.append(parse([(linenum,tvalue(line[0])[1])]))
				line = line[1:]
			else:
				ast.append(line[0])
				line = line[1:]
	return ast

print(parse(tokenize("""\
if x > 6
    print "hello"
    print ("hi")
end
\
""")))

