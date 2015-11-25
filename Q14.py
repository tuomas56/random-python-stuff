f = lambda n: n/2 if n % 2 == 0 else 3*n+1
def collatz(n):
	print(str(int(n*100/1000000))+"%")
	l = 1
	while f(n) != 1:
		n = f(n)
		l += 1
	return l + 1 #because the final one is included

stats = dict(zip(range(1,1000000),map(collatz,range(1,1000000))))
k = list(stats.keys())
v = list(stats.values())
print(k[v.index(max(v))])