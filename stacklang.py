import operator

def tokenize(source):
	seperators = ("\t","\n"," ")
	terminators = ("'",'"')
	source = list(source)
	tokens = []
	cur = ""
	atom = False
	while len(source):
		if source[0] in terminators:
			if cur != "":
				tokens.append(("atom" if atom else "symbol",cur))
				cur = ""
			atom = False
			terminator,*source = source
			ls = ""
			try:
				while source[0] != terminator:
					ls,source = (ls + source[0]),source[1:]
				source = source[1:]
			except:
				raise SyntaxError("Unexpected EOF while scanning string literal.")
			tokens.append(("string",ls))
		elif source[0] == "#":
			if cur != "":
				tokens.append(("atom" if atom else "symbol",cur))
				cur = ""
			atom = False
			_,*source = source
			ls = ""
			try:
				while source[0] != '#':
					_,*source = source
				_,*source = source
			except:
				raise SyntaxError("Unexpected EOF while scanning comment.")
		elif source[0] == "@":
			atom = True
			source = source[1:]
		elif source[0] in seperators:
			source = source[1:]
			if cur != "":
				tokens.append(("atom" if atom else "symbol",cur))
				cur = ""
			atom = False
		elif source[0] in ("[","]"):
			if cur != "":
				tokens.append(("atom" if atom else "symbol",cur))
				cur = ""
			atom = False
			tokens.append(("symbol",source[0]))
			source = source[1:]
		elif source[0] == "{":
			if cur != "":
				tokens.append(("atom" if atom else "symbol",cur))
				cur = ""
			atom = False
			source = source[1:]
			ls = ""
			try:
				depth = 1
				while depth:
					if source[0] == "{":
						depth += 1
					elif source[0] == "}":
						depth -= 1
						if not depth:
							break
					ls,source = (ls + source[0]),source[1:]
				source = source[1:]
			except:
				raise SyntaxError("Unexpected EOF while scanning function literal.")
			arity,*ls = tokenize(ls+" ")
			if arity == ("symbol","-"):
				arity = ("int",-1)
			checktype(arity,"int")
			tokens.append(("function",arity[1],ls))
		elif source[0].isnumeric() or source[0] == ".":
			if cur != "":
				tokens.append(("atom" if atom else "symbol",cur))
				cur = ""
			atom = False
			ln = ""
			while len(source) and source[0].isnumeric():
				ln,source = (ln + source[0]),source[1:]
			if len(ln):
				ln = int(ln)
			else:
				ln = 0
			if len(source) and source[0] == ".":
				ln,source = float(ln),source[1:]
			ld = ""
			while len(source) and source[0].isnumeric():
				ld,source = (ld + source[0]),source[1:]
			if len(ld):
				ln += float("."+ld)
			tokens.append((("int" if isinstance(ln,int) else "float"),ln))
		else:
			cur,source = (cur + source[0]),source[1:]
	return tokens

def eval(tokens,env={},trace=False):
	stack = []
	stacks = []
	for token in tokens:
		if token[0] == "symbol":
			if token[1] == "[":
				stacks.append(stack)
				stack = []
				continue
			elif token[1] == "]":
				stack = stacks.pop() + stack
				continue

			arity = map(operator.itemgetter(0),env[token[1]])
			for a in sorted(list(arity),reverse=True):
				if len(stack) >= a:
					arity = a
					break
				elif a == -1:
					arity = a
					break
			else:
				arity = map(operator.itemgetter(0),env[token[1]])
				raise ValueError("Not enough values on stack for "+str(token[1])+"/"+str(min(arity)))
			if arity == -1:
				args,stack= stack,[]
			else:
				args,stack = stack[-arity:],stack[:-arity]
			f = enumerate(map(operator.itemgetter(1),env[token[1]]))
			arities = list(enumerate(map(operator.itemgetter(0),env[token[1]])))
			f = next(filter(lambda x: arities[x[0]][1] == arity,f))[1]
			result,env,stack = f(*args,env=env,stack=stack)
			if result != ("none",False):
				stack.append(result)
		else:
			stack.append(token)
		if trace:
			print(token,stack)
	return stack,env

