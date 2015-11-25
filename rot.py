ab = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def rot(s,n):
	return ''.join(map(lambda x: ab[(ab.index(x.upper()) + n) % 26] if x.upper() in ab else x,list(s)))
print(rot(input(),2))
