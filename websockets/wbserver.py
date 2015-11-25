from contextlib import contextmanager
from event import EventManager

class WebSocketServer(EventManager):
	def __init__(self):
		super().__init__()
		self._register('connect')
		self._register('disconnect')
		self.users = []

		@self.on('connect')
		def on_connect(self, user):
			self.users.append(user)

		@self.on('disconnect')
		def on_disconnect(self, user):
			self.users.remove(user)

	@contextmanager
	def connect(self, user):
		wuser = WebSocketClient(user, server)
		self.connected_event.trigger(wuser)
		yield wuser
		wuser.start()
		self.disconnected_event.trigger(wuser)

class WebSocketClient(EventManager):
	def __init__(self, websocket):
		super().__init__()
		self.ws = websocket
		self._register('data')

	def start(self):
		while True:
			msg = self.ws.receive()
			if msg is not None:
				self.trigger('data', msg)
			else:
				break

	def send(self, message):
		self.ws.send(message)