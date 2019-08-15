import socket
import base64

HOST = '127.0.0.1'
PORT = 65432
text = open('./client data/text.txt', "r").read()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT))

try:
    server.sendall(str.encode(text))
finally:
    print("receiving result")
    data = server.recv(len(text)*2)
    newText = open('./client data/text_small.txt', "w")
    newText.write(data.decode())
    newText.close()
    server.close()


# data = s.recv(1024)

# print('Received', repr(data))

