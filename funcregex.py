from funcparserlib.parser import *
import funcparserlib.parser
import string
from collections import namedtuple
from functools import reduce
import operator

__all__ = ['match', 'compile']

string.alphanumeric = string.digits + string.ascii_letters

@funcparserlib.parser.Parser
def started(tokens, s):
    """Parser(a, None)

    Throws an exception if any tokens have been parsed.
    """
    if s.pos <= 0:
        return None, s
    else:
        raise NoParseError('should not have parsed any tokens.', s)

class RegexElem: 
	def transform(self): pass

class Char(namedtuple('Char', 'value'), RegexElem):
	def transform(self):
		return a(self.value)

class Sequence(namedtuple('Sequence', 'type'), RegexElem):
	def transform(self):
		if self.type == "A":
			return skip(started)
		elif self.type == "b":
			pass
		elif self.type == "B":
			pass
		elif self.type == "d":
			return some(lambda x: x in string.digits)
		elif self.type == "D":
			return some(lambda x: x not in string.digits)
		elif self.type == "s":
			return some(lambda x: x in ' \t\n\r')
		elif self.type == "S":
			return some(lambda x: x not in ' \t\n\r')
		elif self.type == "w":
			return some(lambda x: x in string.alphanumeric)
		elif self.type == "W":
			return some(lambda x: x not in string.alphanumeric)
		elif self.type == "Z":
			return skip(finished)
		elif self.type == "g":
			pass

class Group(namedtuple('Group', 'body'), RegexElem):
	def transform(self):
		return reduce(operator.add, map(operator.methodcaller('transform'), self.body)) >> Group

class Alternate(namedtuple('Alternate', 'options'), RegexElem):
	def transform(self):
		return reduce(operator.or_, map(operator.methodcaller('transform'), self.options))

class Special(namedtuple('Special', 'type'), RegexElem):
	def transform(self):
		if self.type == ".":
			return some(lambda x: True)
		elif self.type == "$":
			return skip(finished)
		elif self.type == "^":
			return skip(started)

class CharRange(namedtuple('CharRange', 'start end'), RegexElem):
	def transform(self):
		char_set = None
		for x in (string.ascii_lowercase, string.ascii_uppercase, string.digits):
			if self.start in x and self.end in x:
				char_set = x
		if char_set is None:
			raise SyntaxError("Invalid range: %s-%s" % self)
		return some(lambda x: x in char_set[char_set.index(self.start):char_set.index(self.end)+1])

class CharClass(Alternate): pass

class Quantifier(namedtuple('Quantifier', 'expr quantity'), RegexElem):
	def transform(self):
		if self.quantity.min is None and self.quantity.max is None:
			return many(self.expr.transform())
		elif self.quantity.min is None:
			return reduce(operator.add, [maybe(self.expr.transform())]*self.quantity.max)
		elif self.quantity.max is None:
			return reduce(operator.add, [self.expr.transform()]*self.quantity.min) + many(self.expr.transform()) >> (lambda x: [x[0]] + x[1])
		elif self.quantity.min == self.quantity.max:
			return reduce(operator.add, [self.expr.transform()]*self.quantity.min)
		else:
			return reduce(operator.add, [self.expr.transform()]*self.quantity.min) + reduce(operator.add, 
				[maybe(self.expr.transform())]*(self.quantity.max - self.quantity.min)) >> (lambda x: x[:self.quantity.min] + x[self.quantity.min])

class QuantityRange(namedtuple('QuantityRange', 'min max')): pass

star = lambda func: lambda x: func(*x)

def make_quantifier(args):
	if args[1] is not None:
		return Quantifier(args[0], args[1])
	else:
		return args[0]



toplevel = forward_decl()
specials = "[]()|.^$\\*+?{},"
letter = some(lambda x: x in string.ascii_letters)
digit = some(lambda x: x in string.digits)
ws = some(lambda x: x in string.whitespace)
char = letter | digit | ws | some(lambda x: x in ''.join(filter(lambda x: x not in specials, string.punctuation)))
char >>= Char

