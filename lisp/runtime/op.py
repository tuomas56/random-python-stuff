import operator

def register(default_state):
	def op2(func, name):
		@strict
		def _op2(x, y, state):
			return func(x, y), state
		default_state[name] = _op2
		return _op2

	def op1(func, name):
		@strict
		def _op1(x, state):
			return func(x), state
		default_state[name] = _op1
		return _op1

	op2(operator.add, "+")
	op2(operator.sub, "-")
	op2(operator.mul, "*")
	op2(operator.truediv, "/")
	op2(operator.floordiv, "//")
	op1(operator.not_, 'not')
	op2(operator.or_, '|')
	op2(operator.and_, '&')
	op2(operator.xor, '^')
	op2(operator.pow, '**')
	op2(operator.rshift, '>>')
	op2(operator.lshift, '<<')
	op2(operator.mod, '%')


	return default_state
