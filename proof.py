import itertools

class PrologTerm:
	def unifies(self,other):
		pass

	def __eq__(self,other):
		return self.unifies(other)

	def isTrue(self):
		return False

	def substitute(self,vars):
		return self

class Constant(PrologTerm):
	def __init__(self,value):
		self.value = value

	def unifies(self,other):
		if isinstance(other,Constant):
			return self.value == other.value
		elif isinstance(other,Variable):
			return True
		else:
			return False

	def isTrue(self,env):
		return False

	def __str__(self):
		return self.value

	def subsitute(self,vars):
		return self

class Fact(PrologTerm):
	def __init__(self,term):
		self.term = term

	def unifies(self,other):
		if isinstance(other,Fact):
			return self.term == other.term
		elif isinstance(other,Variable):
			return True
		else:
			return False

	def isTrue(self,env):
		return self in env.facts or self.term.isTrue(env) or any([rule.implies(self,env) for rule in env.rules])

	def __str__(self):
		return "Fact(" + str(self.term) + ")"

	def substitute(self,vars):
		return self.term.substitute(vars)

class Variable(PrologTerm):
	def __init__(self,name):
		self.name = name

	def unifies(self,other):
		return True

	def __str__(self):
		return self.name

	def substitute(self,vars):
		if any([x[0] == self.name for x in vars]):
			return vars[list(map(lambda x: x[0],vars)).index(self.name)][1]

class LogicalStatment(PrologTerm):
	def __init__(self,first,second,op):
		self.op = op
		self.first = first
		self.second = second

	def isTrue(self,env):
		if self.op == "or":
			return self.first.isTrue(env) or self.second.isTrue(env)
		elif self.op == "and":
			return self.first.isTrue(env) and self.second.isTrue(env)
		else:
			raise Exception("Unsupported operation: "+self.op)

	def __str__(self):
		return str(self.first) + (";" if self.op == "or" else ",") + str(self.second)

	def substitute(self,vars):
		return LogicalStatment(Fact(self.first.substitute(vars)),Fact(self.second.substitute(vars)),self.op)

class Functor(PrologTerm):
	def __init__(self,name,args):
		self.name = name
		self.args = args

	def unifies(self,other):
		if isinstance(other,Variable):
			return True
		elif isinstance(other,Functor):
			return self.name == other.name and all([arg1 == arg2 for arg1,arg2 in zip(self.args,other.args)])
		else:
			return False

	def _gpi(self,env,names=False):
		def interpolate(self,varvals,names):
			argslist = []
			curargs = []
			for perm in itertools.permutations(varvals,len(self.args)):
				curindex = 0
				for arg in self.args:
					if isinstance(arg,Variable) and arg.name not in curargs:
						curargs.append((arg.name,perm[curindex]) if names else perm[curindex])
						curindex += 1
					else:
						curargs.append((arg,arg) if names else arg)
				argslist.append(curargs)
				curargs = []
			return argslist
		argcombos = interpolate(self,env.constants,names)
		return [Functor(self.name,combo) for combo in argcombos]

	def isTrue(self,env):
		return Fact(self) in env.facts or any([ any([rule.implies(this,env) for rule in env.rules]) for this in self._gpi(env)])

	def getSuccessArgs(self,env,names):
		for func in self._gpi(env,names):
			func2 = Functor(func.name,map(lambda x: x[1],func.args))
			if any([rule.implies(Fact(func2),env) or (Fact(func2) in env.facts) for rule in env.rules]):
				yield func

	def __str__(self):
		return self.name + "(" + ','.join(map(str,self.args)) + ")"

	def substitute(self,vars):
		return Functor(self.name,[arg.substitute(vars) for arg in self.args])

class Rule:
	def __init__(self,first,cond):
		self.first = first
		self.cond = cond

	def implies(self,term,env):
		if term == self.first and self.cond.isTrue(env):
			return True
		else:
			return False

	def allCombos(self,env):
		if isinstance(self.first,Functor):
			return [Rule(Functor(func.name,list(map(lambda x: x[1],func.args))), self.cond.substitute(func.args)) for func in self.first._gpi(env,names=True)]
		else:
			return [self]

	def __str__(self):
		return str(self.first) + " :- " + str(self.cond)

class KnowledgeBase:
	def __init__(self,facts=[],rules=[],constants=[]):
		self.facts = facts
		self.rules = rules
		self.constants = constants

a = Constant("A")
b = Constant("B")
c = Constant("C")

A = Fact(a)
B = Fact(b)
C = Fact(c)

env = KnowledgeBase([A,B,C],[],[a,b,c])

r = list(map(lambda x: Rule(Fact(x.first),x.cond),Rule(Functor("and",[Variable("X"),Variable("Y")]),LogicalStatment(Variable("X"),Variable("Y"),"and")).allCombos(env)))

env.rules += r

def query(query,env):
	print("?-",str(query)+":")
	if isinstance(query,Functor):
		for func in query.getSuccessArgs(env,names=True):
			print('\n'.join([" "*3+name+" = "+str(value)+"," for name,value in func.args])[:-1] + ";\n")
	else:
		print(query.isTrue(env))

query(Functor("and",[Variable("X"),Variable("Y")]),env)
