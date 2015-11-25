from collections import namedtuple

Context = namedtuple('Context', 'globals locals')

def newcontext():
	g = {}
	l = {}
	exec('', g, l)
	g.update(g.get('__builtins__'))
	return Context(globals=g, locals=l)

def wrapifcallable(func):
	if callable(func):
		@strict
		@variadicwithstate
		def _func(args, state):
			return wrapifcallable(func(*args)), state
		return _func
	else:
		return func

def get(name, context):
	name = name.split(".")
	try:
		t = context.locals
		for part in name:
			try:
				t = t[part]
			except TypeError:
				t = getattr(t, part)
	except:
		t = context.globals
		for part in name:
			try:
				t = t[part]
			except TypeError:
				t = getattr(t, part)
	return wrapifcallable(t)

def set_(*args):
	if len(args) == 4:
		name, value, is_global, context = args
	else:
		name, value, context = args
		is_global = False
	if is_global:
		context.globals[name] = value
	else:
		context.locals[name] = value
	return context

def eval_(source, context):
	exec(source, context.globals, context.locals)
	return context

def import_(name, context):
	mod = __import__(name)
	context.globals[name] = mod
	return context

def register(default_state):
	_newcontext = wrap(newcontext, "newcontext", default_state)
	_get = wrap(get, "get", default_state)
	_eval_ = wrap(eval_, "eval", default_state)
	_import_ = wrap(import_, "import", default_state)

	@builtin(default_state, "set")
	@strict
	@variadicwithstate
	def _set(args, state):
		return set_(*args), state

	return default_state
