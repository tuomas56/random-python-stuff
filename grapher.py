from matplotlib.pyplot import *

def plotf(f,start,stop,prec):
	x = [start + x * prec for x in range(int(stop/prec))]
	fx = list(map(f,x))
	return plot(x,fx)

print("Simple Grapher")
modules = input("Required Modules (comma seperated): ").split(',')
if modules != ['']:
	for x in modules:
		exec("from "+x+" import *")

while True:
	f = input("F(x) := ")
	if f == "quit()":
		quit()
	xlabel("x")
	ylabel("F(x)")
	plotf(lambda x: eval(f),float(input("Start := ")),float(input("Stop := ")),float(input("Step := ")))
	show()
