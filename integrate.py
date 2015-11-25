def integrate(f,a,b,dw):
	return sum([dw*f(a+n*dw) for n in range(0,int((b-a)/dw)+1)])

def derivative(f,x,d):
	return (f(x+d)-f(x))/d

def differentiate(f,d):
	return lambda x: derivative(f,x,d)

def within(x,d,y):
	return abs(x - y) <= d

print("Constant of integration for 2^x:",2**5 - integrate(differentiate(lambda x: 2**x,0.001),0,5,0.001))