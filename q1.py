from functools import reduce
import operator
import math
x = list(range(1,21))
sx = (len(x)/2)*(len(x)+1)
x.remove(7)
x.remove(2)
mul = lambda l: reduce(operator.mul,l)
s = sx - sum(x)
m = mul(range(1,21)) / mul(x)
b = (-s + math.sqrt(s**2 - (-4*(-m))))/-2
a = s - b
print(a,b) #15,5