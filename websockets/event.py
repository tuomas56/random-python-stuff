from multiprocessing import Process

class Event:
	def __init__(self):
		self.handlers = []

	def __call__(self, f=None, async=False):
		def _evt(f1):
			f1 = Handler(f1, async)
			self.handlers.append(f1)
			return f1
		if f is None:
			return _evt
		else:
			return _evt(f)

	def __iadd__(self, other):
		if isinstance(other, Handler):
			self.handlers.append(other)
		elif callable(other):
			self.handlers.append(Handler(other, True))
		else:
			raise TypeError("Cannot add %s to Event." % other.__class__.__name__)
		return self

	def trigger(self, *args):
		for handler in self.handlers:
			handler(*args)

class Handler:
	def __init__(self, f, async):
		self.f = f
		self.async = async

	def __call__(self, *args):
		if self.async:
			Process(target=self.f, args=args).start()
		else:
			self.f(*args)

def async(f):
	return Handler(f, async=True)

class EventManager:
	def __init__(self):
		self.events = {}

	def _register(self, name):
		self.events[name] = Event()

	def trigger(self, name, data=None):
		self.events[name].trigger(data)

	def on(self, name):
		def _on(func):
			self.events[name] += func
			return func
		return _on