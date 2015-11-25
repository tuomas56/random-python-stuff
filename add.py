def add(a,b):
	a = bin(a)[2:][::-1] #chop of '0b' and flip to little-endian
	b = bin(b)[2:][::-1]
	length = max(len(a),len(b)) #the length we need both strings to be minus 1
	while len(a) < length:
		a += "0"
	while len(b) < length:
		b += "0"
	a += "0"
	b += "0"
	b = map(lambda x: True if x == "1" else False,b)
	a = map(lambda x: True if x == "1" else False,a)
	c = [False for _ in range(len(a)+1)]
	result = [False for _ in range(len(a)+1)]

	for i,(x,(y,z)) in enumerate(zip(a,zip(b,c))):
		#1-bit binary full adder
		i1 = (x or y) and not (x and y)
		result[i] = (i1 or z) and not (i1 and z)
		c[i + 1] = (i1 and z) or (x and y)

	result = ''.join(map(lambda x: "1" if x else "0",result)) #flip conv and map it to result then join to form bit string
	return int(result[::-1],2) #result converted from base 2

print(add(4,2))