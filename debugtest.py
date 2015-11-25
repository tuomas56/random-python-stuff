import re

class LObject:
	def __init__(self):
		self.slots = {}
		self.slots['setslot'] = self.setsloti
		self.slots['getslot'] = self.getslot
		self.slots['setslot'] = LFunctionObject(self,'setslot')
		self.slots['getslot'] = LFunctionObject(self,'getslot')
		self.setslot('repr',self.repr)
		self.setslot('repr',LFunctionObject(self,'repr'))

	def call(self):
		return self

	def repr(self):
		return self

	def setslot(self,name,value):
		self.slots[name] = value

	def setsloti(self,name,value):
		self.slots[name.repr()] = value
		print(self.slots)

	def getslot(self,name):
		return self.slots[name]

class LFunctionObject(LObject):
	def __init__(self,parent,fname):
		self.slots = {}
		self.f = parent.getslot(fname)

	def call(self,*args):
		return self.f(*args)

class LStringLiteral(LObject):
	def __init__(self,s):
		super(LStringLiteral,self).__init__()
		self.s = s
		self.setslot('print',self.put)
		self.setslot('print',LFunctionObject(self,'print'))
		self.setslot('add',self.add)
		self.setslot('substr',self.substr)
		self.setslot('add',LFunctionObject(self,'add'))
		self.setslot('substr',LFunctionObject(self,'substr'))


	def repr(self):
		return self.s

	def put(self):
		print(self.s)

	def add(self,other):
		return self.s + other.s

	def substr(self,start,end):
		return self.s[start.v:end.v]

class LNumericLiteral(LObject):
	def __init__(self,v):
		super(LNumericLiteral,self).__init__()
		self.v = v
		self.setslot('add',self.add)
		self.setslot('sub',self.sub)
		self.setslot('mul',self.mul)
		self.setslot('div',self.div)
		self.setslot('pow',self.pow)
		self.setslot('put',self.put)
		self.setslot('add',LFunctionObject(self,'add'))
		self.setslot('sub',LFunctionObject(self,'sub'))
		self.setslot('mul',LFunctionObject(self,'mul'))
		self.setslot('div',LFunctionObject(self,'div'))
		self.setslot('pow',LFunctionObject(self,'pow'))
		self.setslot('put',LFunctionObject(self,'put'))

	def repr(self):
		return str(self.v)

	def put(self):
		print(str(self.v))

	def add(self,other):
		return self.v + other.v

	def sub(self,other):
		return self.v - other.v

	def mul(self,other):
		return self.v * other.v

	def div(self,other):
		return self.v / other.v

	def pow(self,other):
		return self.v ** other.v

class LRootObject(LObject):
	def __init__(self):
		super(LRootObject,self).__init__()
		self.setslot('root',self)
		self.setslot('print',self.puts)
		self.setslot('print',LFunctionObject(self,'print'))
		self.setslot('input',self.gets)
		self.setslot('input',LFunctionObject(self,'input'))

	def puts(self,*args):
		for x in args:
			print(x.repr())

	def gets(self,*args):
		return input(*args)

def parseargs(root,s):
	def eat(l=1):
		nonlocal s
		c = s[:l]
		s = s[l:]
		return c
	def eatif(a):
		nonlocal s
		if s[:len(a)] == a:
			s = s[len(a):]
			return True
		return False
	ast = []
	node = ""
	while len(s) > 0:
		if eatif('"'):
			cs = ""
			while s[0] != '"':
				cs += eat()
			eat()
			node = LStringLiteral(s)
		elif eatif("'"):
			cs = ""
			while s[0] != "'":
				cs += eat()
			eat()
			node = LStringLiteral(s)
		elif eatif(","):
			ast.append(parse(root,node))
			node = ""
		elif s[0].isnumeric():
			cs = ""
			while s[0].isnumeric():
				cs += eat()
			return LNumericLiteral(float(cs))
		else:
			node += eat()
	if node != "":
		ast.append(parse(root,node))
	print(ast)
	return ast


def parse(root,s):
	if not isinstance(s,str):
		return s
	s = s.split(" ")
	if len(s) == 1:
		s = s[0]
		if "(" in s and ")" in s:
			a = parseargs(root,s.split("(")[1][:-1])
			r = s.split("(")[0]
			r = root.getslot(r)
			return r.call(*a)
		else:
			return root.getslot(s)
	else:
		return parse(parse(root,s[0]),' '.join(s[1:]))

_root = LRootObject()
while True:
	parse(_root,input(">>> "))