G = 6.67384*10**-11

class Object:
	def __init__(self,pos,acc,mass):
		self.pos = pos
		self.acc = acc
		self.mass = mass

	def step(self,world):
		self.pos += self.acc

class Vector:
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def __sub__(self,other):
		return Vector(self.x - other.x, self.y - other.y)

	def __add__(self,other):
		return Vector(self.x + other.x, self.y + other.y)

	def __mul__(self,other):
		return Vector(self.x * other, self.y * other)

	def __div__(self,other):
		return Vector(self.x / other, self.y / other)

	def __invert__(self):
		return (self.x**2 + self.y**2)**0.5

	def __repr__(self):
		return "("+str(self.x)+","+str(self.y)+")"

class World:
	def __init__(self):
		self.objects = []

	def step(self):
		for x in self.objects:
			for y in filter(lambda z: z != x,self.objects):
				x.pos += ((y.pos - x.pos)/~(y.pos - x.pos))*((G*x.mass*y.mass)/((~(y.pos - x.pos))**2))/x.mass
			x.step(self)

w = World()
w.objects.append(Object(Vector(2,3),Vector(0,0),200))
w.objects.append(Object(Vector(4,5),Vector(0,0),100))
for x in range(0,10000):
	w.step()
	print(w.objects[0].pos,w.objects[1].pos)