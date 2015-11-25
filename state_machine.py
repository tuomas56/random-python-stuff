class State:
	def __init__(self):
		self._events = {}

	def on(self,event,func):
		self._events[event].append(func)

	def trigger(self,event,*args):
		return [x(*args) for x in self._events]

	def add_event(self,name):
		self._events[name] = []

	def hook(self,event):
		def wrapper(func):
			self.on(event,func)
		return wrapper


class StateMachine:
	def __init__(self):
		self._states = {}

	def add_state(self,name,state):
		self._states[name] = state

	def get_state(self,name):
		return self._states[name]

	def start(self,initial):
		self.current = initial

	def next_state(self,func):
		next_state = func(self.current)
		self.get_state(self.current).trigger('exit',next_state)
		self.get_state(next_state).trigger('enter',self.current)
		self.current = next_state

class CallableDict(dict):
	def __call__(self,arg):
		return self[arg]

ezs = StateMachine()

ezs.add_state('even',State())
ezs.add_state('odd',State())
string = input()
ezs.start('even')
for x in string:
	ezs.next_state(CallableDict({
		'even': {
				True: 'even',
				False: 'odd'
			}[x == "1"],
		'odd': {
				True: 'odd',
				False: 'even'
			}[x == "1"]
		}))

print("Yes" if ezs.current == 'even' else "No")