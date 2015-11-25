class PickleSlots:
	def __reduce__(self):
		if super(self.__class__,self).__class__ != PickleSlots:
			ret = list(super(self.__class__,self).__reduce__())
			l = [ret]
		else:
			l = []
		l.append(self.__dict__)
		return tuple(l)

	def __setstate__(self, l):
		
		self.__dict__.update(l[1])
		if super(self.__class__,self).__class__ != PickleSlots:
			return super(self.__class__,self).__setstate__(self, l[0])
		else:
			return self
