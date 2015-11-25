#FPNum(m, e) => m / 10^e

from decimal import Decimal

class FPNum:
	@staticmethod
	def from_float(f):
		e = 0
		m = Decimal(f)
		while m.to_integral() != m:
			e += 1
			m *= 10
		return FPNum(m, e)

	def __init__(self, m, e):
		self.m, self.e = m, e

	def __float__(self):
		return float(self.m / 10**self.e)

	def __add__(self, other):
		if self.e > other.e:
			max_n, min_n = self, other
		else:
			max_n, min_n = other, self
		return FPNum(min_n.m * 10**(max_n.e - min_n.e) + max_n.m, max_n.e)

	def __neg__(self):
		return FPNum(-self.m, self.e)

	def __sub__(self, other):
		return self + (-other)

	def __mul__(self, other):
		return FPNum(self.m * other.m, self.e * other.e)

	def __div__(self, other):
		return FPNum(self.m / other.m, self.e * other.e)

	def __str__(self):
		return "%s(%s, %s)" % (type(self).__name__, self.m, self.e)

x = FPNum.from_float(10.12)
y = FPNum.from_float(3.8)
print(x)
print(y)
z = x + y
print(z)
print(float(z))
print(10.12 + 3.8)