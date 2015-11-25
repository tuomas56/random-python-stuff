class DoubleLinkedNode:
	def __init__(self, value, parent=None, child=None):
		self.value = value
		self.parent = parent
		self.child = child

	def append(self, value):
		if self.child is None:
			self.child = DoubleLinkedNode(value, self)
		else:
			self.child.append(value)

	def pop(self):
		if self.child is None and self.parent is None:
			return self.value
		elif self.child is None:
			self.parent.child = None
			return self.value
		return self.child.pop()

	def delete(self, value=None):
		if value is None and self.parent is None:
			self.child.parent = None
			return self.child
		elif value is None and self.child is None:
			self.parent.child = None
			return self.parent
		elif value is None:
			self.parent.child = self.child
			self.child.parent = self.parent
			return self.child
		elif self.value == value and self.parent is None:
			return True
		elif self.value == value and self.child is None:
			self.parent.child = None
			return True
		elif self.value == value:
			self.parent.child = self.child
			self.child.parent = self.parent
			return True
		elif self.child is not None:
			return self.child.delete(value)
		return False

	def __contains__(self, value):
		if self.value == value:
			return True
		elif self.child is not None:
			return value in self.child
		return False

	def __str__(self):
		if self.child is not None:
			return "%s -> %s" % (self.value, self.child)
		return str(self.value)

	def __iter__(self):
		yield self.value
		if self.child is None:
			raise StopIteration
		yield from self.child