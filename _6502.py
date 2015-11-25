import re
from collections import namedtuple
import string
from enum import Enum

class ParserError(Exception):
	def __init__(self,line,message):
		self.line = line
		self.message = message

	def __str__(self):
		return "[Line %s] Syntax Error - %s" % (self.line, self.message)

class CompilerError(ParserError):
	def __str__(self):
		return "[Line %s] Compile Error - %s" % (self.line, self.message)


AddressMode = Enum('AddressMode','absolute zero_page label indirect_before indirect_after accumulator')

Literal = namedtuple('Literal','value')
Address = namedtuple('Address','value register mode')
Instruction = namedtuple('Instruction','name argument')
Label = namedtuple('Label','name line')

asmre = re.compile('(?P<opcode>[A-Z]+)(?: (?P<literal>#)?(?P<hex>\$)?(?P<argument>.*))?')
labelre = re.compile('(?P<name>[a-z]+):')
def parse(source):
	for i,line in enumerate(filter(lambda x: x.strip() != "",source.split("\n"))):
		line = line.strip()
		match = asmre.match(line)
		if match is None:
			match = labelre.match(line)
			if match is None:
				raise ParserError(i + 1, "Invalid syntax.")
			else:
				yield Label(match.group('name'),i)
		elif match.group('argument') == "":
			raise ParserError(i + 1, "Invalid syntax. Perhaps you put your literal and hex markers backwards.")
		elif match.group('argument') is not None:
			if match.group('literal') is not None:
				if match.group('hex') is not None:
					try:
						yield Instruction(match.group('opcode'), Literal(int(match.group('argument'),16)))
					except:
						raise ParserError(i + 1, "Malformed literal.")
				else:
					try:
						yield Instruction(match.group('opcode'), Literal(int(match.group('argument'),10)))
					except:
						raise ParserError(i + 1, "Malformed literal.")
			else:
				if match.group('argument') == "A":
					yield Instruction(match.group('opcode'), Address(0,None,AddressMode.accumulator))
				elif match.group('hex') is None and not match.group('argument').startswith('('):
					yield Instruction(match.group('opcode'), parseLabelAddress(match.group('argument'),i + 1))
				elif not match.group('argument').startswith('('):
					yield Instruction(match.group('opcode'), parseNumericAddress(match.group('argument'),i + 1))
				else:
					yield Instruction(match.group('opcode'), parseIndirectAddress(match.group('argument'),i + 1))
		else:
			yield Instruction(match.group('opcode'), None)

numericaddressre = re.compile('(?P<zero>[0-9a-fA-F]{2})(?P<absolute>[0-9a-fA-F]{2})?(?P<register>\,(?:X|Y))?')
def parseNumericAddress(address,line):
	match = numericaddressre.match(address)
	if match is None:
		raise ParserError(line,"Malformed address.")
	if match.group('register') is not None:
		register = match.group('register')[1:]
	else:
		register = None
	try:
		if match.group('absolute') is not None:
			address = int(match.group('zero') + match.group('absolute'), 16)
			absolute = True
		else:
			address = int(match.group('zero'), 16)
			absolute = False
	except:
		raise ParserError(line,"Malformed address.")

	return Address(address, register, AddressMode.absolute if absolute else AddressMode.zero_page)

def parseLabelAddress(address,line):
	if not all(x in string.ascii_letters + "_" for x in address):
		raise ParserError(line,"Malformed label address.")
	else:
		return Address(address,None,AddressMode.label)

indirectaddressre = re.compile('\((?P<address>.*?)(?P<before>,(?:X|Y))?\)(?P<after>,(?:X|Y))?')
def parseIndirectAddress(address,line):
	match = indirectaddressre.match(address)
	if match is None:
		raise ParserError(line,"Malformed address.")
	if match.group('before') is not None and match.group('after') is not None:
		raise ParserError(line,"Malformed address. Can't add registers both before and after dereferencing.")
	if match.group('before') is not None:
		address = match.group('address')
		try:
			if address.startswith('$'):
				address = int(match.group('address'),16)
			else:
				address = parseLabelAddress(address).address
		except:
			raise ParserError(line,"Malformed address.")
		before = match.group('before')[1:]
		return Address(address, before, AddressMode.indirect_before)
	elif match.group('after') is not None:
		address = match.group('address')
		try:
			if address.startswith('$'):
				address = int(match.group('address'),16)
			else:
				address = parseLabelAddress(address).address
		except:
			raise ParserError(line,"Malformed address.")
		after = match.group('after')[1:]
		return Address(address, after, AddressMode.indirect_after)
	else:
		try:
			if address.startswith('$'):
				address = int(match.group('address'),16)
			else:
				address = parseLabelAddress(address).address
		except:
			raise ParserError(line,"Malformed address.")
		return Address(address, None, AddressMode.indirect_before)


