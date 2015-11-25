import socket
import re
import threading
def x(c):
	u=str(c.recv(1024))
	if not'GET'in u:conn.sendall(t("HTTP/1.1 405 Not Supported"))
	u=re.search('GET [^\s]+ HTTP/1.1',u).group(0).split(" ")[1];u="/index.html" if u == "/" else u;e=u.split(".")[1]
	try:c.sendall(t("HTTP/1.1 200 OK\nContent-Type: "+({'txt':'text/plain','html':'text/html'}[e]if e in'txthtml'else'application/octet-stream')+"\n\n")+open("."+u,'rb').read())
	except:c.sendall(t("HTTP/1.1 404 File Not Found\n\n404 File Not Found"))
t=lambda s: bytes(s,'utf8')
s=socket.socket(2,1)
s.bind(('',36895))
s.listen(10)
while 1:threading.Thread(target=x,args=[s.accept()[0]]).run()
