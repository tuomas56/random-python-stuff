import re
from functools import partial

def lex(source):
	for match in re.findall(r"[a-z_]+|[0-9]+(?:\.[0-9]+)?|[\$\^\&\%\@\!\(\)\*\:\;\`\~\>\<\.\,\/\\\?\[\]\{\}\#]|(?:\".*?\")",source):
		try:
			yield float(match)
		except:
			yield match

def execute(tokens, env, cur_frame=[], stack=[]):
	tokens = list(tokens)
	for token in tokens:
		if token == '!':
			(func, is_monadic), *cur_frame = cur_frame
			if is_monadic:
				arg, *cur_frame = cur_frame
				x = func(arg, cur_frame, stack, env)
				cur_frame, stack, env = x
			else:
				cur_frame, stack, env = func(cur_frame, stack, env)
		elif isinstance(token, float) or '"' in token:
			cur_frame.insert(0, token)
		else:
			cur_frame.insert(0, env[token])
	return cur_frame, stack, env

def multiply(arg, cur_frame, stack, env):
	return ([(lambda a, cur_frame, stack, env: ([arg * a] + cur_frame, stack, env), True)] + cur_frame), stack, env

def divide(arg, cur_frame, stack, env):
	return ([(lambda a, cur_frame, stack, env: ([arg / a] + cur_frame, stack, env), True)] + cur_frame), stack, env

def add(arg, cur_frame, stack, env):
	return ([(lambda a, cur_frame, stack, env: ([arg + a] + cur_frame, stack, env), True)] + cur_frame), stack, env

def subtract(arg, cur_frame, stack, env):
	return ([(lambda a, cur_frame, stack, env: ([arg - a] + cur_frame, stack, env), True)] + cur_frame), stack, env

def map_(pred, cur_frame, stack, env):
	def wrapper(ls, cur_frame, stack, env):
		result = []
		for el in ls:
			cur_frame, stack, env = pred[0](el, cur_frame, stack, env)
			result.append(cur_frame[0])
			_, *cur_frame = cur_frame
		return [result] + cur_frame, stack, env
	return [(wrapper, True)] + cur_frame, stack, env

def eq(a, cur_frame, stack, env):
	def wrapper(b, cur_frame, stack, env):
		return [a == b] + cur_frame, stack, env
	return [(wrapper, True)] + cur_frame, stack, env

def index(a, cur_frame, stack, env):
	def wrapper(b, cur_frame, stack, env):
		return [b[int(a)]] + cur_frame, stack, env
	return [(wrapper, True)] + cur_frame, stack, env

def raise_(a, cur_frame, stack, env):
	return [cur_frame[int(a)]] + cur_frame[:int(a)] + cur_frame[int(a)+1:], stack, env

def if_(cond, cur_frame, stack, env):
	def w(elsebody, cur_frame, stack, env):
		def w(body, cur_frame, stack, env):
			if cond:
				return [execute([body], env)[0][0]] + cur_frame, stack, env
			else:
				return [execute([elsebody], env)[0][0]] + cur_frame, stack, env
		return [(w, True)] + cur_frame, stack, env
	return [(w, True)] + cur_frame, stack, env

def lambda_(code, cur_frame, stack, env):
	def w(arg, cur_frame, stack, env):
		new_env = env.copy()
		new_env['#'] = arg
		return execute(code, new_env)[0] + cur_frame, stack, env
	return [(w, True)] + cur_frame, stack, env



std_env = {
	'r': (lambda cur_frame, stack, env: (([cur_frame[1], cur_frame[0]] + cur_frame[2:]), stack, env), False),
	'd': (lambda cur_frame, stack, env: (([cur_frame[0]] + cur_frame), stack, env), False),
	'rep': (lambda arg, cur_frame, stack, env: (([cur_frame[0]]*int(arg) + cur_frame), stack, env), True),
	'rem': (lambda cur_frame, stack, env: (cur_frane[1:], stack, env), False),
	'v': (lambda arg, cur_frame, stack, env: ([cur_frame[:int(arg)]] + cur_frame[int(arg):], stack, env), True),
	'exec': (lambda arg, cur_frame, stack, env: execute(arg, env), True),
	'quote': (lambda arg, cur_frame, stack, env: ([arg[1:-1]]+cur_frame, stack, env), True),
	'*': (multiply, True),
	'/': (divide, True),
	'+': (add, True),
	'-': (subtract, True),
	'map': (map_, True),
	'eq': (eq, True),
	'@': (index, True),
	'^': (raise_, True),
	'if': (if_, True),
	'lambda': (lambda_, True)
}