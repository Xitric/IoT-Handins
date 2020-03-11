from serial import Serial
import os
import socket

s = socket.socket()
# addr_info = socket.getaddrinfo('127.0.0.1', 5000)
# s.bind(addr_info[0][-1])
# (connection, _) = s.accept()
s.bind(('', 5000))
s.listen()
c, a = s.accept()
print("Connection from {}".format(a))

while True:
    msg = c.recv(4096).decode('utf-8')
    print(msg)

# baud_rate = 115200
# serConIn = Serial(os.environ['RECEIVER_PORT'], baud_rate)