#			imp,a,imm,zp,zpx,zpy,rel,abs,absx,absy,ind,indx,indy
OPCODES = {
	"ADC": (None,None,0x69,0x65,0x75,None,None,0x6d,0x7d,0x79,None,0x61,0x71),
	"AND": (None,None,0x29,0x25,0x35,None,None,0x2d,0x3d,0x39,None,0x21,0x31),
	"ASL": (None,0x0a,None,0x06,0x16,None,None,0x0e,0x1e,None,None,None,None),
	"BCC": (None,None,None,None,None,None,0x90,None,None,None,None,None,None),
	"BCS": (None,None,None,None,None,None,0xb0,None,None,None,None,None,None),
	"BEQ": (None,None,None,None,None,None,0xf0,None,None,None,None,None,None),
	"BIT": (None,None,None,0x24,None,None,None,0x2c,None,None,None,None,None),
	"BMI": (None,None,None,None,None,None,0x30,None,None,None,None,None,None),
	"BNE": (None,None,None,None,None,None,0xb0,None,None,None,None,None,None),
	"BPL": (None,None,None,None,None,None,0x10,None,None,None,None,None,None),
	"BRK": (0x00,None,None,None,None,None,None,None,None,None,None,None,None),
	"BVC": (None,None,None,None,None,None,0x50,None,None,None,None,None,None),
	"BVS": (None,None,None,None,None,None,0x70,None,None,None,None,None,None),
	"CLC": (0x18,None,None,None,None,None,None,None,None,None,None,None,None),
	"CLD": (0xd8,None,None,None,None,None,None,None,None,None,None,None,None),
	"CLI": (0x58,None,None,None,None,None,None,None,None,None,None,None,None),
	"CLV": (0xb8,None,None,None,None,None,None,None,None,None,None,None,None),
	"CMP": (None,None,0xc9,0xc5,0xd5,None,None,0xcd,0xdd,0xd9,None,0xc1,0xd1),
	"CPX": (None,None,0xe0,0xe4,None,None,None,0xec,None,None,None,None,None),
	"CPY": (None,None,0xc0,0xc4,None,None,None,0xcc,None,None,None,None,None),
	"DEC": (None,None,None,0xc6,0xd6,None,None,0xce,0xde,None,None,None,None),
	"DEX": (0xca,None,None,None,None,None,None,None,None,None,None,None,None),
	"DEY": (0x88,None,None,None,None,None,None,None,None,None,None,None,None),
	"EOR": (None,None,0x49,0x45,0x55,None,None,0x4d,0x5d,0x59,None,0x41,0x51),
	"INC": (None,None,None,0xe6,0xf6,None,None,0xee,0xfe,None,None,None,None),
	"INX": (0xe8,None,None,None,None,None,None,None,None,None,None,None,None),
	"INY": (0xc8,None,None,None,None,None,None,None,None,None,None,None,None),
	"JMP": (None,None,None,None,None,None,None,0x4c,None,None,0x6c,None,None),
	"JSR": (None,None,None,None,None,None,None,0x20,None,None,None,None,None),
	"LDA": (None,None,0xa9,0xa5,0xa9,None,None,0xad,0xbd,0xb9,None,0xa1,0xb1),
	"LDX": (None,None,0xa2,0xa6,None,0xb6,None,0xae,None,0xbe,None,None,None),
	"LDY": (None,None,0xa0,0xa4,0xb4,None,None,0xac,0xbc,None,None,None,None),
	"LSR": (None,0x4a,None,0x46,0x56,None,None,0x4e,0x5e,None,None,None,None),
	"NOP": (0xea,None,None,None,None,None,None,None,None,None,None,None,None),
	"ORA": (None,None,0x09,0x05,0x15,None,None,0x0d,0x1d,0x19,None,0x01,0x11),
	"PHA": (0x48,None,None,None,None,None,None,None,None,None,None,None,None),
	"PHP": (0x08,None,None,None,None,None,None,None,None,None,None,None,None),
	"PLA": (0x68,None,None,None,None,None,None,None,None,None,None,None,None),
	"PLP": (0x28,None,None,None,None,None,None,None,None,None,None,None,None),
	"ROL": (None,0x2a,None,0x26,0x36,None,None,0x2e,0x3e,None,None,None,None),
	"ROR": (None,0x6a,None,0x66,0x76,None,None,0x6e,0x7e,None,None,None,None),
	"RTI": (0x40,None,None,None,None,None,None,None,None,None,None,None,None),
	"RTS": (0x60,None,None,None,None,None,None,None,None,None,None,None,None),
	"SBC": (None,None,0xe9,0xe5,0xf5,None,None,0xed,0xfd,0xf9,None,0xe1,0xf1),
	"SEC": (0x38,None,None,None,None,None,None,None,None,None,None,None,None),
	"SED": (0xf8,None,None,None,None,None,None,None,None,None,None,None,None),
	"SEI": (0x78,None,None,None,None,None,None,None,None,None,None,None,None),
	"STA": (None,None,None,0x85,0x95,None,None,0x8d,0x9d,0x99,None,0x81,0x91),
	"STX": (None,None,None,0x86,None,0x96,None,0x8e,None,None,None,None,None),
	"STY": (None,None,None,0x84,0x94,None,None,0x8c,None,None,None,None,None),
	"TAX": (0xaa,None,None,None,None,None,None,None,None,None,None,None,None),
	"TAY": (0xa8,None,None,None,None,None,None,None,None,None,None,None,None),
	"TSX": (0xba,None,None,None,None,None,None,None,None,None,None,None,None),
	"TXA": (0x8a,None,None,None,None,None,None,None,None,None,None,None,None),
	"TXS": (0x9a,None,None,None,None,None,None,None,None,None,None,None,None),
	"TYA": (0x98,None,None,None,None,None,None,None,None,None,None,None,None)
}

