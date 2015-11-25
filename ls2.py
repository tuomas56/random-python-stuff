class List(list):
	def filter_im(self,exp):
		self = filter(exp,self)
		return self

	def filter(self,exp):
		return filter(exp,self)

	def map_im(self,exp):
		self = map(exp,self)
		return self

	def map(self,exp):
		return map(exp,self)