def checktype(x,*t):
	try:
		assert(x[0] in t)
	except:
		raise TypeError("Required type "+' or '.join(t)+" got type "+x[0])

def checkseq(x):
	try:
		assert(x[0].startswith("seq"))
	except:
		raise TypeError("Required seq, got "+x[0])

def add(x,y,env={},stack=[]):
	checktype(x,"int","float")
	checktype(y,"int","float")
	if "float" in (x[0],y[0]):
		return ("float",x[1]+y[1]),env,stack
	else:
		return ("int",x[1]+y[1]),env,stack

def sub(x,y,env={},stack=[]):
	checktype(x,"int","float")
	checktype(y,"int","float")
	if "float" in (x[0],y[0]):
		return ("float",x[1]-y[1]),env,stack
	else:
		return ("int",x[1]-y[1]),env,stack

def neg(x,env={},stack=[]):
	checktype(x,"int","float")
	return (x[0],-x[1]),env,stack

def _sum(*args,env={},stack=[]):
	if not len(args):
		raise ValueError("At least 1 value required for sum.")
	if not all([arg[0] == args[0][0] for arg in args]):
		raise TypeError("Can't sum with multiple types.")
	if args[0][0] == "string":
		raise TypeError("Can't sum strings. use 'seq join'")
	return (args[0][0],sum([arg[1] for arg in args[:-1][::-1]],args[-1][1])),env,stack

def seq(*args,env={},stack=[]):
	if not all([arg[0] == args[0][0] for arg in args]):
		raise TypeError("Can't construct list of multiple types.")
	return ("seq<"+args[0][0]+">",args),env,stack

def join(ls,env={},stack=[]):
	checktype(ls,"seq<string>")
	return ("string",''.join(map(operator.itemgetter(1),ls[1]))),env,stack

def concat(a,b,env={},stack=[]):
	checkseq(a)
	checkseq(b)
	if a[0] != b[0]:
		raise TypeError("Can't concat seqs of different types.")
	return (a[0],a[1]+b[1]),env,stack

def el(type,env={},stack=[]):
	checktype(type,"string")
	return ("seq<"+type[1]+">",tuple()),env,stack

def args(*args,env={},stack=[]):
	return ("arglist",args),env,stack

def splat(args,f,env={},stack=[]):
	if not (args[0] == "arglist" or args[0].startswith("seq")):
		raise TypeError("Can't splat "+args[0]+".")
	checktype(f,"atom")
	arity = map(operator.itemgetter(0),env[f[1]])
	for a in sorted(list(arity),reverse=True):
		if len(args[1]) >= a:
			arity = a
			break
		elif a == -1:
			arity = a
			break
	else:
		arity = map(operator.itemgetter(0),env[f[1]])
		raise ValueError("Not enough values for "+str(f[1])+"/"+str(min(arity)))
	fn = enumerate(map(operator.itemgetter(1),env[f[1]]))
	arities = list(enumerate(map(operator.itemgetter(0),env[f[1]])))
	fn = next(filter(lambda x: arities[x[0]][1] == arity,fn))[1]
	return fn(*args[1],env=env)

def _print(*args,env={},stack=[]):
	print(*[arg[1] for arg in args])
	return ("none",None),env,stack

def _input(prompt,env={},stack=[]):
	return ("string",input(prompt[1])),env,stack

def _map(seq,pred,env={},stack=[]):
	checktype(pred,"atom")
	checkseq(seq)
	fn = enumerate(map(operator.itemgetter(1),env[pred[1]]))
	arities = list(enumerate(map(operator.itemgetter(0),env[pred[1]])))
	try:
		fn = next(filter(lambda x: arities[x[0]][1] == 1,fn))[1]
	except:
		raise ValueError(pred[1]+"/1 not found!")
	vals = []
	for s in seq[1]:
		val,env,stack = fn(s,env=env,stack=stack)
		vals.append(val)
	vals = tuple(vals)
	if len(vals) == 0:
		raise TypeError("Type inference impossible when mapping empty seq!")
	type = "seq<"+vals[0][0]+">"
	return (type,vals),env,stack

