import pickle
import struct
import socketserver
import socket

class DBServerHandler(socketserver.BaseRequestHandler):
	def setup(self):
		try:
			with open(self.server.filename,"rb") as f:
				self.tables = dict([(name,Table(*table)) for name,table in pickle.load(f).items()]) #Table(*table) unpacks the tuple list and creates a table
		except:
			with open(self.server.filename,"wb") as f:
				self.tables = {}

	def handle(self):
		data = pickle.dumps(dict([(name,table.serialize()) for name,table in self.tables.items()]))
		self.request.send(struct.pack('!q',len(data)))
		self.request.send(data)
		while True:
			try:
				data = struct.unpack('!c',self.request.recv(1))[0].decode("utf-8")
			except:
				break
			if data == "s":
				data = struct.unpack('!q',self.request.recv(8))[0]
				data = self.request.recv(data)
				data = dict([(name,Table(*table)) for name,table in pickle.loads(data).items()])
				for name,table in data.items():
					for value in table.select(allitems):
						if name not in self.tables:
							self.tables[name] = table
						else:
							self.tables[name].update(value[table.primarykey],value)
			elif data == "r":
				data = pickle.dumps(dict([(name,table.serialize()) for name,table in self.tables.items()]))
				self.request.send(struct.pack('!q',len(data)))
				self.request.send(data)
			elif not data:
				break
			with open(self.server.filename,"wb") as f:
				pickle.dump(dict([(name,table.serialize()) for name,table in self.tables.items()]),f)

class DBServer(socketserver.TCPServer):
	def __init__(self,server_address,filename):
		self.filename = filename
		super(DBServer,self).__init__(server_address,DBServerHandler)

class DB:
	def __init__(self):
		self.tables = {}

	def get_table(self,name):
		return self.tables[name]

	def store_table(self,name,table):
		self.tables[name] = table

	def reload(self):
		self.tables = {}

	def save(self):
		pass

class DBFile(DB):
	def __init__(self,filename):
		self.filename = filename
		try:
			with open(filename,"rb") as f:
				self.tables = dict([(name,Table(*table)) for name,table in pickle.load(f).items()])
		except:
			with open(filename,"wb") as f:
				self.tables = {}

	def reload(self):
		with open(self.filename,"rb") as f:
			self.tables = dict([(name,Table(*table)) for name,table in pickle.load(f).item()])

	def save(self):
		with open(self.filename,"wb") as f:
			pickle.dump(dict([(name,table.serialize()) for name,table in self.tables.items()]),f)

class DBRemote(DB):
	def __init__(self,addr):
		self.sock = socket.create_connection(addr)
		data_len = struct.unpack('!q',self.sock.recv(8))[0] #the data length must fit in a long int
		self.tables = dict([(name,Table(*table)) for name,table in pickle.loads(self.sock.recv(data_len)).items()])

	def save(self):
		data = pickle.dumps(dict([(name,table.serialize()) for name,table in self.tables.items()]))
		self.sock.send(struct.pack('!c','s'.encode('utf-8')))
		self.sock.send(struct.pack('!q',len(data)))
		self.sock.send(data)

	def reload(self):
		self.sock.send(struct.pack('!c','r'.encode('utf-8')))
		data_len = struct.unpack('!q',self.sock.recv(8))[0]
		self.tables = dict([(name,Table(*table)) for name,table in pickle.loads(self.sock.recv(data_len)).items()])

	def close(self):
		self.sock.close()

class Table:
	def __init__(self,schema,primarykey,values=[]):
		self.schema = schema
		self.primarykey = primarykey
		self.values = values

	def insert(self,row):
		if isinstance(row,list):
			return [insert(x) for x in row]
		elif isinstance(row,dict):
			try:
				assert(len(row) == len(self.schema))
				for name, type in self.schema.items():
					assert(isinstance(row[name],type))
				self.values.append(row)
			except Exception as e:
				return False

	def get(self,name):
		for value in self.values:
			if value[self.primarykey] == name:
				return value
		else:
			return False

	def update(self,name,newval):
		for value in self.values:
			if value[self.primarykey] == name:
				value.update(newval)
				return value #primary key values must be unique so no need to scan the rest.
		else:
			return False

	def select(self,query):
		return filter(query,self.values)

	def serialize(self):
		return self.schema,self.primarykey,self.values


class Query:
	def __init__(self,func):
		self.func = func

	def __call__(self,*args):
		return self.func(*args)

	def __and__(self,other):
		assert(isinstance(other,Query))
		return Query(lambda *args: self(*args) and other(*args))

	def __or__(self,other):
		assert(isinstance(other,Query))
		return Query(lambda *args: self(*args) or other(*args))

	def __invert__(self):
		return Query(lambda *args: not self(*args))

	def __eq__(self,other):
		return Query(lambda *args: self(*args) == other)

	def __ne__(self,other):
		return Query(lambda *args: self(*args) != other)

	def __le__(self,other):
		return Query(lambda *args: self(*args) <= other)

	def __ge__(self,other):
		return Query(lambda *args: self(*args) >= other)

	def __lt__(self,other):
		return Query(lambda *args: self(*args) < other)

	def __gt__(self,other):
		return Query(lambda *args: self(*args) > other)


where = lambda name: Query(lambda *args: args[0][name])
allitems = Query(lambda *args: True)




