class MemoizedFunc:
	def __init__(self,func,computed={}):
		self.computed = computed
		self.func = func

	def __call__(self,*args):
		if args not in self.computed:
			self.computed[args] = self.func(*args)
		return self.computed[args]

def memoize(func):
	return MemoizedFunc(func)

@memoize
def fib(n):
	if n < 2:
		return 1
	else:
		return fib(n-1) + fib(n-2)

for x in range(1000):
	print(x,fib(x))