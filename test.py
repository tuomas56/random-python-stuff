def test(passed,failed,tfunc,desc):
	try:
		assert(tfunc())
		return (passed + [desc]),failed
	except:
		return passed,(failed + [desc])


def do_tests(title,tests,silent=False):
	print("\n",title,"\n")
	failed = []
	passed = []
	global test
	
	for tfunc,desc in tests:
		passed,failed = test(passed,failed,tfunc,desc)

	if not silent:
		print("Passed Tests ("+str(len(passed))+"):")
		for t in passed:
			print(" "*3,t)
		print("Failed Tests ("+str(len(failed))+"):")
		for t in failed:
			print(" "*3,t)

	return passed,failed