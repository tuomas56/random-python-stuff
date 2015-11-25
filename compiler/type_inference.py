import ast
import abc

#literal -> type
#variable -> value type
#function call -> return type -> argument types
#builtins -> predef type

class LiteralNode(metaclass=abc.ABCMeta):
	pass

LiteralNode.register(ast.Str)
LiteralNode.register(ast.Num)

class ArrayNode(metaclass=abc.ABCMeta):
	pass

ArrayNode.register(ast.List)
ArrayNode.register(ast.Tuple)

class Module(list):
	def __repr__(self):
		return 'Module' + super().__repr__()

class Array(list):
	def __repr__(self):
		return 'Array' + super().__repr__()

class Constraint(list):
	def __repr__(self):
		return 'Constraint' + super().__repr__()

	def append(self, other):
		if other not in self:
			super().append(other)

class TypeOf(list):
	def __repr__(self):
		return 'TypeOf' + super().__repr__()

def infer_type(node, env):
	if isinstance(node, LiteralNode):
		return infer_literal_type(node, env)
	elif isinstance(node, ArrayNode):
		return infer_array_type(node, env)
	elif isinstance(node, ast.Assign):
		val, env = infer_type(node.value, env)
		env[node.targets[0].id] = val
		return None, env
	elif isinstance(node, ast.Name):
		return env.get(node.id, Constraint([TypeOf([node.id])])), env
	elif isinstance(node, ast.Module):
		t_node = Module()
		for expr in node.body:
			t_expr, env = infer_type(expr, env)
			t_node.append(t_expr)
		return t_node, env
	elif isinstance(node, ast.Expr):
		t, env = infer_type(node.value, env)
		return t, env
	elif isinstance(node, ast.Call):
		return infer_type(node.func, env)[0](node.args, env)
	elif isinstance(node, ast.Lambda):
		return lambda args, env: (infer_type(node.body, env), env)


def infer_literal_type(node, env):
	if isinstance(node, ast.Str):
		return Constraint([str]), env
	elif isinstance(node, ast.Num):
		if isinstance(node.n, int):
			return Constraint([int]), env
		elif isinstance(node.n, float):
			return Constraint([float]), env
		elif isinstance(node.n, complex):
			return Constraint([complex]), env
	else:
		raise TypeError("Not a literal node!")

def infer_array_type(node, env):
	t_node = Array()
	for expr in node.elts:
		try:
			t_expr, env = infer_type(expr,env)
		except:
			t_expr = infer_type(expr, env)
		t_node.append(t_expr)
	return Constraint([t_node]), env

def t_int(args, env):
	assert len(args) < 3
	if len(args) != 0:
		t_arg_0, env = infer_type(args[0],env)
		assert t_arg_0 == Constraint([str])
		if len(args) == 2:
			t_arg_1, env = infer_type(args[1], env)
			assert t_arg_1 == Constraint([int])
	return Constraint([int]), env

def t_float(args, env):
	assert len(args) < 2
	if len(args) != 0:
		t_arg_0, env = infer_type(args[0],env)
		assert t_arg_0 == Constraint([str])
	return Contraint([float]), env

env_with_builtins = {
	'int': t_int,
	'float': t_float
}

node = ast.parse("a = 4; b = '4'; c = a; [a, int(b), lambda x: x * 2, lambda x: (c, b)]")

print(infer_type(node, env_with_builtins)[0])