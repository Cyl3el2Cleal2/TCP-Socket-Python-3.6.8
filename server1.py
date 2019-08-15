import socket
import base64
import time

HOST = '127.0.0.1'
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST, PORT))
server.listen(5)


while True:
    conn, addr = server.accept()
    print("Connected by", addr)
    while True:
        indata = conn.recv(1024)
        if indata is None : 
            print(indata is None)
            break

        if len(indata) == 0:
            print(len(indata) == 0)
            break

        data = repr(indata.decode())
        data = data[1:len(data)-1]
        conn.send(str.encode(data.lower()))
