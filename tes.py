import socket

s = socket.socket()
s.connect(("192.168.4.1", 8000))
s.send(b"ping\n")
print(s.recv(1024).decode())
s.close()
