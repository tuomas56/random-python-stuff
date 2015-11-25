

def rms(seed, p=15485867, m=12889):
	while True:
		seed *= p
		seed %= m
		yield seed

r = rms(47)
for _ in range(100):
	print(next(r))