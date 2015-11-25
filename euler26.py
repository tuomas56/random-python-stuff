from math import log10

def n_digits(num):
	return int(log10(num) + 1)

def nth_digit(num, dig):
	return (num % 10**dig) // 10**(dig-1)

def long_divide(p,q):
	s = []
	i = 1
	n = nth_digit(p, i)
	for _ in range(n_digits(p)):
		qo, d = divmod(n, q)
		s.append(qo)
		n -= qo * q
		n *= 10
		i += 1
		n += nth_digit(p, i)
	return sum(n*10**i for i, n in enumerate(s[::-1]))



print(long_divide(425,25))