expression = forward_decl()

char_range = ((letter + skip(a("-")) + letter) | (digit + skip(a("-")) + digit)) >> star(CharRange)

char_class = skip(a("[")) + many(char_range | char) + skip(a("]")) >> CharClass

group = skip(a("(")) + toplevel + skip(a(")")) >> Group

string_start = a("A")
word_boundary = a("b")
not_word_boundary = a("B")
digit_seq = a("d")
not_digit_seq = a("D")
whitespace = a("s")
not_whitespace = a("S")
alphanumeric = a("w")
not_alphanumeric = a("W")
string_end = a("Z")
prev_group = a("g") + skip(a("<")) + many(digit) + skip(a(">"))

sequence = skip(a("\\")) + (string_start | word_boundary | not_word_boundary |
					  digit_seq | not_digit_seq | whitespace | not_whitespace | 
					  alphanumeric | not_alphanumeric | string_end | prev_group) >> Sequence

escape = skip(a("\\")) + some(lambda x: x in specials) >> Char

dot = a(".") >> Special
start = a("^") >> Special
end = a("$") >> Special

special = dot | start | end

zero_plus = skip(a("*")) >> (lambda _: QuantityRange(None,None))
one_plus = skip(a("+")) >> (lambda _: QuantityRange(1, None))
optional = skip(a("?")) >> (lambda _: QuantityRange(None, 1))
exactly_n = skip(a("{")) + many(digit) + skip(a("}")) >> (lambda x: int(''.join(x))) >> (lambda x: QuantityRange(x, x))
from_n_to_m = skip(a("{")) + maybe(many(digit)) + skip(a(",")) + maybe(many(digit)) + skip(a("}")) >> (lambda x: list(map(lambda y: int(''.join(y)), x))) >> star(QuantityRange)

quantifier = zero_plus | one_plus | optional | exactly_n | from_n_to_m

expression.define((char_class | char | sequence | escape | special | group) + maybe(quantifier) >> make_quantifier)

alternate = many(expression) + skip(a("|")) + toplevel >> Alternate

toplevel.define(alternate | many(expression))

parse = (toplevel + skip(finished)).parse

def flatten(ls, g):
	result = []
	for e in ls:
		if not isinstance(e, (list, tuple)):
			result.append(e)
		elif isinstance(e, Group):
			g.append(e)
			x = flatten(e.body, g)
			result += x[0]
			g = x[1]
		else:
			x = flatten(e, g)
			result, g = result + x[0], x[1]
	return result, g

class Match:
	def __init__(self, body, groups):
		self._groups = groups
		self._body = body

	def group(self, id):
		if id == 0:
			return self._body
		else:
			return self._groups[id - 1]

class Pattern:
	def __init__(self, p):
		self._p = p

	def match(self, string):
		return _match(self._p, string)

def compile(pattern):
	return Pattern(_compile(pattern))

def _compile(pattern):
	pattern = parse(pattern)
	pattern = reduce(operator.add, map(operator.methodcaller('transform'), pattern)) + skip(finished)
	return pattern

def match(pattern, string):
	pattern = _compile(pattern)
	return _match(pattern, string)

def _match(pattern, string):
	result = pattern.parse(string)
	result = flatten(result, [])
	return Match(*result)

def do_tests():
	TESTS = {
		"[ab]*": ("", "a", "aa", "aaa", "ab", "abb", "aba", "b", "bb", "bbb"),
		"[0-9]*\.[0-9]*": (".", "1.", ".1", "1.0", "1.2", "1.45", "65.2")
	}
	wins, losses = 0, 0
	for pattern, strings in TESTS.items():
		pattern = compile(pattern)
		for string in strings:
			try:
				pattern.match(string)
			except:
				losses += 1
			else:
				wins += 1
	return wins, losses

if __name__ == "__main__":
	print("%s, %s" % do_tests())