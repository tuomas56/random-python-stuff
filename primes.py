import itertools

def gcd(a,b):
	if a == b:
		return a
	elif a > b:
		return gcd(a - b,b)
	elif b > a:
		return gcd(a,b - a)
def a(n):
	if n == 1:
		return 8
	else:
		return a(n-1) + gcd(a(n-1),n)

print(a(4))