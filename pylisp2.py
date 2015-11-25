#!/usr/bin/env python3

from funcparserlib.parser import *
from funcparserlib.lexer import make_tokenizer
import operator

TOKEN_SPECS = [
	("LB", (r'\(',)),
	("RB", (r'\)',)),
	("WS", (r'\s+',)),
	("STRING", (r'"[^"]*"',)),
	("ATOM", (r'[a-zA-Z_][a-zA-Z0-9_]*',)),
	("NUMBER", (r'[0-9]*\.?[0-9]*',)),
]

lex = lambda x: list(make_tokenizer(TOKEN_SPECS)(x))

class ASTNode:
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return "%s(%s)" % (self.__class__.__name__, str(self.value))

class Number(ASTNode):
	def __init__(self, value):
		self.value = float(value)

class String(ASTNode):
	def __init__(self, value):
		self.value = value[1:-1]

class Atom(ASTNode): pass

class List(ASTNode): pass

ttype = lambda s: some(lambda t: t.type == s)
tokval = lambda t: t.value

ws = skip(maybe(ttype("WS")))

lb = ws + ttype("LB") + ws
rb = ws + ttype("RB") + ws
number = ws + ttype("NUMBER") + ws >> tokval >> Number
string = ws + ttype("STRING") + ws >> tokval >> String
atom = ws + ttype("ATOM") + ws >> tokval >> Atom

literal = number | string

llist = forward_decl()
llist.define(ws + skip(lb) + many(literal | atom | llist) + skip(rb) + ws >> List)

parse = (ws + many(llist | atom | literal) + ws + skip(finished)).parse

def evalexpr(expr, state):
	if isinstance(expr, List):
		f, state = evalexpr(expr.value[0], state)
		return f(*(expr.value[1:] + [state]))
	elif isinstance(expr, Number):
		return expr.value, state
	elif isinstance(expr, String):
		return expr.value, state
	elif isinstance(expr, Atom):
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

class LispRuntimeError(Exception): pass

default_state = {}

@builtin(default_state, "quote")
def quote(arg, state):
	return arg, state

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
def define(name, value, state):
	if name in state:

	state[name] = value
	return value, state

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

@builtin(default_state, "input")
@strict
def _input(prompt, state):
	return input(prompt), state


def op(func, name, state):
	@builtin(state, name)
	@strict
	def _op(x, y, state):
		return func(x, y), state
	return _op

op(operator.add, "+", default_state)
op(operator.sub, "-", default_state)
op(operator.mul, "*", default_state)
op(operator.truediv, "/", default_state)
op(operator.floordiv, "//", default_state)
def evallisp(source, state):
	ast = parse(lex(source))
	for expr in ast:
		_, state = evalexpr(expr, state)

evallisp('(define "x" 10) (print x)', default_state)

	
