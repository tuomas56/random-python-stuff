from functools import partial
from operator import lshift, add
import time

def pack_varint(n: int) -> bytes:
	"""Pack an integer into bytes using 7 bits with a continuation bit."""
	if n == 0:
		return b'\x00'
	result = to_bin_str(n)
	result = "0"*((7 - len(result) % 7) % 7) + result
	result = chunks(result, 7)
	result = map(partial(int, base=2), result)
	result = list(map(partial(add, 1), map(partial(inv(lshift), 1), result)))
	result[-1] -= 1
	result = map(bytes, map(lambda x: [x], result))
	return b''.join(result)

def unpack_varint(s: bytes, stream=False) -> (int, bytes):
	"""Unpack bytes to a varint and the remaining bytes"""
	num = []
	while True:
		if stream:
			n = ord(s.read(1))
		else:
			n, s = s[0], s[1:]
		if n == 0:
			return 0, s
		x = to_bin_str(n)[:-1]
		x = "0"*((7 - len(x) % 7) % 7) + x
		num.append(x)
		if not n % 2:
			break
	return int(''.join(num), 2), s

def to_bin_str(n: int) -> str:
	"""Convert an integer into binary"""
	result = []
	while n:
		result.insert(0, str(n % 2))
		n >>= 1
	return ''.join(result)

def chunks(l: list, n: int) -> iter:
	"""Divide l into floor(len(l)/n) chunks of n and one chunk of len(l) % n."""
	for i in range(0, len(l), n):
		yield l[i:i+n]

def inv(f):
	"""inv(f: (a -> b)) -> (a -> b). Return a function which reverses its arguments before applying them to 'f'."""
	def _wrapper(*args, **kwargs):
		return f(*(args[::-1]), **kwargs)
	return _wrapper

def wait_until(f, period=0.25):
	while not f():
		time.sleep(period)