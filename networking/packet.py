from .util import pack_varint, unpack_varint

class Packet:
	_packets = {}
	_reverse_packets = {}
	_cur_id = 0

	def __init__(self) -> None:
		self.id = Packet.get_id_by_packet(self.__class__)

	def _serialize(self) -> None:
		pass

	@staticmethod
	def _deserialize(input: bytes):
		pass

	def _to_bytes(self) -> bytes:
		"""Serialize to bytes. Normally, subclasses should override Packet#_serialize."""
		x = self._serialize()
		return pack_varint(self.id) + pack_varint(len(x)) + x

	@staticmethod
	def _from_bytes(input: bytes) -> None:
		"""Deserialize from bytes. Subclasses should override Packet._deserialize."""
		id, payload = unpack_varint(input)
		length, payload = unpack_varint(payload)
		return Packet.get_packet_by_id(id)._deserialize(payload)

	@staticmethod
	def _from_stream(input: bytes) -> None:
		"""Deserialize from stream."""
		id, input = unpack_varint(input, stream=True)
		length, input = unpack_varint(input, stream=True)
		payload = input.read(length)
		return Packet.get_packet_by_id(id)._deserialize(payload)

	@staticmethod
	def register_packet(cls):
		Packet._packets[Packet._cur_id] = cls
		Packet._reverse_packets[cls] = Packet._cur_id
		Packet._cur_id += 1

	@staticmethod
	def get_packet_by_id(id):
		return Packet._packets[id]

	@staticmethod
	def get_id_by_packet(cls):
		return Packet._reverse_packets[cls]