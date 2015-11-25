results = [[]]*1000
for p in range(1000):
	print(p,flush=True)
	for a in range(p):
		for b in range(p):
			for c in range(p):
				if a**2 + b**2 == c**2:
					results[p].append((a,b,c))

print(results)