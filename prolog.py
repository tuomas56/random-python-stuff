
class PObject:
	def unify(self,other):
		return False

	def backtrack(self,other):
		pass

	def __str__(self):
		return ""

class PVariable(PObject):
	def __init__(self,name):
		self.name = name
		self._bind(None)
		self._uvar = 0

	def _getNextUVar(self):
		self._uvar += 1
		return PVariable('_'+str(self._uvar))

	def unify(self,other):
		if isinstance(other,PVariable) and not self.isBound() and not other.isBound():
			var = self._getNextUVar()
			self._bind(var)
			other._bind(var)
			return True
		elif isinstance(other,PVariable) and not other.isBound():
			self._bind(other.getValue())
			return True
		elif isinstance(other,PVariable):
			return False
		elif not self.isBound():
			self._bind(other)
			return True
		else:
			return self.getValue().unify(other)

	def backtrack(self,other):
		self._bind(None)
		if isinstance(other,PVariable):
			other._bind(None)

	def _bind(self,value):
		global env
		env._bind(self.name,value)
		self._value = value

	def getValue(self):
		return self._value

	def isBound(self):
		return self.getValue() != None

	def __str__(self):
		return self.name + ("="+str(self.getValue()) if self.isBound() else "")

class PAtom(PObject):
	def __init__(self,value):
		self.value = value

	def unify(self,other):
		if isinstance(other,PVariable):
			other._bind(self)
			return True
		elif isinstance(other,PAtom):
			return other.value == self.value
		else:
			return False

	def backtrack(self,other):
		if isinstance(other,PVariable):
			other._bind(None)

	def __str__(self):
		return self.value

class PFunctor(PObject):
	def __init__(self,name,args):
		self.name = name
		self.args = args

	def unify(self,other):
		if isinstance(other,PVariable) and not other.isBound():
			other._bind(self)
			return True
		elif isinstance(other,PVariable):
			return other.getValue().unify(self)
		elif isinstance(other,PFunctor):
			nameseq = self.name == other.name
			arityeq = len(self.args) == len(other.args)
			argsCompat = all([arg1.unify(arg2) for arg1,arg2 in zip(self.args,other.args)])
			return nameseq and arityeq and argsCompat
		else:
			return False

	def backtrack(self,other):
		if isinstance(other,PVariable) and other.isBound() and other.getValue() == self:
			other._bind(None)
		elif isinstance(other,PFunctor):
			for arg1,arg2 in zip(self.args,other.args):
				arg1.backtrack(arg2)

	def __str__(self):
		return self.name + "(" + ','.join(map(str,self.args)) + ")"

class PClause:
	def __init__(self,a,b,op):
		self.a = a
		self.b = b
		self.op = op

	def __str__(self):
		return str(self.a) + ("," if self.op == "and" else ";") + str(self.b)

class PStatement:
	pass

class PFact(PStatement):
	def __init__(self,thing):
		self.value = thing

	def __str__(self):
		return str(self.value) + "."

class PRule(PStatement):
	def __init__(self,head,body):
		self.head = head
		self.body = body

	def __str__(self):
		return str(self.head) + " :- " + str(self.body) + "."

class PEnvironment:
	def __init__(self,facts,rules):
		self.facts = facts
		self.rules = rules
		self.varvals = {}

	def prove(self,thing):
		if isinstance(thing,PClause):
			if thing.op == "or":
				return self.prove(thing.a) or self.prove(thing.b)
			elif thing.op == "and":
				return self.prove(thing.a) and self.prove(thing.b)

		for fact in self.facts:
			if thing.unify(fact.value):
				return True

		for rule in self.rules:
			if thing.unify(rule.head):
				if self.prove(rule.body):
					return True
				else:
					thing.backtrack(rule.head)

		raise StopIteration

	def _bind(self,name,value):
		if name not in self.varvals:
			self.varvals[name] = set()
		if value != None:
			self.varvals[name].add(value)

	def _value(self,name):
		return self.varvals[name]

	def __str__(self):
		return '\n'.join(map(str,self.facts))+'\n'+'\n'.join(map(str,self.rules))

class PQuery:
	def __init__(self,env,goal):
		self.env = env
		self.goal = goal

	def prove(self):
		return self.env.prove(self.goal)

	def variables(self):
		if isinstance(self.goal,PAtom):
			return []
		elif isinstance(self.goal,PVariable):
			return [self.goal]
		elif isinstance(self.goal,PFunctor):
			return list(filter(lambda x: isinstance(x,PVariable),self.goal.args))

	def __str__(self):
		return "?- "+str(self.goal)+"."

env = PEnvironment([],[])

p = PFunctor('happy',[PVariable('X')])
q = PFunctor('isalive',[PVariable('X')])
r = PFunctor('notdead',[PVariable('X')])

fp = PFact(PFunctor('isalive',[PAtom('me')]))
fr = PFact(PFunctor('notdead',[PAtom('me')]))
rq = PRule(p,PClause(q,r,"and"))

env.rules = [rq]
env.facts = [fp,fr]

query = PQuery(env,PFunctor('happy',[PVariable('X')]))

print("?- listing.")
print('    ','\n     '.join(str(env).split("\n")),'\n')
print(query)
if query.prove():
	for var in query.variables():
		for val in query.env._value(var.name):
			print("   ",var.name,"=",val)
	print("    yes.")
else:
	print("    no.")


		