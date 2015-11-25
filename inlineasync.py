from concurrent.futures import ProcessPoolExecutor
from functools import partial
import time

class FakeVal:
	def __init__(self, done_func):
		self._func = done_func	
		@partial(setattr, self, '__setattr')
		def __setattr__(self, name, value):
			return FakeVal(lambda v: v.__setattr__(name, value))

	def __getattr__(self, name):
		if name != '_done':
			return FakeVal(lambda v: v.__getattr__(name))
		else:
			return super().__getattr__('_done')

	def __add__(self, other):
		return FakeVal(lambda v: v + other)

	def __mul__(self, other):
		return FakeVal(lambda v: v * other)

	def __sub__(self, other):
		return FakeVal(lambda v: v - other)

	def __div__(self, other):
		return FakeVal(lambda v: v / other)

	def _done(self, val):
		result = self._func(val)
		while isinstance(result, FakeVal):
			result = result._func(val)
		return result

class AsyncVal:
	def __init__(self, fut):
		self._fut = fut
		self._fake = FakeVal(lambda _: _)

	@property
	def value(self):
	    if self._fut.done():
	    	return self._fake._done(self._fut.result())
	    else:
	    	return self._fake

	def wait(self):
		self._fut.result()

pool = ProcessPoolExecutor(2)

def f():
	time.sleep(10)
	print("Hi")
	return 5

x = AsyncVal(pool.submit(f))
y = x.value + 2
x.wait()
print(x.value)
print(y.value)