def dict2tplist(dict):
	return zip(list(dict.keys()),list(dict.values()))

class Node:
	def __init__(self,value="",children={}):
		self.value = value
		self.children = children

	def __str__(self):
		return ("Node - Value:",self.value,"Children:",' '.join([key + "|" + str(value) for key,value in dict2tplist(self.children)]))

def find(node,key):
	for char in key:
		if char not in node.children: return None
		else: node = node.children.get(char)

def insert(node,key,value):
	i = 0
	n = len(key)
	while i < n:
		if node.children.get(key[i],False):
			node = node.children.get(key[i])
			i += 1
		else: break

	while i < n:
		node.children[key[i]] = Node()
		node = node.children.get(key[i])
		i += 1

	node.value = value

root = Node()
insert(root,"hello",3)