def getAddressingMode(node,line):
	if node.argument is None:
		return 0
	elif isinstance(node.argument, Address):
		if node.argument.mode is AddressMode.label:
			return 6
		elif node.argument.mode is AddressMode.indirect_after:
			if node.argument.register in (None,'X'):
				raise CompilerError(line,"Invalid indirect indexed address. Perhaps you meant ',Y'?")
			else:
				return 12
		elif node.argument.mode is AddressMode.indirect_before:
			if node.argument.register == 'X':
				return 11
			elif node.argument.register == 'Y':
				raise CompilerError(line,"Invalid indexed indirect address. Perhaps you meant ',X'?")
			elif node.argument.register is None:
				return 10
		elif node.argument.mode is AddressMode.absolute:
			if node.argument.register is None:
				return 7
			elif node.argument.register == 'X':
				return 8
			elif node.argument.register == 'Y':
				return 9
		elif node.argument.mode is AddressMode.accumulator:
			return 1
		elif node.argument.mode is AddressMode.zero_page:
			if node.argument.register is None:
				return 3
			elif node.argument.register == 'X':
				return 4
			elif node.argument.register == 'Y':
				return 5
	elif isinstance(node.argument,Literal):
		return 2

def to_bytes(i):
	if i > 255:
		hi = i & 0xff
		lo = i >> 8
		return to_bytes(hi) + to_bytes(lo)
	elif i < 0 and i < -255:
		return to_bytes(2**16 - 1 - i)
	elif i < 0:
		return to_bytes(255-i)
	else:
		return chr(i)

def compile(ast):
	labels = {}
	result = b''
	for i,node in enumerate(ast):
		if isinstance(node, Label):
			labels[node.name] = node.line
		else:
			mode = getAddressingMode(node,i+1)
			opcode = OPCODES[node.name][mode]
			if opcode is None:
				raise CompilerError("Incompatible addressing mode used with instruction.t")
			if mode in (0,1):
				result += to_bytes(opcode)
			elif mode == 6 and isinstance(node.argument.value,str):
				result += to_bytes(opcode) + to_bytes(labels[node.argument.name] - i)
			elif mode in (2,3,4,5,6,7,8,9,10,11,12):
				result +=  to_bytes(opcode) + to_bytes(node.argument.value)
	return result