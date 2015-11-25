tests = []

def test(name):
	def _test(f):
		tests.append((name, f))
		return f
	return _test

def no_errors(f):
	try:
		f()
		return True
	except Exception:
		return False

def do_tests():
	print("Running %s tests.\n" % len(tests))
	good = []
	bad = []
	for name, test in tests:
		(good if no_errors(test) else bad).append(name)
	for name in good:
		print("Test - %s - SUCCEEDED" % name)
	for name in bad:
		print("Test - %s - FAILED" % name)
	print("\n%s tests succeeded, %s failed." % (len(good), len(bad)))

