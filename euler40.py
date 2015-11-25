c = ""
for x in range(1,2000000):
	c += str(x)

print(int(c[0]))

print(int(c[0]) * int(c[9]) * int(c[99]) * int(c[999]) * int(c[9999]) * int(c[99999]) * int(c[999999]))