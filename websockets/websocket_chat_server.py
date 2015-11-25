from bottle import get, run
from bottle.ext.websocket import GeventWebSocketServer, websocket
from wbserver import WebSocketServer
import time

server = WebSocketServer()

@get('/', apply=[websocket])
def chat(ws):
	with server.connect(ws) as user:
		@user.on('data')
		def on_data(msg):
			print("[%s - %s] %s" % (time.asctime(), user, msg))
			for u in server.users:
				if u is not user:
					u.send(msg)

@server.on('connect')
def on_connect(user):
	print("[%s] %s CONNECTED" % (time.asctime(), user))

@server.on('disconnect')
def on_disconnect(user):
	print("[%s] %s DISCONNECTED" % (time.asctime(), user))

run(host='localhost', port=8080, server=GeventWebSocketServer)