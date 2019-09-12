import socket
import base64
import time
import hashlib

HOST = '127.0.0.1'
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST, PORT))
server.listen(5)

sendOUT = 0

while True:
    conn, addr = server.accept()
    print("Connected by", addr)
    now = time.localtime()
    conn.settimeout(0.002)
    encodedData = ''
    while True:
        start = time.time() #เริ่มจับเวลา
        indata = ''
        try:
            indata = conn.recv(1024)
        except socket.timeout as e:
            if sendOUT == 0:
                print(e)
                conn.sendall(bytes('NACK()', 'utf-8')) #ส่ง NACK เพื่อขอข้อมูลใหม่
                continue
        if indata is None : 
            # print(indata is None)
            print("Timeout changed to 9999")
            break

        if len(indata) == 0:
            # print(len(indata) == 0)
            print("Timeout changed to 9999")
            break
        
        data = repr(indata.decode()) #แปลง object -> string
        data = data[1:len(data)-1] #ตัด ' ' หัวท้ายออก
        print('{{ {}'.format(data[0]))
        print(data[1:len(data)-32])
        print('{} }}'.format(data[-32:]))
        check = hashlib.md5(bytes(data[:len(data)-32], 'utf-8')).hexdigest() == data[-32:] #ตรวจสอบความถูกต้องของข้อมูล
        print('Verification = {}'.format(check))
        if check:
            processedText = data[1:len(data)-32].lower() #แปลงเป็นตัวเล็ก
            conn.sendall(bytes(data[0]+processedText+hashlib.md5(bytes(data[0]+processedText, 'utf-8')).hexdigest(), 'utf-8')) #ส่งข้อมูลกลับไป
            sendOUT = 1 #ไม่ต้อง NACK() เมื่อ timeout
            end = time.time() #หยุดการจับเวลา
            print('Total Time = {} seconds'.format(end-start)) #แสดงเวลา
        else:
            conn.sendall(bytes('NACK()', 'utf-8')) #ส่ง NACK เพื่อขอข้อมูลใหม่
            print('Send NACK({}) signal to secondary'.format(data[0]))
        
        
