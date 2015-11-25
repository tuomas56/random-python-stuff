def d(n):
	return sum(filter(lambda x: n % x == 0,range(1,n)))

nums = set()
for n in range(10000):
	a = d(n)
	if d(a) == n and a != n:
		nums.add(a)
		nums.add(n)
print(sum(nums))