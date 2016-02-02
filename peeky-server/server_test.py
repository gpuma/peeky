from mysocket import MySocket

port = 6666
srv_sock = MySocket()
print 'server socket ready and listening on port', port
srv_sock.listen(port)
print 'connection ended'
