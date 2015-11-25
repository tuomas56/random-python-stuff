from collections import namedtuple
from operator import methodgetter
from functools import partial

class Sequent(namedtuple("Sequent", "antecedents consequents")):
	def infer(self, env):
		if Conjunction(*self.antecedents).prove(env):
			env.proven(Disjunction(*self.consequents))

class Conjunction:
	def __init__(self, *terms):
		self.terms = terms

	def prove(self, env):
		return all(map(partial(methodgetter("prove"), env=env), self.terms))

class Disjunction:
	def __init__(self, *terms):
		self.terms = terms

	def prove(self, env):
		return any(map(partial(methodgetter("prove"), env=env), self.terms))

class Environment:
	def __init__(self, facts):
		self.facts = facts

	def proven(self, term):
		self.facts.append(term)

	def prove(self, term):
		return term in self.facts