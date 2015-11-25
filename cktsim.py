pi = 3.141592653

def ohms_law(v,i,r):
	if v is None:
		return i * r
	elif i is None:
		return v / r
	elif r is None:
		return v / i

class Value:
	def __init__(self, v, i):
		self.v = v
		self.i = i

	def __str__(self):
		return 'Value(V = %s Volts, I = %s Amps)' % (self.v, self.i)

	def __add__(self, other):
		return Value(self.v + other.v, self.i + other.i)

class Component:
	def __init__(self, child):
		self.child = child

	def get_resistance(self, v):
		return self.child.get_resistance(v)

	def get_capacitance(self):
		return self.child.get_capacitance()

	def trace(self):
		print(self.result)
		self.child.trace()

	def step(self, s_in):
		self.result = s_in
		self.child.step(s_in)

class Resistor(Component):
	def __init__(self, resistance, child):
		self.r = resistance
		self.child = child

	def get_resistance(self, v):
		return self.r  + self.child.get_resistance(v)

	def step(self, s_in):
		new_v = s_in.v  - ohms_law(None, s_in.i, self.r)
		self.result = Value(new_v, s_in.i)
		self.child.step(self.result)

class Source(Component):
	def __init__(self, voltage, child):
		self.v = voltage
		self.child = child

	def step(self):
		self.result = Value(self.v, ohms_law(self.v, None, self.get_resistance(self.v)))
		self.child.step(self.result)

class Split(Component):
	def __init__(self, *children):
		self.children = children
	
	def step(self, s_in):
		resistances = [child.get_resistance(s_in.v) for child in self.children]
		r_total = sum(resistances)
		values = [Value(s_in.v, s_in.i * resistances[i] / r_total) for i,child in enumerate(self.children)]
		for i, (value, child) in enumerate(zip(values, self.children)):
			child.step(value)
			values[i] = child.result
		self.result = sum(values, Value(0,0))

	def get_resistance(self, v):
		return sum(child.get_resistance(v) for child in self.children)

	def trace(self):
		for child in self.children:
			print('Branch')
			child.trace()
		print(self.result)

class LED(Resistor):
	efficacy = 150

	def __init__(self, rating, child):
		self.r = 1/rating
		self.child = child
		
	def trace(self):
		print(self.result, 'Luminosity:', (LED.efficacy * self.p)/(4*pi), 'Candela')
		self.child.trace()

	def step(self, s_in):
		new_v = s_in.v  - ohms_law(None, s_in.i, self.r)
		self.result = Value(new_v, s_in.i)
		self.p = s_in.v**2 / self.get_resistance(s_in.v)
		self.child.step(self.result)

class Sink(Component):
	def __init__(self):
		pass

	def get_resistance(self, v):
		return 0

	def get_capacitance(self):
		return 0

	def trace(self):
		print(self.result)

	def step(self, s_in):
		self.result = s_in

class Join(Sink):
	pass

component = Source(12, 
				Split(
					LED(0.01,
						Resistor(10, Join())),
					Resistor(10, Join())))
component.step()
component.trace()
