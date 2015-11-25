import numbers

#module Fractions
#contains classes and functions for dealing with fractions
#@author Tuomas Laakkonen
#@date 1418054074 8/12/14
#@copyright Tuomas Laakkonen (c) 2014 
#@license GPLv3

#contains fields for numerator and denominator and methods to simplify
class Fraction(numbers.Rational):
	def __init__(self,numerator,denominator):
		self._numerator = numerator
		self._denominator = denominator
		self.simplify()

	def simplify(self):
		numerator = self._numerator
		denominator = self._denominator
		while gcd(numerator,denominator) > 1: #while the numbers are not coprime
			a = gcd(numerator,denominator)
			numerator //= a #divide both sides by the hcf
  		self._numerator = numerator
		self._denominator = denominator

	@property
	def numerator(self):
	    return self._numerator
	@numerator.setter
	def numerator(self, value): #automatically simplify when setting
	    self._numerator = value
	    self.simplify()

	@property
	def denominator(self):
	    return self._denominator
	@denominator.setter
	def denominator(self, value): #automatically simplify when setting
	    self._denominator = value
	    self.simplify()	

	def sign(self):
		return sign(self.denominator) * sign(self.numerator)

	#Fraction(1,4).flip() == Fraction(4,1)
	def flip(self):
		return Fraction(self.denominator,self.numerator)
	def __str__(self):
		return {1:"",0:"",-1:"-"}[self.sign()] + str(abs(self.numerator)) + "/" + str(abs(self.denominator))

	def __repr__(self):
		return str(self)

	def __float__(self):
		return self.numerator / self.denominator

	def __int__(self):
		return self.__trunc__()

	def __mul__(self,other): #self * other
		if isinstance(other,int):
			return self * from_int(other)
		elif isinstance(other,float):
			return self * from_float(other)
		elif isinstance(other,Fraction):
			return Fraction(self.numerator * other.numerator,self.denominator * other.denominator)
		else:
			raise ValueError("Can't multiply Fraction and "+str(type(other)))

	def __rmul__(self,other): #other * self
		return self * other #because multiplication is commutative

	def __div__(self,other):
		return self.__truediv__(other)

	def __rdiv__(self,other):
		return self.__rtruediv__(other)

	def __truediv__(self,other): #self / other
		if isinstance(other,int):
			return self / from_int(other)
		elif isinstance(other,float):
			return self / from_float(other)
		elif isinstance(other,Fraction):
			return self * other.flip() # a / b == a * 1/b therefore if a == c/d and b == e/f then c/d / e/f == c/d * 1/(e/f) == c/d * f/e
		else:
			raise ValueError("Can't divide Fraction by "+str(type(other)))


	def __rtruediv__(self,other): #other / self
		if isinstance(other,int):
			return from_int(other) / self
		elif isinstance(other,float):
			return from_float(other) / self
		elif isinstance(other,Fraction):
			return other * self.flip() # a / b == a * 1/b therefore if a == c/d and b == e/f then c/d / e/f == c/d * 1/(e/f) == c/d * f/e
		else:
			raise ValueError("Can't divide "+str(type(other))+" by Fraction")

	def __floordiv__(self,other): #self // other
		return int(self / other)

	def __rfloordiv__(self,other): #other // self
		return int(other / self)

	def __add__(self,other): #self + other
		if isinstance(other,int):
			return self + from_int(other)
		elif isinstance(other,float):
			return self + from_float(other)
		elif isinstance(other,Fraction):
			return Fraction(self.numerator * other.denominator + other.numerator * self.denominator,self.denominator * other.denominator)
		else:
			raise ValueError("Can't add Fraction and "+str(type(other)))

	def __radd__(self,other): #other + self
		return self + other #because adding is commutative

	def __sub__(self,other): #self - other
		if isinstance(other,int):
			return self - from_int(other)
		elif isinstance(other,float):
			return self - from_float(other)
		elif isinstance(other,Fraction):
			return Fraction(self.numerator * other.denominator - other.numerator * self.denominator,self.denominator * other.denominator)
		else:
			raise ValueError("Can't subtract Fraction from "+str(type(other)))

	def __rsub__(self,other): #other - self
		if isinstance(other,int):
			return from_int(other) - self
		elif isinstance(other,float):
			return from_float(other) - self
		elif isinstance(other,Fraction):
			return Fraction(other.numerator * self.denominator - self.numerator * other.denominator,self.denominator * other.denominator)
		else:
			raise ValueError("Can't subtract "+str(type(other))+" from Fraction")

	def __pow__(self,other): #self ** other
		return float(self) ** other

	def __rpow__(self,other): #other ** self
		return other ** float(self)

	def __abs__(self): #abs(self)
		return +self

	def __ceil__(self):
		return self.__trunc__() + 1 if self - self.__trunc__() >= 0.5 else self.__trunc__()

	def __eq__(self,other): #self == other
		if isinstance(other,int):
			return self == from_int(other)
		elif isinstance(other,float):
			return self == from_float(other)
		elif isinstance(other,Fraction):
			return self.numerator == other.numerator and self.denominator == other.numerator

	def __lt__(self,other): #self < other
		if isinstance(other,int):
			return self < from_int(other)
		elif isinstance(other,float):
			return self < from_float(other)
		elif isinstance(other,Fraction):
			return self.numerator < other.numerator and self.denominator < other.numerator

	def __le__(self,other): #self <= other
		if isinstance(other,int):
			return self <= from_int(other)
		elif isinstance(other,float):
			return self <= from_float(other)
		elif isinstance(other,Fraction):
			return self.numerator <= other.numerator and self.denominator <= other.numerator

	def __gt__(self,other): #self > other
		if isinstance(other,int):
			return self > from_int(other)
		elif isinstance(other,float):
			return self > from_float(other)
		elif isinstance(other,Fraction):
			return self.numerator > other.numerator and self.denominator > other.numerator

	def __ge__(self,other): #self >= other
		if isinstance(other,int):
			return self >= from_int(other)
		elif isinstance(other,float):
			return self >= from_float(other)
		elif isinstance(other,Fraction):
			return self.numerator >= other.numerator and self.denominator >= other.numerator

	def __floor__(self):
		return self.__trunc__()

	def __mod__(self,other): #self % other
		raise ValueError("Cannot modulo a Fraction")

	def __neg__(self): #-self
		return Fraction(self.numerator * -1,self.denominator) if self.sign() == 1 else self

	def __pos__(self): #+self
		return Fraction(self.numerator * -1,self.denominator) if self.sign() == -1 else self

	def __rmod__(self,other): #other % self
		raise ValueError("Cannot modulo by a Fraction")

	def __round__(self,p):
		x = str(float(self))
		return float(x[:x.index(".")+p])

	def __trunc__(self):
		return int(str(float(self)).split(".")[0])


#gcd(int a, int b) -> int
#greatest common factor of a and b
def gcd(a,b):
	while b != 0:
		b,a = a % b, b
	return a

#sign(number a) -> int
#returns the sign of a number: -1 (negative), 0 (zero) or 1 (positive)
def sign(a):
	return 1 if a > 0 else -1 if a < 0 else 0

#from_float(float a) -> fraction
#returns a fraction representing the exact value of a
def from_float(a):
	return Fraction(int(a*10**len(str(a).split(".")[1])),10**len(str(a).split(".")[1]))

#from_int(int a) -> fraction
#returns a fraction representing the exact value of a
def from_int(a):
	return Fraction(a,1)


