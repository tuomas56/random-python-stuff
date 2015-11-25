#!/usr/bin/env python3

import socket
import sys
import threading
import multiprocessing
import itertools
import curses
from curses.textpad import Textbox,rectangle



def get(prompt,conv,error=None,aftermessage=None):
	while True:
		try:
			return conv(input(prompt))
		except:
			if error:
				print(error)
		finally:
			if aftermessage:
				print(aftermessage)

def side(s):
	def wrapper(func):
		def wrapper2(*args,**kwargs):
			global SIDE
			assert(SIDE == s)
			return func(*args,**kwargs)
		return wrapper2
	return wrapper

def int_with_clamp(a,b):
	def func(x):
		if int(x) >= a and int(x) <= b:
			return int(x)
		else:
			raise ValueError("Integer out of range")
	return func

def equal(a):
	def func(b):
		return a == b
	return func

def notequal(a):
	def func(b):
		return a != b
	return func

def oneof(ls):
	def func(x):
		return x in ls
	return func

def _assert(f):
	def func(x):
		if not f(x):
			raise AssertionError()
	return func

def compose(f,g):
	def wrapper1(*a,**ka):
		return f(g(*a,**ka))
	return wrapper1

def menu(title,options,conv,error=None,aftermessage=None):
	print(title)
	for i,option in enumerate(options):
		print(" "*3,str(i+1)+")",option)
	return get("Please choose an option [1-"+str(len(options))+"]: ",compose(conv,int_with_clamp(1,len(options))),error,aftermessage)

def handleCtrl(addr,data):
	if data[0] == "n":
		if data[1:] not in list(nicks.values()):	
			hasNick = addr in nicks
			nicks[addr] = data[1:]
			for a,c in filter(lambda x: x[0] != addr,zip(list(clientSocks.keys()),list(clientSocks.values()))):
				c.send(("#n"+addr+"#"+data[1:]+"|").encode('utf8'))
			handleMsg(addr,"[Changed nick]" if hasNick else "[Added nick]")
		else:
			clientSocks[addr].send('#einvalidnick'.encode('utf8'))
	elif data[0] == "q":
		clientThreads[addr].stop()
		clientSocks[addr].close()
		del clientSocks[addr]
		for a,c in zip(list(clientSocks.keys()),list(clientSocks.values())):
			c.send(("#q"+addr+"|").encode('utf8'))
		handleMsg(addr,"[Disconnected]")

def handleMsg(addr,data):
	label = "["+addr+"-"+nicks.get(addr,"N/A")+"]"
	print(label,data)


@side("SERVER")
def newClient(conn,addr):
	handleMsg(addr,"[Connected]")
	while True:
		total_data=[]
		data=''
		while True:
			data=conn.recv(8192).decode('utf8')
			global endChar
			if endChar in data:
				total_data.append(data[:data.find(endChar)])
				break
			total_data.append(data)
			if len(total_data)>1:
				#check if end_of_data was split
				last_pair=total_data[-2]+total_data[-1]
				if endChar in last_pair:
					total_data[-2]=last_pair[:last_pair.find(endChar)]
					total_data.pop()
					break
		data = ''.join(total_data)
		for a,c in filter(lambda x: x[0] != addr,zip(list(clientSocks.keys()),list(clientSocks.values()))):
			c.send(addr.encode('utf8')+"#".encode('utf8')+data.encode('utf8')+"|".encode('utf8'))
		data = data[::-1].rstrip()[::-1].rstrip()
		if data[0] == ctrlChar:
			handleCtrl(addr,data[1:])
		else:
			handleMsg(addr,data)
		if clientThreads[addr].stopped():
			del clientThreads[addr]
			return

class StoppableThread(multiprocessing.Process):
	def __init__(self,**kwargs):
		super(StoppableThread,self).__init__(**kwargs)
		self._stop = threading.Event()

	def stop(self):
		self._stop.set()

	def stopped(self):
		return self._stop.isSet()

@side("SERVER")
def acceptClients():
	while True:
		conn, addr = sock.accept()
		global numClients
		global clientThreads
		global clientSocks
		numClients += 1
		thread = StoppableThread(target=newClient,name="Thread-"+str(numClients)+"-"+addr[0],args=(conn,addr[0]))
		clientSocks[addr[0]] = conn
		clientThreads[addr[0]] = thread
		clientThreads[addr[0]].run()

@side("SERVER")
def setupServer():
	global sock
	global numClients
	global clientThreads
	global clientSocks
	global endChar
	global ctrlChar
	global nicks
	TCP_IP = get("Please enter your loopback interface ip/name (default 127.0.0.1): ",lambda x: "127.0.0.1" if x == "" else x,"Invalid.")
	TCP_PORT = get("Please enter the port you wish to host on (defaut 8000): ",lambda x: 8000 if x == "" else int(x),"Not a valid port.")
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.bind((TCP_IP,TCP_PORT))
	sock.listen(10)
	print("Listening on",TCP_IP,TCP_PORT)
	numClients = 0
	clientThreads = {}
	clientSocks = {}
	endChar = "|"
	ctrlChar = "#"
	nicks = {}
	multiprocessing.Process(target=acceptClients).run()

@side("CLIENT")
def dataMonitor():
	global sock
	while True:
		total_data=[]
		data=''
		while True:
			data=sock.recv(8192).decode('utf8')
			global endChar
			if endChar in data:
				total_data.append(data[:data.find(endChar)])
				break
			total_data.append(data)
			if len(total_data)>1:
				#check if end_of_data was split
				last_pair=total_data[-2]+total_data[-1]
				if endChar in last_pair:
					total_data[-2]=last_pair[:last_pair.find(endChar)]
					total_data.pop()
					break
		data = ''.join(total_data)
		print(data)

@side("CLIENT")
def clientCursesFrame():
	multiprocessing.Process(target=dataMonitor).run()
	global sock
	while True:
		console_input = input()
		print("[Me] "+console_input)
		sock.send((console_input+"|").encode("utf8"))


@side("CLIENT")
def setupClient():
	global endChar
	global ctrlChar
	global nicks
	global sock
	TCP_IP = get("Please enter the ip/name of the server you wish to connect to: ",str,"Invalid.")
	TCP_PORT = get("Please enter the port number (default 8000): ",lambda x: 8000 if x == "" else int(x),"Not a valid port.")
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect((TCP_IP,TCP_PORT))
	endChar = "|"
	crlChar = "#"
	nicks = {}
	clientCursesFrame()



def main():
	isServer = menu("Select a mode:",["Server","Client"],equal(1),error="Not a valid option.")
	global SIDE
	if isServer:
		SIDE = "SERVER"
		setupServer()
	else:
		SIDE = "CLIENT"
		setupClient()

if __name__ == "__main__":
	try:
		sys.exit(main())
	except Exception as e:
		print(e)
		global sock
		sock.close()