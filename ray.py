from vector import Vec3, Color
from functools import partial
from operator import methodcaller, is_not
import numpy
from PIL import Image

class Sphere:
	def __init__(self, center, radius, color):
		self.center = center
		self.radius = radius 
		self.color = color

	def intersection(self, ray):
		a = ray.d.mag2()
		b = 2 * (ray.d ^ (ray.o - self.center))
		c = (ray.o - self.center).mag2() - self.radius**2
		d1 = (-b + (b**2 - 4*a*c)**0.5)/(2*a)
		d2 = (-b - (b**2 - 4*a*c)**0.5)/(2*a)
		print(d1,d2)
		d1 = d1 if isinstance(d1, float) else -1
		d2 = d2 if isinstance(d2, float) else -1
		d = min(d1, d2)
		i = ray.o + d*ray.d
		return Intersection(i, d, self.normal(i), self)

	def normal(self, point):
		return ~(point - self.center)

	def __str__(self):
		return "Sphere(%s, %s, %s)" % (self.center, self.radius, self.color)


class Ray:
	def __init__(self, o, d):
		self.o, self.d = o, ~d

class Intersection:
	def __init__(self, point, distance, normal, obj):
		self.p = point
		self.n = normal
		self.d = distance
		self.obj = obj

	def __lt__(self, other):
		return self.d < other.d

	def __gt__(self, other):
		return self.d > other.d

	def __str__(self):
		return "Intersection(%s, %s, %s, %s)" % (self.p,self.d,self.n,self.obj)

#def test_intersect(ray, objects, ignore=None):
#	return min(Intersection(None,-1,None,None),*map(methodcaller('intersection',ray),filter(partial(is_not,ignore),objects)))

def trace(ray, objects, light, ambient, max_recurse):
	i = objects[0].intersection(ray)
	if i.d != -1:
		return i.obj.color
	else:
		return Color(ambient,ambient,ambient)



def main():
	light = Vec3(0, 10, 0)
	objs = []
	objs.append(Sphere(Vec3(-2,0,1), 1 , Color(0,255,0)))
	img = Image.new("RGB",(256,256))
	camera = Vec3(0,0,0)
	for x in range(256):
		for y in range(256):
			print(x,y)
			ray = Ray(camera, ~(Vec3(x-128,y-128,1)-camera))
			col = trace(ray, objs, light, 0.1, 10)
			print(col)
			col = (int(col.r),int(col.g),int(col.b))
			img.putpixel((x,255-y),col)
	img.save("out.png","PNG")

if __name__ == "__main__":
	main()