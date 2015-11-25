from test import do_tests

class Vec3:
	def __init__(self,x=.0,y=.0,z=.0):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)

	def __eq__(self,other):
		if isinstance(other,Vec3):
			return self.x == other.x and self.y == other.y and self.z == other.z
		else:
			return False


	def __add__(self,other):
		if isinstance(other,Vec3):
			return Vec3(self.x + other.x,self.y + other.y,self.z + other.x)
		else:
			raise TypeError("Can't add a 3-vector to a "+type(other).__name__+".")

	def __radd__(self,other):
		return self + other #addition is commutative.

	def __sub__(self,other):
		if isinstance(other,Vec3):
			return self + (-other)
		else:
			raise TypeError("Can't subtract a "+type(other).__name__+" from a 3-vector.")

	def __rsub__(self,other):
		if isinstance(other,Vec3):
			return (-self) + other
		else:
			raise TypeError("Can't subtract a 3-vector from a "+type(other).__name__+".")

	def __neg__(self):
		return Vec3(-self.x,-self.y,-self.z)

	def __mul__(self,other):
		if isinstance(other,float) or isinstance(other,int):
			return Vec3(self.x*other,self.y*other,self.z*other)
		else:
			raise TypeError("Can't scale a 3-vector by a "+type(other).__name__+".")

	def __rmul__(self,other):
		return self * other #scalar multiplication is commutative

	def __truediv__(self,other):
		if isinstance(other,float) or isinstance(other,int):
			return Vec3(self.x/other,self.y/other,self.z/other)
		else:
			raise TypeError("Can't scale a 3-vector by a "+type(other).__name__+".")

	def __rtruediv__(self,other):
		raise TypeError("Can't divide a "+type(other).__name__+" by a 3-vector.") #NO. Never. No matter what type.

	def __floordiv__(self,other):
		if isinstance(other,float) or isinstance(other,int):
			return Vec3(self.x//other,self.y//other,self.z//other)
		else:
			raise TypeError("Can't scale a 3-vector by a "+type(other).__name__+".")

	def __rfloordiv__(self,other):
		raise TypeError("Can't divide a "+type(other).__name__+" by a 3-vector.") #Same deal.

	def __xor__(self,other): #dot product
		if isinstance(other,Vec3):
			return self.x*other.x + self.y*other.y + self.z*other.z
		else:
			raise TypeError("Can't dot a 3-vector and a "+type(other).__name__+".")

	def __rxor__(self,other):
		return self ^ other #dot product is commutative

	def __abs__(self):
		return (self.x**2 + self.y**2 + self.z**2)**0.5

	def mag2(self):
		return self ^ self

	def __invert__(self):
		try:
			return self / abs(self)
		except:
			return self

	def __and__(self,other): #Just to make sure I don't get the three types of multiplication confused, each has their
							 #own operator. Cross Product.
		if isinstance(other,Vec3):
			return Vec3(self.y*other.z - self.z*other.y,self.z*other.x - self.x*other.z,self.x*other.y - self.y*other.x)
		else:
			raise TypeError("Can't cross a 3-vector and a "+type(other).__name__+".")

	def __rand__(self,other): #Cross Product is anticommutative.
		if isinstance(other,Vec3):
			return -(self & other)
		else:
			raise TypeError("Can't cross a 3-vector and a "+type(other).__name__+".")


	def __repr__(self):
		return "Vec3(x=%s,y=%s,z=%s)" % (self.x,self.y,self.z)

Vec3.ORIGIN = Vec3(0,0,0)
Vec3.X = Vec3(1,0,0)
Vec3.Y = Vec3(0,1,0)
Vec3.Z = Vec3(0,0,1)

class Pos3(Vec3):
	def __repr__(self):
		return "Pos3(x=%s,y=%s,z=%s" % (self.x,self.y,self.z)

	def distance(self,other):
		return abs(other - self)

class Color:

	def __init__(self,r=.0,g=.0,b=.0):
		self.r = float(r)
		self.g = float(g)
		self.b = float(b)

	def __eq__(self,other):
		if isinstance(other,Colour):
			return self.r == other.r and self.g == other.g and self.b == other.b
		else:
			return False


	def __add__(self,other):
		if isinstance(other,Colour):
			return Colour(self.r + other.r,self.g + other.g,self.b + other.b)
		else:
			raise TypeError("Can't add a color to a "+type(other).__name__+".")

	def __radd__(self,other):
		return self + other #addition is commutative.

	def __sub__(self,other):
		if isinstance(other,Colour):
			return self + (-other)
		else:
			raise TypeError("Can't subtract a "+type(other).__name__+" from a colour.")

	def __rsub__(self,other):
		if isinstance(other,Colour):
			return (-self) + other
		else:
			raise TypeError("Can't subtract a colour from a "+type(other).__name__+".")

	def __neg__(self):
		return Colour(-self.r,-self.g,-self.b)

	def __mul__(self,other):
		if isinstance(other,float) or isinstance(other,int):
			return Colour(self.r*other,self.g*other,self.b*other)
		else:
			raise TypeError("Can't scale a colour by a "+type(other).__name__+".")

	def __rmul__(self,other):
		return self * other #scalar multiplication is commutative

	def __truediv__(self,other):
		if isinstance(other,float) or isinstance(other,int):
			return Colour(self.r/other,self.g/other,self.b/other)
		else:
			raise TypeError("Can't scale a colour by a "+type(other).__name__+".")

	def __rtruediv__(self,other):
		raise TypeError("Can't divide a "+type(other).__name__+" by a colour.") #NO. Never. No matter what type.

	def __floordiv__(self,other):
		if isinstance(other,float) or isinstance(other,int):
			return Colour(self.r//other,self.g//other,self.b//other)
		else:
			raise TypeError("Can't scale a colour by a "+type(other).__name__+".")

	def __rfloordiv__(self,other):
		raise TypeError("Can't divide a "+type(other).__name__+" by a colour.") #Same deal.

	def __repr__(self):
		return "Colour(r="+str(self.r)+",g="+str(self.g)+",b="+str(self.b)+")"


	def interpolate(self,other,control):
		return self*(1-control) + other*control
	
Color.R = Color(1,0,0)
Color.G = Color(0,1,0)
Color.B = Color(0,0,1)
Color.BLACK = Color(0,0,0)
	

def tests():
	#I don't have a unit test library so I'm improvising.
	#They're wrapped in lambdas so they're no executed yet,
	#so that we can execute them later wrapped in a try...except.
	do_tests("3-Vector",[(lambda: Vec3(1,1,1) + Vec3(2,2,2) == Vec3(3,3,3),"3-Vector addition."),
			  (lambda: Vec3(3,4,3) - Vec3(1,1,1) == Vec3(2,3,2),"3-Vector subtraction."),
			  (lambda: Vec3(1,1,1) * 6 == Vec3(6,6,6),"3-Vector scalar multiplication."),
			  (lambda: -Vec3(2,3,2) == Vec3(-2,-3,-2),"3-Vector negation."),
			  (lambda: Vec3(3,3,3) / 3 == Vec3(1,1,1),"3-Vector scalar division."),
			  (lambda: Vec3(1,2,3) ^ Vec3(2,1,1) == 7,"3-Vector dot product."),
			  (lambda: abs(Vec3(1,1,1)) == 3**0.5,"3-Vector magnitude."),
			  (lambda: abs(~Vec3(3,3,3)) == 1,"3-Vector normalization."),
			  (lambda: Vec3(0,0,1) & Vec3(1,0,0) == Vec3(0,1,0),"3-Vector cross product.")])

	do_tests("Colour",[(lambda: Colour(0.5,0.5,0.5) + Colour(0.2,0,0) == Colour(0.7,0.5,0.5),"Colour addition."),
			  (lambda: Colour(0.5,0.5,0.5).interpolate(Colour(1,1,1),0.5) == Colour(0.75,0.75,0.75),"Colour interpolation."),
			  (lambda: Colour(1,1,1) * 0.5 == Colour(0.5,0.5,0.5),"Colour scalar multiplication."),
			  (lambda: Colour(1,1,1) / 2 == Colour(0.5,0.5,0.5),"Colour scalar division."),
			  (lambda: -Colour(1,1,1) == Colour(-1,-1,-1),"Colour negation."),
			  (lambda: Colour(1,1,1) - Colour(0.5,0.5,0.5) == Colour(0.5,0.5,0.5),"Colour subtraction.")])


if __name__ == "__main__":
	tests()