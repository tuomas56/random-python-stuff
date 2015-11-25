import sys
import os

class Tape:
	def __init__(self):
		self.pointer = 0
		self.tape = [0]

	def right(self):
		self.pointer += 1
		if self.pointer == len(self.tape):
			self.tape.append(0)

	def left(self):
		if self.pointer > 0:
			self.pointer -= 1

	def jmp(self, pos):
		self.pointer = pos
		while self.pointer >= len(self.tape):
			self.tape.append(0)

	def get(self):
		return self.tape[self.pointer]

	def set(self, value):
		self.tape[self.pointer] = value

	def inc(self):
		self.tape[self.pointer] += 1

	def dec(self):
		if self.tape[self.pointer] > 0:
			self.tape[self.pointer] -= 1

RIGHT = 1
LEFT = 2
INC = 3
DEC = 4
IN = 5
OUT = 6
START = 7
END = 8

def parse(source):
	ast = []
	cur = 0
	bc_map = {}
	while len(source):
		token = source[0]
		cur += 1
		if token == '>':
			ast.append(RIGHT)
			source = source[1:]
		elif token == '<':
			ast.append(LEFT)
			source = source[1:]
		elif token == '+':
			ast.append(INC)
			source = source[1:]
		elif token == '-':
			ast.append(DEC)
			source = source[1:]
		elif token == '.':
			ast.append(OUT)
			source = source[1:]
		elif token == ',':
			ast.append(IN)
			source = source[1:]
		elif token == '[':
			source = source[1:]
			ls = 0
			depth = 1
			while True:
				token = source[ls]
				if token == ']':
					depth -= 1
					if depth == 0:
						break
				elif token == '[':
					depth += 1
				ls += 1
			bc_map[cur] = cur + ls
			bc_map[cur + ls] = cur
			ast.append(START)
		elif token == ']':
			ast.append(END)
			source = source[1:]
	return ast, bc_map

def exec_ast(ast, tape):
	cur = 0
	while cur < len(ast[0]):
		symbol = ast[0][cur]
		if isinstance(symbol, list):
			while tape.get():
				exec_ast(symbol, tape)
		elif symbol == RIGHT:
			tape.right()
		elif symbol == LEFT:
			tape.left()
		elif symbol == INC:
			tape.inc()
		elif symbol == DEC:
			tape.dec()
		elif symbol == IN:
			tape.set(ord(os.read(0,1)[0]))
		elif symbol == OUT:
			print(chr(tape.get()))
		elif symbol == START and not tape.get():
			cur = ast[1][cur] - 1
		elif symbol == END and tape.get():
			cur = ast[1][cur] - 1
		cur += 1

def exec_bf(source):
	exec_ast(parse(source), Tape())

def entry_point(argv):
	try:
		filename = argv[1]
	except:
		return 0
	fd = os.open(filename, os.O_RDONLY, 0777)
	source = ""
	while True:
		read = os.read(fd, 4096)
		if len(read) == 0:
			break
		source += read
	os.close(fd)
	exec_bf(source)
	return 0

def target(*args):
	return entry_point, None

if __name__ == "__main__":
	entry_point(sys.argv)
