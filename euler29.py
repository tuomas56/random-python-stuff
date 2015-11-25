results = set([])
for a in range(2,101):
	for b in range(2,101):
		print(a,b)
		results.add(a**b)
print(results)
print(len(results))