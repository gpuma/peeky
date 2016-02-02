import socket


class MySocket:
    '''demonstration class only
      - coded for clarity, not efficiency
    '''

    def __init__(self, sock=None, msglen=2048):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.MSGLEN = msglen

    def listen(self, port):
        self.sock.bind(('localhost', port))
        # queue up as many as 5 connection requests
        self.sock.listen(5)
        while True:
            # establish connection with client socket
            ct, addr = self.sock.accept()
            print 'got connection from', addr
            ct.send('arigato')
            # todo: might need to change this in the future
            # no further reads or writes on the other end of the connection
            ct.shutdown(socket.SHUT_RDWR)
            ct.close()
            return

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < self.MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        # get the message length
        self.MSGLEN = int(self.sock.recv(2048))
        while bytes_recd < self.MSGLEN:
            chunk = self.sock.recv(min(self.MSGLEN - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd += len(chunk)
        return ''.join(chunks)