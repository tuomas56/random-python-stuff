class Perceptron:
	def __init__(self, n_in, bias, learning_rate):
		self.weights = [bias] + [0]*n_in
		self.learning_rate = learning_rate

	def train(self, n_in, desired):
		actual = self.calculate(n_in)
		n_in = [desired] + n_in
		for i, w in enumerate(self.weights):
			self.weights[i] = w + self.learning_rate * (desired - actual) * n_in[i]

	def calculate(self, n_in):
		return sum([self.weights[i]*x for i, x in enumerate([0] + n_in)])

	def classify(self, n_in):
		return round(self.calculate(n_in))

p_and = Perceptron(2, 0, 0.5)

for _ in range(100):
	p_and.train([0, 0], 0)
	p_and.train([0, 1], 1)
	p_and.train([1, 0], 1)
	p_and.train([1, 1], 1)
	print(p_and.weights)

print(p_and.classify([0, 1]))

