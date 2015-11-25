#!/usr/bin/env python3

from parser import lex, parse, Atom, String, Number, List
import operator
from importlib import import_module
from runtime.lispimport import import_
import os.path

def evalexpr(expr, state):
	if expr.__class__.__name__ == 'List':
		f, state = evalexpr(expr.value[0], state)
		return f(*(expr.value[1:] + [state]))
	elif expr.__class__.__name__ == 'Number':
		return expr.value, state
	elif expr.__class__.__name__ == 'String':
		return expr.value, state
	elif expr.__class__.__name__ == 'Atom':
		return state[expr.value], state
	else:
		raise TypeError("Can't evaluate expression of type %s." % expr.__class__.__name__)

def strict(f):
	def _strict(*args):
		a = []
		*args, state = args
		for arg in args:
			x, state = evalexpr(arg, state)
			a.append(x)
		return f(*(a + [state]))
	return _strict

def builtin(state, name):
	def _builtin(f):
		state[name] = f
		def _2builtin(*args):
			return f(*args)
		return _2builtin
	return _builtin

def variadicwithstate(f):
	def _variadicwithstate(*args):
		*args, state = args
		return f(args, state)
	return _variadicwithstate

default_state = {}

def topyval(val):
	if val.__class__.__name__ == "List":
		return [topyval(x) for x in val.value]
	else:	
		return val.value

@builtin(default_state, "quote")
def quote(arg, state):
	return topyval(arg), state

@builtin(default_state, "cond")
@variadicwithstate
def cond(args, state):
	for c, v in args:
		x, state = evalexpr(c, state)
		if x:
			return evalexpr(v, state)

@builtin(default_state, "lambda")
def _lambda(a, func, state):
	@strict
	def _wrapper(*args):
		newstate = dict(state)
		for a, n in zip(args, a):
			newstate[n] = a
		return evalexpr(func, newstate)
	return _wrapper

@builtin(default_state, "define")
@strict
def _define(name, value, state):
	return define(name, value, state)

def define(name, value, state):
	if name in state:
		raise RuntimeError("%s has already been defined." % name)
	state[name] = value
	return value, state

@builtin(default_state, "def")
def _def(name, a, func, state):
	@strict
	def _wrapper(*args):
		newstate = dict(state)
		for a, n in zip(args, a):
			newstate[n] = a
		for statement in func:
			val = evalexpr(func, newstate)
		return val
	if name in state:
		raise RuntimeError("%s has already been defined." % name)
	state[name] = _wrapper
	return _wrapper

def loadex(args, state):
	mod = import_module(args[0])
	if len(args) == 2:
		if args[1] == "":
			prefix = ""
		else:
			prefix = args[1] + "."
	else:
		prefix = args[0] + "."
	mod.__loader__.load_module()
	for name in globals().keys():
		setattr(mod, name, globals()[name])
	newstate = mod.register(state.copy())
	for name, value in newstate.items():
		state[prefix + name] = value
	return None, state

@builtin(default_state, "loadex")
@strict
@variadicwithstate
def _loadex(args, state):
	return loadex(args, state)

def wrap(func, name, state):
	@builtin(state, name)
	@strict
	@variadicwithstate
	def _wrap(args, state):
		return func(*args), state
	return _wrap

@builtin(default_state, "getvar")
@strict
def getvar(name, state):
	return state[name], state

@builtin(default_state, "setvar")
@strict
def setvar(name, value, state):
	if name in state:
		state[name] = value
	else:
		raise KeyError(name)
	return None, state

def loadprelude(state):
	prelude_ex = ["runtime.op", "runtime.io", "runtime.lispimport", "runtime.functional"]
	prelude_mod = []
	for ex in prelude_ex:
		_, state = loadex([ex, ""], state)
	for mod in prelude_mod:
		_, state = import_([mod], state)
	return state

def evallisp(source, state):
	ast = parse(lex(source))
	for expr in ast:
		_, state = evalexpr(expr, state)

default_state = loadprelude(default_state)
evallisp('''
''', default_state)
