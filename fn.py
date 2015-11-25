from functools import partial,wraps
from inspect import getfullargspec
import operator

class ComposableFunction:
	def __init__(self,func):
		self.func = func

	def __rshift__(self,other): #function piping
		if not isinstance(other,ComposableFunction):
			other = composable(other)
		return composable(lambda *args: other(self(*args)))

	def __ge__(self,other): #function piping
		if not isinstance(other,ComposableFunction):
			other = composable(other)
		return lambda *args: [other(x) for x in self(*args)]


	def __call__(self,*args):
		return self.func(*args)


def composable(func):
	return ComposableFunction(func)

composable = composable(composable)

def arityof(func):
	return len(getfullargspec(func)[0])

def curry2(func):
	def fx(x):
		def fy(y):
			return func(x,y)
		return composable(fy)
	return composable(fx)

def curry3(func):
	def fx(x):
		def fy(y):
			def fz(z):
				return func(x,y,z)
			return composable(fz)
		return composable(fy)
	return composable(fx)

def test_functions():

	curry2composable = composable >> curry2
	curry3composable = composable >> curry3

	global map
	map = curry2composable(map)

	global filter
	filter = curry2composable(filter)

	lt = curry2composable(operator.lt)
	gt = curry2composable(operator.gt)
	le = curry2composable(operator.le)
	ge = curry2composable(operator.ge)
	eq = curry2composable(operator.eq)
	ne = curry2composable(operator.ne)

	add = curry2composable(operator.add)
	sub = curry2composable(operator.sub)
	mul = curry2composable(operator.mul)
	div = curry2composable(operator.truediv)
	floordiv = curry2composable(operator.floordiv)
	mod = curry2composable(operator.mod)
	pow = curry2composable(operator.pow)
	neg = composable(operator.neg)

	(map(add(3)) >> filter(mod(2) >> eq(0)) >> list >> print)([1,2,3,4])

if __name__ == "__main__":
	test_functions()
