import socket
import base64
import time
import hashlib

HOST = '127.0.0.1'
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST, PORT))
server.listen(5)

while True:
    conn, addr = server.accept()
    print("Connected by", addr)
    now = time.localtime()
    filetime = time.strftime("%H%M%S",now)
    encodedData = ''
    while True:
        start = time.time()
        indata = conn.recv(1024)
        if indata is None : 
            print(indata is None)
            break

        if len(indata) == 0:
            print(len(indata) == 0)
            break

        data = repr(indata.decode())
        data = data[1:len(data)-1]
        print('{{ {}'.format(data[0]))
        print(data[1:len(data)-32])
        print('{} }}'.format(data[-32:]))
        check = hashlib.md5(bytes(data[:len(data)-32], 'utf-8')).hexdigest() == data[-32:]
        print('Verification = {}'.format(check))
        processedText = data[1:len(data)-32].lower()
        conn.sendall(bytes(data[0]+processedText+hashlib.md5(bytes(data[0]+processedText, 'utf-8')).hexdigest(), 'utf-8'))
        end = time.time()
        print('Total Time = {} seconds'.format(end-start))