def _filter(seq,pred,env={},stack=[]):
	checktype(pred,"atom")
	checkseq(seq)
	fn = enumerate(map(operator.itemgetter(1),env[pred[1]]))
	arities = list(enumerate(map(operator.itemgetter(0),env[pred[1]])))
	try:
		fn = next(filter(lambda x: arities[x[0]][1] == 1,fn))[1]
	except:
		raise ValueError(pred[1]+"/1 not found!")
	vals = []
	for s in seq[1]:
		val,env,stack = fn(s,env=env,stack=stack)
		if val:
			vals.append(s)
	vals = tuple(vals)
	if len(vals) == 0:
		raise TypeError("Type inference impossible when filtering empty seq!")
	type = "seq<"+vals[0][0]+">"
	return (type,vals),env,stack

def _index(seq,index,env={},stack=[]):
	checkseq(seq)
	checktype(index,"int")
	return (seq[0][4:-1],seq[1][index[1]][1]),env,stack

def _len(seq,env={},stack=[]):
	checkseq(seq)
	return ("int",len(seq[1])),env,stack

def _type(x,env={},stack=[]):
	return ("string",x[0]),env,stack

def eq(a,b,env={},stack=[]):
	return ("bool",a==b),env,stack

def neq(a,b,env={},stack=[]):
	return ("bool",a!=b),env,stack

def ge(a,b,env={},stack=[]):
	return ("bool",a>=b),env,stack

def le(a,b,env={},stack=[]):
	return ("bool",a<=b),env,stack

def gt(a,b,env={},stack=[]):
	return ("bool",a>b),env,stack

def lt(a,b,env={},stack=[]):
	return ("bool",a<b),env,stack

def true(env={},stack=[]):
	return ("bool",True),env,stack

def false(env={},stack=[]):
	return ("bool",False),env,stack

def _str(x,env={},stack=[]):
	return ("string",str(x[1])),env,stack

def _int(x,env={},stack=[]):
	return ("int",int(x[1])),env,stack

def _float(x,env={},stack=[]):
	return ("float",float(x[1])),env,stack

def pop(a,env={},stack=[]):
	return ("none",False),env,stack

def mul(a,b,env={},stack=[]):
	checktype(x,"int","float")
	checktype(y,"int","float")
	if "float" in (x[0],y[0]):
		return ("float",x[1]*y[1]),env,stack
	else:
		return ("int",x[1]*y[1]),env,stack	

def div(a,b,env={},stack=[]):
	checktype(x,"int","float")
	checktype(y,"int","float")
	return ("float",x[1]/y[1]),env,stack

def pow(x,y,env={},stack=[]):
	checktype(x,"int","float")
	checktype(y,"int","float")
	if "float" in (x[0],y[0]):
		return ("float",x[1]**y[1]),env,stack
	else:
		return ("int",x[1]**y[1]),env,stack

def _if(pred,ifblock,elseblock,env={},stack=[]):
	checktype(pred,"bool")
	checktype(ifblock,"atom")
	checktype(elseblock,"atom")
	arity = map(operator.itemgetter(0),env[ifblock[1]])
	for a in sorted(list(arity),reverse=True):
		if len(stack) >= a:
			arity = a
			break
		elif a == -1:
			arity = a
			break
	arity2 = map(operator.itemgetter(0),env[elseblock[1]])
	for a in sorted(list(arity2),reverse=True):
		if len(stack) >= a:
			arity2 = a
			break
		elif a == -1:
			arity2 = a
			break
	fn = enumerate(map(operator.itemgetter(1),env[ifblock[1]]))
	arities = list(enumerate(map(operator.itemgetter(0),env[ifblock[1]])))
	try:
		fn = next(filter(lambda x: arities[x[0]][1] == arity,fn))[1]
	except:
		raise ValueError(ifblock[1]+"/"+str(arity)+" not found!")

	fe = enumerate(map(operator.itemgetter(1),env[elseblock[1]]))
	arities = list(enumerate(map(operator.itemgetter(0),env[elseblock[1]])))
	try:
		fe = next(filter(lambda x: arities[x[0]][1] == arity2,fe))[1]
	except:
		raise ValueError(elseblock[1]+"/"+str(arity2)+" not found!")

	stack2 = stack
	if arity == -1:
		args,stack = stack,[]
	else:
		args,stack = stack[-arity:],stack[:-arity]

	if arity2 == -1:
		args2,stack2 = stack,[]
	else:
		args2,stack2 = stack[-arity2:],stack[:-arity2]


	if pred[1]:
		return fn(*args,env=env,stack=stack)
	else:
		return fe(*args2,env=env,stack=stack)

