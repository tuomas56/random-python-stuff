def register(default_state):
	@builtin(default_state, "print")
	@strict
	@variadicwithstate
	def _print(args, state):
		a = []
		for arg in args:
			if isinstance(arg, Atom):
				a.append(arg.value)
			else:
				a.append(arg)
		print(*a)
		return None, state

	_input = wrap(input, "input", default_state)

	@builtin(default_state, "open")
	@strict
	def _open(filename, mode, state):
		return open(filename, mode), state

	@builtin(default_state, "read")
	@strict
	def read(file, length, state):
		if length <= 0:
			return file.read(), state
		else:
			return file.read(length), state

	@builtin(default_state, "write")
	@strict
	def write(file, text, state):
		return file.write(text), state
		
	return default_state