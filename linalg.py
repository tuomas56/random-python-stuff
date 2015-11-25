def sign(n):
	if n == 0:
		return 0
	elif n > 0:
		return 1
	else:
		return -1

def solve_linear(d,e):
	if d == 0 and e != 0:
		raise ValueError("x^1 coefficient must be nonzero.")
	elif e == 0:
		return 0
	else:
		return -e/d

def solve_quadratic(c,d,e):
	if c == 0:
		return solve_linear(d,e)
	else:
		desc = (d**2 - 4*c*e)**0.5
		desc /= 2*c
		return ((-d)/(2*c) + desc),((-d)/(2*c) - desc)

def solve_cubic(b,c,d,e):
	if b == 0:
		return solve_quadratic(c,d,e)
	else:
		if c == 0 and d == 0:
			return (-e/b)**(1/3)
		else:
			d0 = c**2 - 3*b*d
			d1 = 2*c**2 - 9*b*c*d + 27*b**2*e

			C = ((d1 + (d1**2 - 4*d0**3)**(1/2))/2)**(1/3)

			u = [1,(-1 + 1j*3**(1/2))/2,(-1 - 1j*3**(1/2))/2]

			x = lambda k: -1/(3*b) * (c + u[k]*C + (d0/(u[k]*C)))

			return (x(0),x(1),x(2))

def solve_quartic(a,b,c,d,e):
	if a == 0:
		return solve_cubic(b,c,d,e)
	else:
		if b == 0 and c == 0 and d == 0:
			return (-e/a)**(1/4)
		else:
			p = (8*a*c - 3*b**2)/(8*a**2)
			q = (b**3 - 4*a*b*c + 8*a**2*d)/(8*a**3)

			d0 = c**2 - 3*b*d + 12*a*e
			d1 = 2*c**3 - 9*b*c*d + 27*b**3*e + 27*a*d**2 - 72*a*c*e

			Q = ((d1 + (d1**2 - 4*d0**3)**(1/2))/2)**(1/3)
			S = (1/2)*((-2/3)*p + (Q + d0/Q)/(3*a))**(1/2)

			f = -b/(4*a)
			g = -4*S**2 - 2*p
			h = q/S

			x1 = f - S + (1/2)*(g + h)**(1/2)
			x2 = f - S - (1/2)*(g + h)**(1/2)
			x3 = f + S + (1/2)*(g - h)**(1/2)
			x4 = f + S - (1/2)*(g - h)**(1/2)

			return (x1,x2,x3,x4)

def derivative(f,h=0.001):
	return lambda x: (f(x + h) - f(x))/h

def solve_newton(f,iters=10,h=0.001,initial=1):
	f_prime = derivative(f,h=h)
	x = initial
	for _ in range(iters):
		x -= f(x)/f_prime(x)
	return x


def solve_poly(*coeffs,n_iters=10,n_h=0.001,n_initial=1):
	if len(coeffs) <= 5:
		coeffs = tuple([0]*(5-len(coeffs))) + coeffs
		return solve_quartic(*coeffs)
	else:
		f = lambda x: sum(coeff*x**(len(coeffs)-i-1) for i, coeff in enumerate(coeffs))
		return solve_newton(f,iters=n_iters,h=n_h,initial=n_initial)
