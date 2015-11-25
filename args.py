import sys

class ArgumentError(Exception):
	pass

class ArgParser:
	def __init__(self):
		self.positional_required = []
		self.positional_optional = []
		self.positional_collect  = None
		self.named_required = {}
		self.named_optional = {}
		self.named_collect = None

	def add_argument(self,name, switch=False, required=True, metavar="", default="", named=True, description="", collect=False, position=None):
		if required:
			if named:
				self.named_required[name] = { 'switch': switch, 'metavar': metavar, 'default': default, 'description': description }
			else:
				if position == None:
					self.positional_required.append({ 'name': name, 'switch': switch, 'metavar': metavar, 'default': default, 'description': description })
				else:
					self.positional_required.insert(position, { 'name': name, 'switch': switch, 'metavar': metavar, 'default': default, 'description': description })
		elif not collect:
			if named:
				self.named_optional[name] = { 'switch': switch, 'metavar': metavar, 'default': default, 'description': description }
			else:
				if position == None:
					self.positional_optional.append({ 'name': name, 'switch': switch, 'metavar': metavar, 'default': default, 'description': description })
				else:
					self.positional_optional.insert(position, { 'name': name, 'switch': switch, 'metavar': metavar, 'default': default, 'description': description })
		else:
			if named:
				self.named_collect = { 'name': name, 'switch': switch, 'metavar': metavar, 'default': default, 'description': description }
			else:
				self.positional_collect = { 'name': name, 'switch': switch, 'metavar': metavar, 'default': default, 'description': description }

	def parse_args(self,args=None):
		if args == None:
			args = sys.argv[1:]
		num_named = 0
		num_pos = 0
		result = {}
		for i,arg in enumerate(args):
			if len(arg) and arg[0] == "-":
				num_named += 1
				_, *arg = arg
				name = ""
				while len(arg) and arg[0] != "=":
					name += arg[0]
					_, *arg = arg
				switch = False
				value = None
				if len(arg):
					_, *arg = arg
					value = ''.join(arg)
				else:
					switch = True

				if name in self.named_required:
					if switch and not self.named_required[name]['switch']:
						raise ArgumentError("%s is not a switch argument." % name)
					elif switch:
						result[name] = True
					elif self.named_required[name]['switch'] and not switch:
						raise ArgumentError("%s is a switch argument." % name)
					else:
						if value == "":
							value = self.named_required[name]['default']
						result[name] = value
				elif name in self.named_optional:
					if switch and not self.named_optional[name]['switch']:
						raise ArgumentError("%s is not a switch argument." % name)
					elif switch:
						result[name] = True
					elif self.named_optional[name]['switch'] and not switch:
						raise ArgumentError("%s is a switch argument." % name)
					else:
						if value == "":
							value = self.named_optional[name]['default']
						result[name] = value
				elif self.named_collect:
					if self.named_collect['name'] in result:
						if switch:
							result[self.named_collect['name']].append({'name': name, 'value': True})
						else:
							result[self.named_collect['name']].append({'name': name, 'value': value})
					else:
						if switch:
							result[self.named_collect['name']] = [{'name': name, 'value': True}]
						else:
							result[self.named_collect['name']] = [{'name': name, 'value': value}]
				else:
					raise ArgumentError("extra named argument %s provided." % name)
			elif len(arg) and arg[0] != "-":
				value = ''.join(arg)
				index = i - num_named
				num_pos += 1
				if index >= len(self.positional_required):
					if index >= len(self.positional_required) + len(self.positional_optional):
						if self.positional_collect:
							if self.positional_collect['name'] in result:
								result[self.positional_collect['name']].append({'value': value})
							else:
								result[self.positional_collect['name']] = [{'value': value}]
						else:
							raise ArgumentError("extra positional argument provided.")
					else:
						index -= len(self.positional_required)
						name = self.positional_optional[index]['name']
						result[name] = value
				else:
					name = self.positional_required[index]['name']
					result[name] = value

		for name in self.named_required.keys():
			if name not in result and not self.named_required[name]['switch']:
				raise ArgumentError("required named argument %s was not provided." % name)
			elif name not in result and self.named_required[name]['switch']:
				result[name] = False

		if num_pos < len(self.positional_required):
			raise ArgumentError("need more positional arguments.")

		return result

parser = ArgParser()
print(parser.parse_args())





