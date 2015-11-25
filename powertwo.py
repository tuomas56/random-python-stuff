#test if n == 2**k for k, n <- ZZ in Θ(log n) time and Θ(1) space.
def ispoweroftwo(n):
	if n == 1:
		return True
	elif (n >> 1) << 1 != n:
		return False
	else:
		return ispoweroftwo(n >> 1)

for n in range(1,1025):
	print(n, ispoweroftwo(n))
