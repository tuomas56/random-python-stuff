def unzip(dict):
	return zip(list(dict.keys()),list(dict.values()))

class Node:
	def __init__(self,children={}):
		self.children = children

	def append(self,child,distance):
		if not child in list(self.children.keys()):
			self.children[child] = distance

	def remove(self,child):
		if child in list(self.children.keys()):
			del self.children[child]

	def shortestPath(self):
		print(list(self.children.keys()))
		if len(list(self.children.keys())) > 0:
			x = min(unzip(self.children),key=lambda c: sum(c[0].shortestPath()) + c[1])[0].shortestPath() + [self]
			return x
		else:
			return [self]

root = Node()
first = Node()
firstfirst = Node()
firstsecond = Node()
second = Node()
secondfirst = Node()
secondsecond = Node()
first.append(firstfirst,8)
first.append(firstsecond,5)
second.append(secondfirst,6)
second.append(secondsecond,4)
root.append(first,6)
root.append(second,7)

print(root.shortestPath())
