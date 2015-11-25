from collections import defaultdict

class MachineHalted(RuntimeError):
	def __str__(self):
		return "Machine Halted!"

class Symbol:
	def __init__(self,name):
		self.name = name

	def __str__(self):
		return self.name

class State:
	def __init__(self,name):
		self.name = name

	def __str__(self):
		return self.name

L = Symbol("L")
R = Symbol("R")

class TuringMachine:
	def __init__(self,states,alphabet,blank,input,transition,initial,accepting):
		self._states = states
		self._alphabet = alphabet
		self._black = blank
		self._input = input
		self._transition = transition
		self._initial = initial
		self._accepting = accepting
		self._pos = 0
		self.tape = defaultdict(lambda:blank)
		self.state = initial

	def step(self):
		self.state, self.tape[self._pos], shift = self._transition(self.state,self.tape[self._pos])
		if shift == L:
			self._pos -= 1
		elif shift == R:
			self._pos += 1
		else:
			raise RuntimeError("Shift %s undefined! Should be L or R." % shift)
		if self.state in self._accepting:
			raise MachineHalted



b, c, e, f = map(State,"bcef")
p0, p1, blank = map(Symbol,"01 ")
def transition_original(state, symbol):
	if state == b and symbol == blank:
		return c, p0, R
	elif state == c and symbol == blank:
		return e, blank, R
	elif state == e and symbol == blank:
		return f, p1, R
	elif state == f and symbol == blank:
		return b, blank, R

machine_original = TuringMachine([b,c,e,f],[p0,p1,blank],blank,[p0,p1,blank],transition_original,b,[])

A, B, C, HALT = map(State,["A","B","C","HALT"])
P0, P1 = map(Symbol,"01")
def transition_beaver(state,symbol):
	if state == A and symbol == P0:
		return B, P1, R
	elif state == A and symbol == P1:
		return C, P1, L
	elif state == B and symbol == P0:
		return A, P1, L
	elif state == B and symbol == P1:
		return B, P1, R
	elif state == C and symbol == P0:
		return B, P1, L
	elif state == C and symbol == P1:
		return HALT, P1, R

machine_beaver = TuringMachine([A, B, C, HALT],[P0,P1],P0,[P0,P1],transition_beaver,A,[HALT])

while True:
	try:
		print(machine_beaver.state,''.join(map(str,machine_beaver.tape.values())))
		machine_beaver.step()
	except MachineHalted as e:
		print(machine_beaver.state,''.join(map(str,machine_beaver.tape.values())))
		print(e)
		break