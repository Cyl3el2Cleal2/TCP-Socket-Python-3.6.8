import socket
import base64

HOST = '127.0.0.1'
PORT = 65432
allbyte = open('./client data/ceeeb.mp3', "rb").read()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT))

try:
    server.sendall(base64.b64encode(allbyte))
finally:
    print("Closing socket")
    server.close()


# data = s.recv(1024)

# print('Received', repr(data))
print(allbyte)
print('Length => '+str(len(allbyte)))
