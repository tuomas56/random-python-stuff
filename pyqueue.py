#Queue class.
#self.elems contains queue elements
#elems initializer converted to list on construction so
#don't attempt to queue an infinite iterator!
#Iterating through a Queue will dequeue the elements it yields!
#If you wish to iterate through a queue non-destructively iterate
#through Queue.elems.
class Queue:
	def __init__(self,elems=[]):
		self.elems = list(elems)

	def enqueue(self,item):
		self.elems.append(item)

	def dequeue(self):
		return self.elems.pop(0)

	def __len__(self):
		return len(self.elems)

	def __iter__(self):
		return self

	def __next__(self):
		if len(self.elems):
			return self.dequeue()
		else:
			raise StopIteration

#An example of using Queues.
#This is a rather elegant implementation of cycle from itertools
#using Queues. It requires less memory than the standard cycle implementation
#but requires that iters is a finite iterator (preferably a list).
def cycle(iters):
	q = Queue(iters)
	for x in q:
		q.enqueue(x)
		yield x