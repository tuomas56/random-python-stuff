def lod(reg, mem, machine=None):
	machine.registers[reg] = machine.memory[mem]
	return machine.registers, machine.memory

def sto(reg, mem, machine=None):
	machine.memory[mem] = machine.registers[reg]
	return machine.registers, machine.memory

def _str(reg, val, machine=None):
	machine.registers[reg] = val
	return machine.registers, machine.memory

def stm(mem, val, machine=None):
	machine.memory[mem] = val
	return machine.registers, machine.memory

def cmp(a, b, machine=None):
	if a == b:
		machine.registers[REGS["FLAGS"]] |= 0b01000000
	if a > b:
		machine.registers[REGS["FLAGS"]] |= 0b10000000
	return machine.registers, machine.memory

def mov(a, b, machine=None):
	machine.memory[b] = machine.memory[a]
	return machine.registers, machine.memory

def swp(a, b, machine=None):
	machine.registers[a], machine.registers[b] = machine.registers[b], machine.registers[a]
	return machine.registers, machine.memory

def jmp(loc, machine=None):
	machine.registers[REGS["PC"]] += loc
	return machine.registers, machine.memory

def jeq(loc, machine=None):
	if machine.registers[REGS["FLAGS"]] >> 6 == 1:
		machine.registers[REGS["PC"]] += loc
	return machine.registers, machine.memory

def jne(loc, machine=None):
	if machine.registers[REGS["FLAGS"]] >> 6 != 1:
		machine.registers[REGS["PC"]] += loc
	return machine.registers, machine.memory

def jgt(loc, machine=None):
	if machine.registers[REGS["FLAGS"]] >> 6 == 2:
		machine.registers[REGS["PC"]] += loc
	return machine.registers, machine.memory

def jlt(loc, machine=None):
	if machine.registers[REGS["FLAGS"]] >> 6 == 0:
		machine.registers[REGS["PC"]] += loc
	return machine.registers, machine.memory

def jge(loc, machine=None):
	if machine.registers[REGS["FLAGS"]] >> 6 in (1,2):
		machine.registers[REGS["PC"]] += loc
	return machine.registers, machine.memory

def jle(loc, machine=None):
	if machine.registers[REGS["FLAGS"]] >> 6 in (1,0):
		machine.registers[REGS["PC"]] += loc
	return machine.registers, machine.memory

def jrv(reg, machine=None):
	machine.registers[REGS["PC"]] += machine.registers[reg]

def add(a, b, c, machine=None):
	val = (machine.registers[a] + machine.registers[b])
	if val & 0xffff != val:
		machine.registers[REGS["FLAGS"]] |= 0b00100000
	machine.registers[c] = val & 0xffff
	return machine.registers, machine.memory

def adc(const, reg, machine=None):
	val = (machine.registers[reg] + const)
	if val & 0xffff != val:
		machine.registers[REGS["FLAGS"]] |= 0b00100000
	machine.registers[reg] = val & 0xffff
	return machine.registers, machine.memory

def sub(a, b, c, machine=None):
	machine.registers[c] = (machine.registers[a] - machine.registers[b]) & 0xffff
	return machine.registers, machine.memory

def sbc(const, reg, machine=None):
	machine.registers[reg] = (machine.registers[reg] - const) & 0xffff
	return machine.registers, machine.memory

def mul(a, b, c, machine=None):
	val = (machine.registers[a] * machine.registers[b])
	if val & 0xffff != val:
		machine.registers[REGS["FLAGS"]] |= 0b00100000
	machine.registers[c] = val & 0xffff
	return machine.registers, machine.memory

def mlc(const, reg, machine=None):
	val = (machine.registers[reg] * const)
	if val & 0xffff != val:
		machine.registers[REGS["FLAGS"]] |= 0b00100000
	machine.registers[reg] = val & 0xffff
	return machine.registers, machine.memory

def div(a, b, c, machine=None):
	machine.registers[c] = machine.registers[a] // machine.registers[c]
	return machine.registers, machine.memory

def dvc(const, reg, machine=None):
	machine.registers[reg] //= const
	return machine.registers, machine.memory

def mod(a, b, c, machine=None):
	machine.registers[c] = machine.registers[a] % machine.registers[b]
	return machine.registers, machine.memory

def mdc(const, reg, machine=None):
	machine.registers[reg] %= const
	return machine.registers, machine.memory

def shl(a, b, c, machine=None):
	machine.registers[c] = machine.registers[a] << machine.registers[b]
	return machine.registers, machine.memory

def slc(const, reg, machine=None):
	machine.registers[reg] <<= const
	return machine.registers, machine.memory

def shr(a, b, c, machine=None):
	machine.registers[c] = machine.registers[a] >> machine.registers[b]
	return machine.registers, machine.memory

def src(const, reg, machine=None):
	machine.registers[reg] >>= const
	return machine.registers, machine.memory

def psr(reg, machine=None):
	machine.registers[REGS["SE"]] += 1
	machine.memory[machine.registers[REGS["SE"]]] = machine.registers[reg]
	return machine.registers, machine.memory

def psm(mem, machine=None):
	machine.registers[REGS["SE"]] += 1
	machine.memory[machine.registers[REGS["SE"]]] = machine.memory[mem]
	return machine.registers, machine.memory

