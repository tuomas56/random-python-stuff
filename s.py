from socket import*
s=socket(AF_INET,SOCK_STREAM)
s.bind(('',8002));s.listen(10)
while 1:s.accept()[0].sendall(bytes('HTTP/1.1 418\n','UTF8'))