import sys
from funcparserlib.parser import *
from funcparserlib.lexer import make_tokenizer

token_specs = [
	("NAME", (r"[a-zA-Z_0-9]+",)),
	("EQ", (r"=",)),
	("DASH", (r"-",)),
	("STRING", (r'\"([^\"]*)\"',)),
	("SPACE", (r" ",))
]

tokenize = make_tokenizer(token_specs)

tokval = lambda t: t.value

typ = lambda s: some(lambda t: t.type == s)

name = typ("NAME") >> tokval
eq = typ("EQ") >> tokval
dash = typ("DASH") >> tokval
string = typ("STRING") >> tokval
space = typ("SPACE") >> tokval

class Arg:
	def __init__(self, string, value):
		if value:
			self.name = string[0]
			self.value = string[1]
		else:
			self.name = string
		self.is_value_arg = value

def arg(value):
	def _arg(s):
		return Arg(s, value)
	return _arg

value_normal_arg = skip(dash) + name + skip(space) + (name | string)
value_normal_arg >>= arg(value=True)

value_alternate_arg = skip(dash) + skip(dash) + name + skip(eq) + (name | string)
value_alternate_arg >>= arg(value=True)

checked_normal_arg = skip(dash) + name
checked_normal_arg >>= arg(value=False)

checked_alternate_arg = skip(dash) + skip(dash) + name
checked_alternate_arg >>= arg(value=False)

arg_parser = many((value_normal_arg | value_alternate_arg | checked_normal_arg | checked_alternate_arg) + skip(many(space)))

class NoValueError(Exception): pass
class ValueProvidedError(Exception): pass
class ArgumentNotPresentError(Exception): pass
class NoArgumentError(Exception): pass
class ArgumentAlreadyProvidedError(Exception): pass

class ArgumentParser:
	def __init__(self, help_message=None):
		self.help_message = help_message
		self._optional_normal = {}
		self._required_normal = {}
		self._optional_alternate = {}
		self._required_alternate = {}
		self._action = {}

	def add_arg(self, name, alternate, optional=False, value_arg=True, action=None):
		if optional:
			self._optional_normal[name] = value_arg
			self._optional_alternate[alternate] = name
		else:
			self._required_normal[name] = value_arg
			self._required_alternate[alternate] = name
		self._action[name] = action

	def _parse(self, args):
		source = ' '.join(args[1:])
		tokens = list(tokenize(source))
		args = arg_parser.parse(tokens)
		result = {}
		for arg in args:
			if arg.name in self._optional_alternate:
				arg.name = self._optional_alternate[arg.name]
			if arg.name in self._required_alternate:
				arg.name = self._required_alternate[arg.name]

			if arg.name in self._optional_normal:
				d = self._optional_normal
			elif arg.name in self._required_normal:
				d = self._required_normal
			else:
				raise NoArgumentError(arg.name)

			if arg.name in result:
				raise ArgumentAlreadyProvidedError(arg.name)

			if d[arg.name] and arg.is_value_arg:
				result[arg.name] = arg.value
			elif d[arg.name]:
				raise NoValueError(arg.name)
			elif arg.is_value_arg:
				raise ValueProvidedError(arg.name)
			else:
				result[arg.name] = True

		for name in self._required_normal.keys():
			if name not in result:
				raise ArgumentNotPresentError(name)
		
		for name, value in result.items():
			if self._action[name] is not None:
				result[name] = self._action[name](value)
		return result

	def print_help(self):
		if self.help_message is not None:
			print(self.help_message)
		else:
			print("Usage\n  Required options:\n    %s\n  Optional options:\n    %s\n" % ('\n    '.join(self._required_normal.keys()), 
				'\n    '.join(self._optional_normal.keys())))

	def parse(self, args):
		try:
			return self._parse(args)
		except NoValueError as e:
			print("No value was provided for option %s." % e.args[0])
		except ValueProvidedError as e:
			print("No value should have been provided for switch %s." % e.args[0])
		except ArgumentNotPresentError as e:
			print("The option %s is required." % e.args[0])
		except NoArgumentError as e:
			print("%s is not a valid option." % e.args[0])
		except ArgumentAlreadyProvidedError as e:
			print("The option %s has already been specified." % e.args[0])
		self.print_help()
		sys.exit()