def _def(name,func,env={},stack=[]):
	checktype(name,'atom')
	checktype(func,'function')
	def wrapper(*args,env={},stack=[]):
		newenv = env.copy()
		newenv['@'] = ("seq",args)
		for i,arg in enumerate(args):
			newenv['@'+str(i+1)] = arg
		stack,newenv = eval(func[2],newenv)
		return stack[0],env,stack
	env[name[1]] = [(func[1],wrapper)]
	return ("none",False),env,stack


def cons(a,b,env={},stack=[]):
	if not (a[0].startswith("seq") or a[0] == "arglist"):
		raise TypeError("Can only cons to seq or arglist.")
	if a[0].startswith("seq") and a[0] != "seq<"+b[0]+">":
		raise TypeError("Can only cons to seq of same type as elem.")
	return (a[0],tuple(list(a[1])+[b])),env,stack

def slice(arr,*args,env={},stack=[]):
	checktype(args[0],"int")
	checktype(args[1],"int")
	if len(args) == 3:
		checktype(args[2],"int")
	if len(args) == 3:
		if args[0][1] == 0:
			if args[1][1] == 0:
				if args[2][1] == 0:
					return (arr[0],arr[1][::]),env,stack
				else:
					return (arr[0],arr[1][::args[2]]),env,stack
			else:
				if args[2][1] == 0:
					return (arr[0],arr[1][:args[1]:]),env,stack
				else:
					return (arr[0],arr[1][:args[1]:args[2]]),env,stack
		else:
			if args[1][1] == 0:
				if args[2][1] == 0:
					return (arr[0],arr[1][args[0]::]),env,stack
				else:
					return (arr[0],arr[1][args[0]::args[2]]),env,stack
			else:
				if args[2][1] == 0:
					return (arr[0],arr[1][args[0]:args[1]:]),env,stack
				else:
					return (arr[0],arr[1][args[0]:args[1]:args[2]]),env,stack

def _range(*args,env={},stack=[]):
	if len(args) == 1:
		checktype(args[0],"int")
		return ("seq<int>",tuple(map(lambda x: ('int',x),range(args[0][1])))),env,stack
	elif len(args) == 2:
		checktype(args[0],"int")
		checktype(args[1],"int")
		return ("seq<int>",tuple(map(lambda x: ('int',x),range(args[0][1],args[1][1])))),env,stack
	elif len(args) == 3:
		checktype(args[0],"int")
		checktype(args[1],"int")
		checktype(args[2],"int")
		return ("seq<int>",tuple(map(lambda x: ('int',x),range(args[0][1],args[1][1],args[2][1])))),env,stack

def _and(a,b,env={},stack=[]):
	checktype(a,"bool")
	checktype(b,"bool")
	return ("bool",a[1] and b[1]),env,stack

def _or(a,b,env={},stack=[]):
	checktype(a,"bool")
	checktype(b,"bool")
	return ("bool",a[1] or b[1]),env,stack

def _not(a,env={},stack=[]):
	checktype(a,"bool")
	return ("bool",not a[1]),env,stack

def atom(x,env={},stack=[]):
	return ("atom",str(x[1])),env,stack

def arg(*args,env={},stack=[]):
	if len(args) == 0:
		return env['@'],env,stack
	else:
		checktype(args[0],"int")
		return env['@'+str(args[0][1])],env,stack

def dup(a,env={},stack=[]):
	return a,env,stack+[a]

def unseq(seq,env={},stack=[]):
	checkseq(seq)
	return ("none",False),env,stack+list(seq[1])

