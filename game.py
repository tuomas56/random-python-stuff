import os
import sys
import random
import time
import math


class Pos:
	def __init__(self,x,y):
		self.x = x
		self.y = y

health = 100
money = 0
home = Pos(0,0)
location = Pos(0,0)

UP = "\x1b[A"
DOWN = "\x1b[B"
RIGHT = "\x1b[C"
LEFT = "\x1b[D"

INVENTORY = []
INVWEIGHT = 0
OBJECTS = {}

WEIGHT = {"W":2,"R":8}
MAXWEIGHT = 40

CURINDEX = 0

def RLE(ls):
	result = []
	rlist = []
	for elem in ls:
		if not elem in rlist:
			result.append((ls.count(elem),elem))
			rlist.append(elem)
	return result

def getLightLevel():
	return (math.sin(time.time() / 30) + 1)*80

def GetMap(x):
	def GetMap2(y):
		if (location.y - y)**2 + ((location.x - x)/2**0.5)**2 <= getLightLevel()**2:
			if location.x == x and location.y == y:
				return "@"
			elif home.x == x and home.y == y:
				return "#"
			elif (x,y) in list(OBJECTS.keys()):
				return OBJECTS[(x,y)]
			else:
				return " "
		else:
			return "*"
	return GetMap2

MAP = GetMap

def dispitem(x):
	if x[0] > 1:
		return str(x[0]) + " " + x[1]
	else:
		return x[1]

def frame():
	(width,height) = os.get_terminal_size()
	height -=3
	stats = "HP:" + str(health) + "|GOLD:" + str(money) + "|HOME:" + str(home.x) + "," + str(home.y) + "|LOCATION:" + str(location.x) + "," + str(location.y)
	remcols = width - len(stats)
	stats = "="*(remcols//2) + stats + "="*(remcols//2) + "="*(remcols % 2)
	print(stats)
	inv = "INVENTORY:"+'|'.join(list(map(lambda x: "@" + dispitem(x) if RLE(INVENTORY).index(x) == CURINDEX else dispitem(x),RLE(INVENTORY))))
	remcols = width - len(inv)
	inv = "="*(remcols//2) + inv + "="*(remcols//2) + "="*(remcols % 2)
	print(inv)
	wt = "WEIGHT:" + str(INVWEIGHT) + "|MAX WEIGHT:" + str(MAXWEIGHT)
	remcols = width - len(wt)
	wt = "="*(remcols//2) + wt + "="*(remcols//2) + "="*(remcols % 2)
	print(wt)
	for y in range(height):
		for x in range(width):
			print(GetMap(x)(y),end="")

def welcome():
	(width,height) = os.get_terminal_size()
	msg = "KEEP MOVING"
	remcols = width - len(msg)
	msg = '='*(remcols//2) + msg + '='*(remcols//2) + '='*(remcols % 2)
	print(msg)
	msg = "Written by Tuomas Laakkonen"
	remcols = width - len(msg)
	msg = '='*(remcols//2) + msg + '='*(remcols//2) + '='*(remcols % 2)
	print(msg,flush=True)
	print("\n"*(height - 6))
	msg = "PRESS ANY KEY TO START"
	remcols = width - len(msg)
	msg = '='*(remcols//2) + msg + '='*(remcols//2) + '='*(remcols % 2)
	print(msg)

def sidetox(side):
	if side == "a":
		return location.x - 1
	elif side == "d":
		return location.x + 1
	else:
		return location.x

def sidetoy(side):
	if side == "w":
		return location.y - 1
	elif side == "s":
		return location.y + 1
	else:
		return location.y

OBSTRUCTINGOBJECTS = ['T','R']

def isnotobstructed(side):
	return not MAP(sidetox(side))(sidetoy(side)) in OBSTRUCTINGOBJECTS

def isonside(side,obj):
	return MAP(sidetox(side))(sidetoy(side)) == obj

def action(side):
	if side == "w":
		...
	elif side == "s":
		...
	elif side == "a":
		...
	elif side == "d":
		...
	if isonside(side,"T"):
		global INVWEIGHT
		if (INVWEIGHT + 4 * WEIGHT["W"]) <= MAXWEIGHT:
			del OBJECTS[(sidetox(side),sidetoy(side))]
			for _ in range(4):
				INVENTORY.append("W")	
			INVWEIGHT += 4 * WEIGHT["W"]
	if isonside(side,"R"):
		if INVWEIGHT + WEIGHT["R"] <= MAXWEIGHT:
			del OBJECTS[(sidetox(side),sidetoy(side))]
			INVENTORY.append("R")
			INVWEIGHT += WEIGHT["R"]

def drop():
	if INVENTORY != [] and not (location.x,location.y) in list(OBJECTS.keys()) and CURINDEX < len(RLE(INVENTORY)):
		OBJECT = RLE(INVENTORY)[CURINDEX][1]
		OBJECTS[(location.x,location.y)] = OBJECT
		INVENTORY.remove(OBJECT)
		global INVWEIGHT
		INVWEIGHT -= WEIGHT[OBJECT]

def pickup():
	if (location.x,location.y) in list(OBJECTS.keys()):
		OBJECT = OBJECTS[(location.x,location.y)]
		global INVWEIGHT
		if INVWEIGHT + WEIGHT[OBJECT] <= MAXWEIGHT:
			INVENTORY.append(OBJECT)
			INVWEIGHT += WEIGHT[OBJECT]
			del OBJECTS[(location.x,location.y)]

def select(num):
	if INVENTORY != [] and num > -1 and num < len(RLE(INVENTORY)):
		global CURINDEX
		CURINDEX = num

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()


(width,height) = os.get_terminal_size()

for _ in range(40):
	OBJECTS[(random.randint(0,width),random.randint(0,height))] = 'T'
	OBJECTS[(random.randint(0,width),random.randint(0,height))] = 'R'

print("\033c")
welcome()
getch()
print("\033c")
frame()
print(flush=True,end="")
while True:
	char = getch()
	if char == '\x1b':
		getch()
		char = '\x1b[' + getch()
	if char == UP:
		if isnotobstructed("w"):
			location.y -= 1
	elif char == DOWN:
		if isnotobstructed("s"):  
			location.y += 1
	elif char == RIGHT:
		if isnotobstructed("d"):
			location.x += 1
	elif char == LEFT:
		if isnotobstructed("a"):
			location.x -= 1
	elif char == "h":
		home.x = location.x
		home.y = location.y
	elif char == "w":
		action("w")
	elif char == "s":
		action("s")
	elif char == "a":
		action("a")
	elif char == "d":
		action("d")
	elif char == "q":
		drop()
	elif char == "e":
		pickup()
	elif char.isnumeric():
		select(int(char) - 1)
	elif char == "z":
		select(CURINDEX - 1)
	elif char == "x":
		select(CURINDEX + 1)
	elif char == "\x03":
		sys.exit(0)
	print("\033c")
	frame()
	print(flush=True,end="")
