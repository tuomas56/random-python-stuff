def d(n):
	return sum(filter(lambda x: n % x == 0,range(1,n)))

results = []
for n in range(28123+1):
	if d(n) > n:
		print(n)