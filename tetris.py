import itertools
from time import time
def reset():
	print(chr(27) + "[2J")

def drawframe():
	...

blocks = {
	't':"""@@@
 @ """,
	'l':"""@
@
@@""",
	'bl':""" @
 @
@@""",
	'f':"""@
@
@
@""",
    'b':"""@@
@@""",
    's':"""@@
 @@""",
    'bs':""" @@
@@"""
}

def distribute(arr,target):
	for x in range(0,len(target)):
		target[x].append(arr.pop(0))
	return target


def sleep(x):
	target = time() + x/1000
	while time() <= target:
		pass

#0: 0deg
#1: 90deg
#2: 180deg
#3: 270deg
def rotate(b,n):
	b = list(map(list,b.split('\n')))
	if n == 0:
		return '\n'.join(map(''.join,b))
	elif n == 2:
		return '\n'.join([''.join(x[::-1]) for x in b][::-1])
	elif n == 1:
		result = [[] for x in range(len(b[0]))]
		for x in b:
			distribute(x,result)
		return '\n'.join([''.join(x)[::-1] for x in result])
	elif n == 3:
		result = [[] for x in range(len(b[0]))]
		for x in b:
			distribute(x,result)
		return '\n'.join([''.join(x) for x in result])		

