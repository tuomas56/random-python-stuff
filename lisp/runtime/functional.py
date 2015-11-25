import functools
import itertools
import operator

def register(default_state):
	_map = wrap(map, "map", default_state)
	_filter = wrap(filter, "filter", default_state)
	_dict = wrap(dict, "dict", default_state)
	_zip = wrap(zip, "zip", default_state)
	_enumerate = wrap(enumerate, "enumerate", default_state)
	_chain = wrap(itertools.chain, "chain", default_state)
	_sum = wrap(sum, "sum", default_state)

	@builtin(default_state, "split")
	@strict
	def split(string, sep, state):
		return sep.split(string), state

	@builtin(default_state, "join")
	@strict
	def join(sep, string, state):
		return sep.join(string), state

	return default_state