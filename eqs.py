def derivative(f,x,prec=0.001):
	return (f(x+prec)-f(x))/prec

def solveNewton(f,prec=0.001):
	x = 100
	while abs(f(x)) > prec:
		x = x - (f(x)/derivative(f,x,prec))
	return x

def solvePolynomial(*coeffs,prec=0.001):
	if len(coeffs) == 1: #a = 0
		a = coeffs[0]
		return -a
	elif len(coeffs) == 2: #ax + b = 0
		a = coeffs[1]
		b = coeffs[0]
		return (-a)/b
	elif len(coeffs) == 3: #ax^2 + bx + c = 0
		a = coeffs[2]
		b = coeffs[1]
		c = coeffs[0]
		desc = b**2 - (4*a*c) #descriminant
		return ((-b + (desc**0.5))/(2*a),(-b - (desc**0.5))/(2*a)) #two solutions
	else: #approximate the solution using newtons method
		f = lambda x: sum([j*x**i for i,j in enumerate(coeffs[::-1])])
		return solveNewton(f,prec)
