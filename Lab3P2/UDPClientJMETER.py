import socket
import threading
import hashlib
import time

BUFF = 1024
lock = threading.Lock()


def cliente(num, last, lock):
    # TCP ------> socket.AF_INET, socket.SOCK_STREAM
    # UDP ------> socket.AF_INET, socket.SOCK_DGRAM
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = "127.0.0.1"
    HostPort = (host, 20001)
    i = 0

    s.sendto("READY".encode(), HostPort)
    hashR = ""
    sha1 = hashlib.sha1()
    fileName = "Recibido/received_file" + str(num)+".pdf"
    with open(fileName, 'wb') as f:
       print("Recibiendo archivo", num)
       while True:
            # print('receiving data...',i)
            i += 1
            data = s.recvfrom(BUFF)
            if not data[0]:
                break

            elif (data[0].__contains__(b"FINM")):
                val = data[0].find(b"FINM")
                sha1.update(data[0][:val])
                hashR = data[0][val:]
                finT = time.time()
                break
            else:
                sha1.update(data[0])
                f.write(data[0])
    f.close()

    hashR = hashR[4:].decode()
    print("HASH RECIBIDO: ", hashR)

    s.close()


cantidadCliente = 25
lock = threading.Lock()

for i in range(cantidadCliente):
    t = threading.Thread(target=cliente, args=(i, False, lock))
    t.start()