import inspect
import functools

NoneType = type(None)

class subscripting:
	def __init__(self, func):
		self._func = func

	def __getitem__(self, *args, **kwargs):
		return self._func(*args, **kwargs)

class TypedVar:
	def __init__(self, name, type):
		self.name = name
		self.type = type

	def __set__(self, instance, value):
		try:
			assert(isinstance(value, self.type))
		except:
			raise TypeError("'%s' should be of type '%s' but got '%s' of type '%s'." % 
				(self.name, repr(self.type), value, repr(type(value))))
		instance.__dict__[self.name] = value

class GenericMeta(type):
	def __getitem__(self, args): return self._handle_args(args)

	def __instancecheck__(self, instance):
		return instance.__class__ in self._type

	def __repr__(self):
		return ' | '.join(map(lambda x: x.__name__, self._type))

	def __or__(self, other):
		self._type += other._type
		return self

	def __eq__(self, other):
		if hasattr(other, '_type'):
			return set(self._type) == set(other._type)
		else:
			return False

class AST(metaclass=GenericMeta):
	@staticmethod
	def paramhandler(func):
		@functools.wraps(func)
		def wrapper(cls, *args):
			a = GenericMeta('', (AST,), {})
			return func(a, *args)
		return wrapper

class Type(AST):
	@classmethod
	@AST.paramhandler
	def _handle_args(cls, type):
		cls._type = [type]
		return cls

class FuncMeta(type):
	def __getitem__(self, args): return self._handle_args(*args)

	def __instancecheck__(self, instance):
		if not callable(instance): return False
		sig = inspect.signature(instance)
		return all(a == b.annotation for a, b in zip(self._parms, sig.parameters.values())) and sig.return_annotation == self._return

	def __repr__(self):
		return "(%s) -> %s" % (', '.join(map(str, self._parms)), self._return)

class Function(metaclass=FuncMeta):
	@classmethod
	def _handle_args(cls, *args):
		a = FuncMeta('', (), {})
		*args, a._return = args
		a._parms = args
		return a

class AnyMeta(type):
	def __instancecheck__(self, instance): return True
	def __repr__(self): return 'Any'

class Any(metaclass=AnyMeta): pass

class IterableMeta(type):
	def __getitem__(self, args): return self._handle_args(args)

	def __instancecheck__(self, instance):
		instance = iter(instance)
		I = 0
		for i, b in enumerate(self._type):
			if b == ...:
				I = i
				break
			try:
				a = next(instance)
			except StopIteration:
				return False
			if not isinstance(a, b):
				return False
		else:
			return True
		for a in instance:
			if not isinstance(a, self._type[I - 1]):
				return False
		return True


	def __repr__(self): return '[%s]' % ', '.join(self._type)

class Iterable(metaclass=IterableMeta):
	@classmethod
	def _handle_args(cls, args):
		a = IterableMeta('', (), {})
		if not hasattr(args, '__next__'):
			args = [args]
		a._type = args
		return a

class TypeVarMeta(type):
	def __getitem__(self, args): return self._handle_args(args)

	def __instancecheck__(self, instance):
		if isinstance(instance, self._type):
			self._type = instance.__class__
			return True
		else:
			return False

	def __repr__(self): return 'TypeVar[%s]' % repr(self._type)

class TypeVar(metaclass=TypeVarMeta):
	_names = {}

	@classmethod
	def _handle_args(cls, args):
		if isinstance(args, list):
			if len(args) == 2:
				a = TypeVarMeta('', (), {})
				a._type = args[1]
				TypeVar._names[args[0]] = a
				return a
			elif len(args) == 1:
				return TypeVar._names[args[0]]
		else:
			a = TypeVarMeta('', (), {})
			a._type = args
			return a

def HasAttrMeta(type):
	def __getitem__(self, args): return self._handle_args

	def __instancecheck__(self, instance): return hasattr(instance, self._attr)

def HasAttr(metaclass=HasAttrMeta):
	@classmethod
	def _handle_args(cls, attr):
		a = HasAttrMeta('', (), {})
		a._attr = attr
		return a

def typed(func):
	signature = inspect.signature(func)
	@functools.wraps(func)
	def _typed(*args, **kwargs):
		boundargs = signature.bind(*args, **kwargs)
		for arg, value in boundargs.arguments.items():
			annotation = signature.parameters[arg].annotation
			if not isinstance(value, annotation):
				raise TypeError("Parameter '%s' should have been of type '%s' when calling '%s', but '%s' of type '%s' was given." % 
					(arg, annotation, func.__qualname__, repr(value), type(value)))
		x = func(*boundargs.args, **boundargs.kwargs)
		if signature.return_annotation != signature.empty and not isinstance(x, signature.return_annotation):
			raise TypeError("Function '%s' should have returned type '%s', but '%s' of type '%s' was returned." % 
				(func.__qualname__, signature.return_annotation, repr(x), type(x)))
		return x
	return _typed

def case(val, options):
	for option, f in options.items():
		if option == True: continue
		if isinstance(val, option): return f(val)
	else:
		return options[True](val)

def catch(f):
	@functools.wraps(f)
	def _catch(*args, **kwargs):
		try:
			return f(*args, **kwargs)
		except BaseException as e:
			return e
	return _catch

Optional = subscripting(lambda type: Type[type] | Type[NoneType])
Number = Type[int] | Type[float] | Type[complex]

__all__ = [TypedVar, Type, Optional, Function, Any, Number, Iterable, TypeVar, HasAttr, typed, case, catch]
