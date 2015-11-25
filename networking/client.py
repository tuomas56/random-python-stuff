import socket
from .packet import Packet
from .event import Event
from multiprocessing import Process
from .util import wait_until

class PacketClient:
	def __init__(self, ip: str, port: int) -> None:
		self._address = (ip, port)
		self._events = {}
		self._all = Event()

	def connect(self) -> None:
		self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._sock.connect(self._address)
		self._is_open = True
		
	def start(self) -> None:
		Process(target=self._mainloop).start()

	def _mainloop(self) -> None:
		while self._open():
			try:
				packet = Packet._from_stream(self._sock.makefile())
				self._handle(packet)
			except:
				self._is_open = False

	def _handle(self, packet):
		packet_class = Packet.get_packet_by_id(packet)
		if packet_class in self._events:
			self._events[packet_class].trigger(packet)
		self._all.trigger(packet)

	def _open(self) -> bool:
		return self._is_open

	def stop(self) -> None:
		self._is_open = False

	def send(self, p: Packet) -> None:
		self._sock.send(p._to_bytes())

	def handler(self, f, ptype=None) -> None:
		if ptype is None and issubclass(f, Packet): #as a decorator
			def _add_handler(f2):
				if f not in self._events:
					self._events[f] = Event()
				self._events[f] += f2
			return _add_handler

		if ptype is not None:
			if ptype not in self._events:
				self._events[ptype] = Event()
			self._events[ptype] += f
		else:
			self._all += f

	def remove_handler(handler) -> None:
		for ptype in self._events.keys():
			if handler in self._events[ptype]:
				self._events[ptype].handlers.remove(handler)
		self._all.handlers.remove(handler)

	def recv(self, ptype=None) -> Packet:
		p = None
		def _handler(packet):
			p = packet
		self.handler(_handler, ptype)
		wait_until(lambda: p is not None)
		self.remove_handler(_handler)
		return p