def psc(const, machine=None):
	machine.registers[REGS["SE"]] += 1
	machine.memory[machine.registers[REGS["SE"]]] = const

def plr(reg, machine=None):
	machine.registers[REGS["SE"]] -= 1
	machine.registers[reg] = machine.memory[machine.registers[REGS["SE"] + 1]]
	return machine.registers, machine.memory

def plm(mem, machine=None):
	machine.registers[REGS["SE"]] -= 1
	machine.memory[mem] = machine.memory[machine.registers[REGS["SE"] + 1]]
	return machine.registers, machine.memory

def ind(a, b, machine=None):
	machine.registers[b] = machine.memory[machine.registers[a]]
	return machine.registers, machine.memory

def ior(a, b, c, machine=None):
	machine.registers[c] = machine.registers[a] | machine.registers[b]
	return machine.registers, machine.memory

def xor(a, b, c, machine=None):
	machine.registers[c] = machine.registers[a] ^ machine.registers[b]
	return machine.registers, machine.memory

def _and(a, b, c, machine=None):
	machine.registers[c] = machine.registers[a] & machine.registers[b]
	return machine.registers, machine.memory

def _not(a, b, machine=None):
	machine.registers[b] = ~machine.registers[b]
	return machine.registers, machine.memory

def cll(loc, machine=None):
	machine.registers[REGS["SE"]] += 1
	machine.memory[machine.registers[REGS["SE"]]] = machine.registers[REGS["PC"]]
	machine.registers[REGS["PC"]] += loc
	return machine.registers, machine.memory

def ret(machine=None):
	machine.registers[REGS["SE"]] -= 1
	machine.registers[REGS["PC"]] -= machine.memory[machine.registers[REGS["SE"] + 1]]
	return machine.registers, machine.memory

OPCODES = {
	"LOD": (0x00,2,(1,2),lod),
	"STO": (0x01,2,(1,2),sto),
	"STR": (0x02,2,(1,2),_str),
	"STM": (0x27,2,(2,2),stm),
	"CMP": (0x03,2,(1,1),cmp),
	"MOV": (0x04,2,(2,2),mov),
	"SWP": (0x04,2,(1,1),swp),
	"JMP": (0x05,1,(2,),jmp),
	"JEQ": (0x06,1,(2,),jeq),
	"JNE": (0x07,1,(2,),jne),
	"JGT": (0x08,1,(2,),jgt),
	"JLT": (0x09,1,(2,),jlt),
	"JGE": (0x0a,1,(2,),jge),
	"JLE": (0x0b,1,(2,),jle),
	"JRV": (0x0c,1,(1,),jrv),
	"ADD": (0x0d,3,(1,1,1),add),
	"ADC": (0x0e,2,(2,1),adc),
	"SUB": (0x0f,3,(1,1,1),sub),
	"SBC": (0x10,2,(2,1),sbc),
	"MUL": (0x11,3,(1,1,1),mul),
	"MLC": (0x12,2,(2,1),mlc),
	"DIV": (0x13,3,(1,1,1),div),
	"DVC": (0x14,2,(2,1),dvc),
	"MOD": (0x15,3,(1,1,1),mod),
	"MDC": (0x16,2,(2,1),mdc),
	"SHL": (0x17,3,(1,1,1),shl),
	"SLC": (0x18,2,(2,1),slc),
	"SHR": (0x19,3,(1,1,1),shr),
	"SRC": (0x1a,2,(2,1),src),
	"PSR": (0x1b,1,(1,),psr),
	"PSM": (0x1c,1,(2,),psm),
	"PSC": (0x1d,1,(2,),psc),
	"PLR": (0x1e,1,(1,),plr),
	"PLM": (0x1f,1,(1,),plm),
	"IND": (0x20,2,(1,1),ind),
	"IOR": (0x21,3,(1,1,1),ior),
	"XOR": (0x22,3,(1,1,1),xor),
	"AND": (0x23,3,(1,1,1),_and),
	"NOT": (0x24,2,(1,1),_not),
	"CLL": (0x25,1,(2,),cll),
	"RET": (0x26,0,None,ret),
	"HLT": (0x28,0,None,None)
}

#FLAGS: gt, eq, carry

REGS = {
	"FLAGS": 255,
	"SP": 254,
	"SE": 253,
	"PC": 252,
	"A": 0,
	"B": 1,
	"C": 2,
	"D": 3,
	"X": 4,
	"Y": 5,
	"Z": 6
}

def find_with_index(index,item):
	for key,value in OPCODES.items():
		if value[index] == item:
			return key,value

def to_int(hex):
	if len(hex) == 2:
		return (ord(hex[0]) << 8) + ord(hex[1])
	elif len(hex) == 1:
		return ord(hex)

class Machine:
	def __init__(self):
		self.registers = [0]*2**8
		self.memory = [0]*2**16

	def run(self):
		code = list(map(to_int,code))
		while len(code):
			print(code)
			name, info = find_with_index(0,code[0])
			code = code[1:]
			args, code = code[:info[1]+1], code[info[1]+1:]
			a = []
			for l in info[2]:
				a.append(args[:l])
				args = args[l:]
			args = []
			for x in a:
				if len(x) == 2:
					args.append((x[0] << 8) + x[1])
				elif len(x) == 1:
					args.append(x[0])
			self.registers, self.memory = info[3](*args,machine=self)

