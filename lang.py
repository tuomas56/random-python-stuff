#!/usr/bin/env python3
import re
from collections import namedtuple, OrderedDict
from functools import wraps, partial
from contextlib import contextmanager
import traceback as tb
import sys
from funcparserlib.parser import *
from operator import attrgetter

##REGION Helpers

@contextmanager
def traceback(depth):
	@wraps(sys.excepthook)
	def _excepthook(type, value, traceback):
		for t in tb.extract_tb(traceback, depth):
			print("File %s, line %s, in %s\n  %s" % t)
		print(value)
	old = sys.excepthook
	sys.excepthook = _excepthook
	yield
	sys.excepthook = _excepthook

##REGION Lexer

token_specs = OrderedDict((
	("string", r"""(?P<string_t>'|")(?P<string_text>(?:(?!(?P=string_t)).)*)(?P=string_t)"""),
	("number", r"""\d+(\.\d+)?"""),
	("lbrace", r"""\{"""),
	("rbrace", r"""\}"""),
	("lsquare", r"""\["""),
	("rsquare", r"""\]"""),
	("lbracket", r"""\("""),
	("rbracket", r"""\)"""),
	("comma", r""","""),
	("keyword", r"""func|if|elif|else|while|for|of|return"""),
	("op", r"""\=\=|\=\+|-|\*|\/|\/\/|~|and|or|not|\&|\||\^|>>|<<|in"""),
	("identifier", r"""[a-zA-Z_\$@!][a-zA-Z0-9_\$@!]*"""),
	("ws", r"""[ \t]+"""),
	("nl", r"""\n+"""),
	("comment", r"""--.*"""),
	("error", r""".""")
))

def get_match_type(match, types):
	for type in types:
		if match.group(type) is not None:
			return type

class Token(namedtuple('Token', 'linenum pos type value file')):
	@staticmethod
	def from_match(line, match, types, file):
		type = get_match_type(match, types)
		if type == "error":
			offset_string = ("\n" if match.string and (match.string[-1] != "\n") else "") + " "*match.span()[0] + "^"
			raise SyntaxError("Unexpected token '%s' in file '%s', line %s.\n%s%s" % (match.group(0), file, line, match.string, offset_string))
		return Token(linenum=line, pos=match.span(), type=type, value=match.group(0), file=file)

def readlines(file):
	curline = b'' if 'b' in file.mode else ''
	while True:
		x = file.read(1)
		curline += x
		if x == '\n':
			yield curline
			curline = b'' if 'b' in file.mode else ''
		elif x == '':
			break

def make_tokenizer(specs):
	types = specs.keys()
	regex = ("(?P<%s>%s)" % (name, regex) for name, regex in specs.items())
	regex = re.compile('|'.join(regex))
	def _make_tokenizer(lineno, string, file):
		for match in iter(regex.scanner(string).match, None):
			yield Token.from_match(lineno, match, types, file)
	return _make_tokenizer

tokenize_line = make_tokenizer(token_specs)

def tokenize_file(filename):
	with open(filename, "r") as file:
		for i, line in enumerate(readlines(file), start=1):
			yield from tokenize_line(i, line, filename)

##REGION Parser

class ASTNode: pass

class Literal(ASTNode):
	def __str__(self):
		return "%s(value=%s)" % (type(self).__name__, self.value)

class StringLiteral(Literal): 
	def __init__(self, value):
		self.value = value.value[1:-1]

class NumberLiteral(Literal):
	def __init__(self, value):
		try:
			self.value = int(value.value)
		except:
			self.value = float(value.value)

class ListLiteral(Literal): pass

class Identifier(ASTNode, namedtuple('Identifier', 'name')): pass

class Call(ASTNode, namedtuple('Call', 'func args')): pass

class BinOp(ASTNode, namedtuple('BinOp', 'lhs op rhs')): pass

class Func(ASTNode, namedtuple('Func', 'name args body')): pass

class IfNode(ASTNode, namedtuple('IfNode', 'pred body elifs elsebody')): pass

class WhileNode(ASTNode, namedtuple('While', 'pred body')): pass

class ForNode(ASTNode, namedtuple('For', 'name iter body')): pass

tok_of_type = lambda t: some(lambda x: x.type == t)
tok_of_value = lambda v: some(lambda x: x.value == v)

expr = forward_decl()

string_literal = tok_of_type('string') >> StringLiteral

number_literal = tok_of_type('number') >> NumberLiteral

list_literal = skip(tok_of_type('lsquare')) + many(expr + skip(tok_of_type('comma'))) + maybe(expr) + skip(tok_of_type('rsquare')) 
list_literal >>= lambda x: x[0] + ([x[1]] if x[1] else [])
list_literal >>= ListLiteral

literal = string_literal | number_literal | list_literal

identifier = tok_of_type('identifier') >> attrgetter('value') >> Identifier

call = expr + skip(tok_of_type('lbracket')) + many(expr + skip(tok_of_type('comma'))) + maybe(expr) + skip(tok_of_type('rbracket'))
call >>= lambda x: (x[0], x[1] + ([x[2]] if x[2] else []))
call >>= Call

expr.define(literal | identifier | call)

toplevel = expr + skip(finished)

print(toplevel.parse(list(tokenize_line(1, '', '<module>'))))