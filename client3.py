import socket
import base64
import hashlib

class Frame:
    seq = b''
    data = b''
    checksum = b''

    def __init__(self, sequen, dataFrame):
        print(dataFrame)
        self.seq = bytes(str(sequen), 'utf-8')
        self.data = bytes(dataFrame, 'utf-8')
        self.checksum = bytes(hashlib.md5(self.seq+self.data).hexdigest(), 'utf-8')

HOST = '127.0.0.1'
PORT = 65432
byteStr = open('./client data/text.txt', "r").read()

# print(allbyte)
# print(str(allbyte))

# byteStr = str(allbyte)[1:]
# byteStr = byteStr[:-1]

print(byteStr)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT))

print(len(byteStr))
sumData = ''
seq = 1
while(len(byteStr) != 0):
    data = Frame(seq, byteStr[:7])
    print(byteStr[:7])
    byteStr = byteStr[7:]
    # sumData += data.data
    try:
        print(type(data.seq))
        print(data.seq+data.data+data.checksum)
        server.send(data.seq+data.data+data.checksum)
    finally:
        seq = seq+1
        print("Receiving return data")
        getData = server.recv(1024)
        print("Return >>>")
        getDataStr = repr(getData.decode()).replace('\'','')
        print(getDataStr)
        print("Next Frame")
        # print(len(data.checksum))
        sumData = sumData + getDataStr[1:len(getDataStr)-32]

server.close()   
print('Exit')
print(sumData)
