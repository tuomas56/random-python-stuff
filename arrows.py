def tokenize(source):
	return source.replace('(',' ( ').replace(')',' ) ').split()

def atom(token):
	try:
		return int(token)
	except:
		try:
			return float(token)
		except:
			return token

def parse(source):
	print(source,flush=True)
	ast = []
	def eat(n=1):
		nonlocal source
		x, source = source[:n],source[n:]
		return x
	def peek():
		nonlocal source
		return source[0]
	while len(source):
		if peek() == "(":
			ep = 0
			l = []
			while ep > 0:
				print(ep,flush=True)
				token = eat()
				print(token,flush=True)
				if token == "(":
					ep += 1
				elif token == ")":
					ep -= 1
				l.append(token)
			ast.append(parse(l))
		else:
			ast.append(atom(eat()[0]))
	return ast


def std_environment(environment):
	def printl(env,*args):
		results = []
		for arg in args:
			result, env = evale(arg,env)
			results.append(result)
		print(*results)
	def evall(env,exp):
		nonlocal environment
		result,environment = evale(exp,environment)
		return result
	std_e = {
		'print': printl,
		'true': lambda env: True,
		'false': lambda env: False,
		'none': lambda env: None,
		'eval': evall
	}
	return std_e

def evale(exp,env):
	result = None
	print(exp)
	if isinstance(exp,list):
		if exp[0] == 'if':
			result, env = evale(exp[2] if bool(evale(exp[1])) else exp[3])
		elif exp[0] == 'quote':
			result = exp[1]
		elif exp[0] == 'define':
			result,env = evale(exp[2],env)
			env[exp[1]] = result
		else:
			result = env[exp[0]](env,*exp[1:])
	else:
		result = env[exp]
	return result, env



def execute(code):
	results = []
	env = std_environment({})
	exps = tokenize(code)
	print(exps)
	exps = parse(['(','print','(','hello',')',')'])
	print(exps)


execute("(define x (quote hello))")