def proc(name,func,env={},stack=[]):
	checktype(name,'atom')
	checktype(func,'function')
	def wrapper(*args,env={},stack=[]):
		newenv = env.copy()
		newenv['@'] = ("seq",args)
		for i,arg in enumerate(args):
			newenv['@'+str(i+1)] = arg
		stack,newenv = eval(func[2],newenv)
		return ("none",False),env,stack
	env[name[1]] = [(func[1],wrapper)]
	return ("none",False),env,stack

def var(name,value,env={},stack=[]):
	checktype(name,'atom')
	def wrapper(env={},stack=[]):
		return value,env,stack
	env[name[1]] = [(0,wrapper)]
	return ("none",False),env,stack

def call(name,*args,env={},stack=[]):
	fn = enumerate(map(operator.itemgetter(1),env[name[1]]))
	arities = list(enumerate(map(operator.itemgetter(0),env[name[1]])))
	try:
		fn = next(filter(lambda x: arities[x[0]][1] == len(args) or arities[x[0]][1] == -1,fn))[1]
	except:
		raise ValueError(name[1]+"/"+str(len(args)) +" not found!")
	return fn(*args,env=env,stack=stack)

def _try(name,errname,env={},stack=[]):
	checktype(name,"atom")
	checktype(errname,"atom")
	try:
		return call(name,tuple(),env=env,stack=stack)
	except:
		return call(errname,tuple(),env=env,stack=stack)

def _del(name,env={},stack=[]):
	checktype(name,"atom")
	if name[1] in env:
		del env[name[1]]
	return ("none",False),env,stack

def fail(message,env={},stack=[]):
	raise Exception(message)

def _bool(x,env={},stack=[]):
	checktype(x,"string")
	if x[1] == "true":
		return ("bool",True),env,stack
	elif x[1] == "false":
		return ("bool",False),env,stack
	else:
		raise ValueError("Can't parse bool.")

def rot(num,env={},stack=[]):
	checktype(num,"int")
	val = stack.pop(-num[1])
	stack.append(val)
	return ("none",False),env,stack

stdenv = {
	'+': [(2,add)],
	'-': [(2,sub),(1,neg)],
	'*': [(2,mul)],
	'/': [(2,div)],
	'**': [(2,pow)],
	'sum': [(-1,_sum)],
	'seq': [(-1,seq)],
	'join': [(1,join)], 
	'concat': [(2,concat)],
	'el': [(1,el)],
	'args': [(-1,args)],
	'splat': [(2,splat)],
	'print': [(-1,_print),(1,_print)],
	'input': [(1,_input)],
	'map': [(2,_map)],
	'filter': [(2,_filter)],
	'!!': [(2,_index)],
	'len': [(1,_len)],
	'type': [(1,_type)],
	'==': [(2,eq)],
	'!=': [(2,neq)],
	'>=': [(2,ge)],
	'<=': [(2,le)],
	'>': [(2,gt)],
	'<': [(2,lt)],
	'true': [(0,true)],
	'false': [(0,false)],
	'str': [(1,_str)],
	'int': [(1,_int)],
	'float': [(1,_float)],
	'bool': [(1,_bool)],
	'pop': [(1,pop)],
	'if': [(3,_if)],
	'and': [(2,_and)],
	'or': [(2,_or)],
	'not': [(1,_not)],
	'def': [(2,_def)],
	'proc': [(2,proc)],
	':': [(2,cons)],
	'slice': [(4,slice),(3,slice)],
	'range': [(1,_range),(2,_range),(3,_range)],
	'atom': [(1,atom)],
	'arg': [(0,arg),(1,arg)],
	'dup': [(1,dup)],
	'unseq': [(1,unseq)],
	'var': [(2,var)],
	'call': [(-1,call)],
	'try': [(2,_try)],
	'del': [(1,_del)],
	'fail': [(1,fail)],
	'rot': [(1,rot)]
}

while True:
	line = input(">>> ")
	if line == "quit":
		break
	text = line
	while line != "":
		line = input("... ")
		text += line
	stack, stdenv = eval(tokenize(text),stdenv)
	print(stack)
