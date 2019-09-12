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

sumData = ''
seq = 1
while(len(byteStr) != 0):
    data = Frame(seq, byteStr[:7])
    # print(byteStr[:7])
    # sumData += data.data
    try:
        print(type(data.seq))
        print(data.seq+data.data+data.checksum)
        server.send(data.seq+data.data+data.checksum)
        seq = seq+1
        # print("Receiving return data")
        getData = server.recv(1024)
        getDataStr = repr(getData.decode()).replace('\'','')
        if getDataStr == 'NACK()':
            print('>>>>>>>>>>>>> Send again')
            seq = seq-1
            continue
        print("Return >>>")
        print(getDataStr)
        check = hashlib.md5(bytes(getDataStr[:len(getDataStr)-32], 'utf-8')).hexdigest() == getDataStr[-32:]
        if check:
            sumData = sumData + getDataStr[1:len(getDataStr)-32]
        byteStr = byteStr[7:]
    finally:
        print("Next Frame")
        # print(len(data.checksum))
        
server.close()   
print('Exit')
print(sumData)
