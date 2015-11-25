p = int(input("Please enter a prime: "))
s1 = int(input("Please enter secret key 1: "))
s2 = int(input("Please enter secret key 2: "))
m1 = input("Please enter secret message 1: ")
m2 = input("Please enter secret message 2: ")
factors=lambda n: list(filter(lambda b:n%b==0,range(2,n)))
prime=lambda n: len(factors(n)) == 0
factorize=lambda n: list(map(int,str(n if prime(n) else [x if prime(x) else factorize(x) for x in [factors(n)[0],factors(n)[-1]]]).replace("[","").replace("]","").split(",")))
def proot(n):
	if n == 2:
		return 1
	else:
		pf = factorize(n-1)
		a = 2
		while True:
			result = True
			for i in pf:
				if result:
					result = pow(a,int((p-1)/i),p) != 1
			if result:
				return a
			else:
				a += 1
g = proot(p)
encode = lambda a: pow(g,a,p)
decode = lambda s,r: pow(r,s,p) 

def rot(s,n):
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
    trans = chars[n*2:]+chars[:n*2]
    rot_char = lambda c: trans[chars.find(c)] if chars.find(c) > -1 else c
    return ''.join(rot_char(c) for c in s)

print("Using prime",p,"and primitive root",g)
print("Alice has secret key",s1)
print("Bob has secret key",s2)
print("Alice sends Bob",encode(s1))
a = encode(s1)
print("Bob sends Alice",encode(s2))
b = encode(s2)
print("Alice computes",decode(s1,b))
sa = decode(s1,b)
print("Bob computes",decode(s2,a))
sb = decode(s2,a)
print("Alice encrypts",m1)
ea = rot(m1,sa)
print("Bob encrypts",m2)
eb = rot(m2,sb)
print("Alice sends Bob",ea)
ub = rot(ea,-sa)
print("Bob sends Alice",eb)
ua = rot(eb,-sb)
print("Alice decrypts",ua)
print("Bob decrypts",ub)