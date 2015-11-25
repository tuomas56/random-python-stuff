import math

def register(state):
	for name in dir(math):
		if not name.startswith("__"):
			wrap(getattr(math, name), "math.%s" % name, state)
	return state