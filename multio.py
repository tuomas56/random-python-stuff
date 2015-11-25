import selectors
import sys
from multiprocessing import Process

class AsyncIO:
	def __init__(self,file):
		self._selector = selectors.DefaultSelector()
		self._read_handlers = {}
		self._write_queue = []
		self._selector.register(file,selectors.EVENT_READ + selectors.EVENT_WRITE)
		self._running = False
		self._read_queue = []

	def write(self,data):
		self._write_queue.append(data)

	def read(self):
		if len(self._read_queue):
			return self._read_queue.pop(0)

	def run_forever(self):
		self._running = True
		while self._running:
			for key,mask in self._selector.select(0):
				if mask == selectors.EVENT_READ:
					self._read_queue.append(key.fileobj.readline())
				elif mask == selectors.EVENT_WRITE:
					if len(self._write_queue):
						key.fileobj.write(self._write_queue.pop(0))

	def stop(self):
		self._running = False

terminal = AsyncIO(sys.stdin)
def write_thread():
	while True:
		terminal.write("Hello World!")
Process(target=write_thread).start()
Process(target=terminal.run_forever()).start()
