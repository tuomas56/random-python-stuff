import inspect
from collections.abc import *

class Any(type):
	pass

def typechecked(func):
	argnames = inspect.getfullargspec(func)[0]
	def wrapper(*args,**kwargs):
		for name in kwargs.keys():
			argnames.remove(name)
		args_with_names = zip(argnames,args)
		for name, arg in args_with_names:
			if name not in func.__annotations__ or func.__annotations__[name] == Any:
				continue
			try:
				if func.__annotations__[name] == None:
					assert(isinstance(arg,type(None)))
				else:
					assert(isinstance(arg,func.__annotations__[name]))
			except:
				raise TypeError("Expected %s to be of type %s but it was of type %s." % (name,func.__annotations__[name],type(arg)))
		for name, arg in kwargs:
			if name not in func.__annotations__ or func.__annotations__[name] == Any:
				continue
			try:
				if func.__annotations__[name] == None:
					assert(isinstance(arg,type(None)))
				else:
					assert(isinstance(arg,func.__annotations__[name]))
			except:
				raise TypeError("Expected %s to be of type %s but it was of type %s." % (name,func.__annotations__[name],type(arg)))
		value = func(*args,**kwargs)
		if 'return' not in func.__annotations__ or func.__annotations__['return'] == Any:
			return value
		try:
			if func.__annotations__['return'] == None:
				assert(isinstance(value,type(None)))
			else:
				assert(isinstance(value,func.__annotations__['return']))
		except:
			raise TypeError("Expected return value to be of type %s but it was of type %s." % (func.__annotations__['return'],type(value)))
		return value
	return wrapper

@typechecked
def f() -> (Iterable):
	return [1,2,3,4]

f()

