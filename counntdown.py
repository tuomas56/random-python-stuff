def guesses(x):
	for _ in range(2+round((x-20)%4,0)):
		yield 4 - getprev()
		x -= 4

	def solve(n):
		if n == 7:
			n -= getprev()
			n -= 7 - getprev()
			yield 7 - getprev()
			if n == 3:
				yield 1
			elif n == 5:
				yield getprev() - 1
		else:


	yield from solve(x)