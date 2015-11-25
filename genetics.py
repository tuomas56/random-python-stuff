from random import random, randrange
import itertools
from functools import partial
import operator
import brainfuck

class Genome:
	def __init__(self,length,mutation_rate=0.05):
		self.genes = [randrange(8) for _ in range(length)]
		self.length = length
		self.mutation_rate = mutation_rate

	def mutate(self):
		for i in range(self.length):
			if random() < self.mutation_rate:
				mut_type = randrange(3)
				if mut_type == 0:
					self.genes.insert(i,randrange(8))
					*self.genes, _ = self.genes
				elif mut_type == 1:
					del self.genes[i]
					self.genes.append(randrange(8))
				elif mut_type == 2:
					self.genes[i] = randrange(8)

	def crossover(self,other):
		pos = randrange(self.length)
		child1 = Genome(self.length,mutation_rate=self.mutation_rate)
		child2 = Genome(self.length,mutation_rate=self.mutation_rate)
		for i in range(self.length):
			if i < pos:
				child1.genes[i] = self.genes[i]
				child2.genes[i] = other.genes[i]
			else:
				child1.genes[i] = other.genes[i]
				child2.genes[i] = self.genes[i]
		return child1,child2

	def __str__(self):
		return "Genome("+','.join(map(str,self.genes))+")"

class GeneticAlgorithm:
	def __init__(self,fitness_function,crossover_rate=0.8,mutation_rate=0.05,population_size=100,genome_size=100,generations=2000):
		self.crossover_rate, self.mutation_rate, self.population_size, self.genome_size, self.generations = crossover_rate, mutation_rate, population_size, genome_size, generations
		self.fitness_function = fitness_function
		self.population = [Genome(genome_size,mutation_rate=mutation_rate) for _ in range(self.population_size)]

	def go(self):
		for i in itertools.count():
			print(i)
			def roulette_select():
				fitness_table = [self.fitness_function(x)[1] for x in self.population]
				total_fitness = sum(fitness_table)
				fitness_table = [x/total_fitness  if total_fitness else 0 for x in fitness_table]
				fitness_table = list(itertools.accumulate(fitness_table))
				sorted_population = sorted(self.population,key=lambda x: fitness_table[self.population.index(x)])
				cutoff = random()
				try:
					pos = fitness_table.index(next(itertools.dropwhile(lambda x: x < cutoff,fitness_table)))
				except:
					pos = len(fitness_table) - 1
				return sorted_population[pos]
			result = []
			for i in range(0,self.population_size,2):
				parent1 = roulette_select()
				parent2 = roulette_select()
				child1, child2 = parent1.crossover(parent2) if random() < self.crossover_rate else (parent1,parent2)
				child1.mutate()
				child2.mutate()
				result.append(child1)
				result.append(child2)
				target, fitness = self.fitness_function(child1)
				if fitness == target:
					return child1
				target, fitness = self.fitness_function(child2)
				if fitness == target:
					return child2
			self.population = result
			print(max([self.fitness_function(x)[1] for x in self.population]))

def fitness_function(func):
	def wrapper(genome):
		output = ""
		def on_out(value):
			output += chr(value)
		try:
			code = ''.join('><+-.,[]'[x] for x in genome.genes)
			bf = brainfuck.Brainfuck(code)
			context = brainfuck.Context(output=on_out,input=lambda: ord('a'))
			bf.execute(context=context)
		except:
			pass
		if len(output):
			print(' '.join(map(ord,output)))
		return func(output)
	return wrapper

def string_fitness(target):
	@fitness_function
	def wrapper(output):
		return 256*len(target), sum(256 - abs(ord(output[i]) - ord(target[i])) for i in range(min(len(target),len(output))))
	return wrapper

ga = GeneticAlgorithm(string_fitness("hi"))
print(ga.go())

