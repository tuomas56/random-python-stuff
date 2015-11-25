class Statement:
	def implies(self,other):
		return False

class Expression:
	def is_true(self,env):
		return False

	def value(self):
		return None

class Unifiable:
	def unify(self,other):
		return False, lambda: (self, other)

class Constant(Expression, Unifiable):
	def __init__(self,value):
		self._value = value

	def value():
		return self._value

	def is_true(self,env):
		return True

	def unify(self,other):
		if isinstance(other,Variable):
			return other.unify(self)
		else:
 			return False, lambda: (self,other)

class Functor(Expression, Unifiable):
	def __init__(self,name,args):
		self._name = name
		self._args = args

	def value():
		return self

	def is_true(self,env):
		pass

	def unify(self,other):
		pass


class Variable(Expression, Unifiable):
	def __init__(self,name):
		self._name = name
		self._bound = False
		self._value = None

	def is_true(self,env):
		if self._bound:
			return self._value.is_true(env)
		else:
			return True

	def bound(self):
		return self._bound

	def value(self):
		return self._value

	def bind(self,value):
		self._value = value

	def unbind(self):
		self._bound = False

	def __str__(self):
		if self.bound():
			return self.name + " = " + self.value()
		else:
			return self.name

	def unify(self,other):
		if isinstance(other, Variable):
			if other.bound() and self.bound():
				return other.value() == self.value(), lambda: (self, other)
			elif other.bound():
				value = self.value()
				self.bind(other.value())
				def backtrack():
					self.bind(value)
					return (self, other)
				return True, backtrack
			elif self.bound():
				value = other.value()
				other.bind(self.value())
				def backtrack():
					other.bind(value)
					return (self, other)
				return True, backtrack
			else:
				var = Variable('_')
				var.bind(None)
				result1, backtrack1 = self.unify(var)
				result2, backtrack2 = other.unify(var)
				def backtrack():
					self,_ = backtrack1()
					other,_ = backtrack2()
					return (self,other)
				return (result1 and result2), backtrack
		elif isinstance(other,Constant):
			if not self.bound():
				value = self.value()
				self.bind(other.value())
				def backtrack():
					self.bind(value)
					return self,other
				return True,backtrack
			else:
				return self.value() == other.value(), lambda: (self,other)







