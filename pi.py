import functools
from collections import defaultdict

@functools.lru_cache()
def x(n):
	return 16*x(n - 1) + (120*n**2 - 89*n + 16)/(512*n**4 - 1024*n**3 + 712*n**2 - 206*n + 21) if n > 0 else 0

def digit(n):
	return int(16*x(n))

for n in range(10):
	print(digit(n))