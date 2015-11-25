class Infix:
	def __init__(self,function):
		self.function = function

	def __ror__(self,other):
		return Infix(lambda x, self=self, other=other: self.function(other,x))

	def __or__(self,other):
		return self.function(other)

	def __rlshift__(self,other):
		return Infix(lambda x, self=self, other=other: self.function(other,x))

	def __rshift__(self,other):
		return self.function(other)

	def __call__(self,value1,value2):
		return self.function(value1,value2)


class Ordering:
	def __init__(self, r):
		self.r = r

	def __str__(self):
		return "Ordering::%s" % self.r

	def __repr__(self):
		return str(self)

Ordering.GREATER = Ordering("GREATER")
Ordering.EQUAL = Ordering("EQUAL")
Ordering.LESS = Ordering("LESS")

@Infix
def cmp(x, y):
	if x > y:
		return Ordering.GREATER
	elif x == y:
		return Ordering.EQUAL
	else:
		return Ordering.LESS

@Infix
def has(x,attr):
	return hasattr(x,attr)

@Infix
def is_instance(obj,clas):
	return isinstance(obj, clas)