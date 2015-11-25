def t(test):
	def i(true):
		def j(false):
			return {True: true,False: false}[bool(test)];
		return j;
	return i;


print(t(1 == 2)("Hi")("Hello"))