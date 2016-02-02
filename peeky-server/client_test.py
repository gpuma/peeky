from mysocket import MySocket

print 'creating client socket'
sock = MySocket()
print 'attempting to connect to server'
sock.connect('localhost', 6666)
print 'connection ended'
