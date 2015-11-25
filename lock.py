from contextlib import contextmanager
import threading

LOCKS = {}

@contextmanager
def lock(name):
	if name in list(LOCKS.keys()):
		while LOCKS[name]: continue
	LOCKS[name] = True
	try:
		yield
	finally:
		LOCKS[name] = False
