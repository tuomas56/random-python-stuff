import timeit

def wilson_montgomery():
	for n in range(5, 1000):
		ans0 = 1
		ans1 = 1
		for i in range(1,(n+1) // 2 - 1):
		    ans0 = (ans0 * (2*i + 0)) % n   
		    ans1 = (ans1 * (2*i + 1)) % n   

		ans = (ans0 * ans1) % n == 1

def wilson_normal():
	for n in range(5, 1000):
		a = 1
		b = n - 2
		while b:
			a *= b
			b -= 1
		ans = a % n == 1