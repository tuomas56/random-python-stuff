import random

def shuffle(ls):
	result = [0 for _ in range(len(ls))]
	ais = range(len(ls)) #available indexes
	for i in range(len(ls)):
		r = randfrom(ais)
		ais.remove(r)
		result[i] = ls[r]
	return result

def randfrom(ls):
	return ls[random.randint(0,len(ls)-1)]

def issorted(ls):
	return all(map(lambda i: ls[i] < ls[i+1],range(len(ls)-1)))

