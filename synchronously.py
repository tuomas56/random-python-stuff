import functools
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import time
import inspect
import copy

class Composable:
	def __init__(self, func):
		self.func = func

	def __lshift__(self, func):
		return Composable(lambda *args: func(self.func(*args)))

	def __call__(self, *args):
		return self.func(*args)

class AsyncValue:
	def __init__(self, func, args, kwargs, _pool=None):
		if _pool is None:
			_pool = pool
		self.fut = pool.submit(func, *args, **kwargs)
		self.func = Composable(lambda x: x)

	def __add__(self, other):
		x = copy.copy(self)
		x.func <<= (lambda x: x.__add__(other))
		return x

	def __str__(self):
		return self.value(no_wait=True).__str__()

	def value(self, *, no_wait=False):
		if self.fut.done() or no_wait:
			return self.func(self.fut.result())
		else:
			return self

class AsyncExecDict(dict):
	def __getitem__(self, key):
		x = super().__getitem__(key)
		if isinstance(x, AsyncValue):
			return x.value()
		else:
			return x

def inline_async(pool):
	def _inline_async(_func):
		new_dict = locals()
		del new_dict['_func']
		sig = inspect.signature(_func)

		@functools.wraps(_func)
		def _wrapper(*args, **kwargs):
			sig.bind(*args, **kwargs)
			for name, val in sig.parameters.items():
				new_dict[name] = val
			locs = AsyncExecDict(new_dict)
			exec(_func.__code__, globals(), locs)
		return _wrapper
	return _inline_async

def async(func):
	def __async(*args, **kwargs):
		return AsyncValue(func, args, kwargs)
	return __async

@async
def task():
	time.sleep(10)
	print("hi", flush=True)
	return 10

pool = ProcessPoolExecutor(4)

@inline_async(pool)
def main():
	x = task()
	time.sleep(5)
	print("hey", flush=True)
	y = x + 5
	print(y)

main()