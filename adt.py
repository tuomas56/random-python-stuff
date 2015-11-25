import copy

class ADT:
	@staticmethod
	def __instancecheck__(val, cls):
		try:
			if cls._adt_type == "product":
				for x, y in zip(val, cls._type):
					assert isinstance(x, y)
			elif cls._adt_type == "sum":
				try:
					assert isinstance(val, cls._type[0])
				except:
					assert isinstance(val, cls._type[1])
			elif cls._adt_type == "simple":
				assert isinstance(val, cls._type)
			return True
		except AssertionError: 
			return False
		except AttributeError: 
			return isinstance(val, cls)

	def __init__(self, name, type):
		self.__name__ = name
		self._adt_type = "simple"
		self._type = type
		self._constructed = False

	def __call__(self, value):
		if not self._constructed:
			assert ADT.__instancecheck__(value, self)
			x = copy.copy(self)
			x._value = value
			x._constructed = True
			return x
		else:
			raise AttributeError()


	def __str__(self):
		if self._adt_type == "simple":
			return "%s(%s)" % (self.__name__, self._value)
		elif self._adt_type == "sum":
			return "%s(%s)" % (self.__name__[0] if ADT.__instancecheck__(self._value, self._type[0]) else self.__name__[1], self._value)
		elif self._adt_type == "product":
			return "(%s(%s),%s(%s))" % (self.__name__[0], self._value[0], self.__name__[1], self._value[1])


	def __or__(self, other):
		if self._constructed:
			try:
				return self._type[0].__or__(self, other)
			except:
				return self._type[1].__or__(self, other)
		else:
			x = copy.copy(self)
			x._adt_type = "sum"
			x.__name__ = (self.__name__, other.__name__)
			x._type = (self._gettype(), other._gettype())
			return x

	def __and__(self, other):
		if self._constructed:
			return self._type.__and__(self, other)
		else:
			x = copy.copy(self)
			x._adt_type = "product"
			x.__name__ = (self.__name__, other.__name__)
			x._type = (self._gettype(), other._gettype())
			return x

	def _matched(self):
		return (self._value,)

	def _gettype(self):
		return self._type

	def __hash__(self):
		return self.__name__.__hash__()



def match(options, value):
	for key, func in options:
		if ADT.__instancecheck__(value, key):
			return func(*value._matched())

Nothing = ADT('Nothing', None.__class__)
Just = ADT('Just', object)
Maybe = Nothing | Just

def find(needle, haystack):
	for index, item in enumerate(haystack):
		if needle == item:
			return Maybe(index)
	else:
		return Maybe(None)

match([
	(Nothing, (lambda _: print("Not Found!"))),
	(Just, (lambda i: print("Found: %s" % i)))
],find(1, [2,3,4]))

print(ADT.__instancecheck__(Nothing(None), Nothing))