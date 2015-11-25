from itertools import islice, tee
from collections import defaultdict
from operator import itemgetter
import random
from nltk.corpus import gutenberg
import pickle
import sys

def ngrams(ls, n):	
	return zip(*(islice(seq, index, None) for index, seq in enumerate(tee(ls, n))))

def weighted_choice(ls):
	ls = normalize(ls)
	v = 1/min(ls, key=itemgetter(1))[1]
	a = []
	for el in ls:
		a += [el[0]]*int(round(el[1]*v))
	return random.choice(a)

def normalize(ls):
	ls = list(ls)
	t = sum(map(itemgetter(1), ls))
	names = list(map(itemgetter(0), ls))
	x = [(name, names.count(name)*prob/t) for name, prob in list(set(ls))]
	return x

def undict(d):
	return zip(list(d.keys()), list(d.values()))

def from_data(ls, order, debug=False):
	c = Chain(list(set(ls)), order)
	l = len(ls)
	for n in range(1, order + 1):
		for i, (*history, el) in enumerate(ngrams(ls, n)):
			if debug:
				print('\x1B[K\r'+'[%s/%s][<' % (n, order + 1) + ('=')*(10*i//l) + '>]', end='')
			c.add_probability(('',)*(order-n-1) + tuple(history), el, 1)
	l = len(c.states)
	for i, el in enumerate(c.states):
		if debug:
			print('\r[%s/%s]' % (order + 1, order + 1) + '[<'+('=')*(10*i//l)+'>]', end='')
		c.add_starting_probability(el, 1)
	print()
	return c

class Chain:
	def __init__(self, states, order):
		self.states = states
		self.matrix = defaultdict(lambda: [])
		self.starting = defaultdict(lambda: 0)
		self.order = order

	def add_probability(self, history, to, prob):
		self.matrix[history].append((to, prob))

	def add_starting_probability(self, state, prob):
		self.starting[state] = prob

	def move(self, history):
		return weighted_choice(self.matrix[history])

	def normalize(self):
		for key, value in self.matrix.items():
			self.matrix[key] = normalize(value)

	def walk(self, n, start=None):
		if start is None:
			start = weighted_choice(undict(self.starting))
		history = ('',)*(self.order-2) + (start,)
		path = []
		for _ in range(n):
			s = 0
			while True:
				try:
					history += (self.move(history[s:]),)
					break
				except:
					s += 1
			path.append(history[-1])
			history = history[1:]
		return path

	def __str__(self):
		s = ""
		for key, values in self.matrix.items():
			s += "%s\n" % (key if isinstance(key, str) else ', '.join(key))
			for to, prob in values:
				s += "    %s %s\n" % (to, prob)
		return s

	def __getstate__(self):
		return self.order, self.states, dict(self.matrix), dict(self.starting)

	def __setstate__(self, state):
		self.order, self.states, self.matrix, self.starting = state

c = from_data(gutenberg.words(sys.argv[1]), int(sys.argv[2]), debug=True)
#pickle.dump(c, open('markov.pyp', 'wb'))
print(' '.join(c.walk(100)))