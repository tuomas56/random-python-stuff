def import_(name, rel, state):
	path = os.path.join(*name.split(".")) + ".lisp"
	prefix = (rel if rel else name) + '.'
	newstate = state.copy()
	with open(path, "r") as f:
		evallisp(f.read(), newstate)
	newstate = dict(map(lambda x: (x, newstate[x]), set(newstate) ^ set(state)))
	for k, v in newstate.items():
		state[prefix + k] = v
	return None, state

def register(default_state):
	@builtin(default_state, "import")
	@strict
	@variadicwithstate
	def _import_(args, state):
		name = args[0]
		if len(args) == 2:
			rel = args[1]
		else:
			rel = ""
		return import_(name, rel, state)

	return default_state