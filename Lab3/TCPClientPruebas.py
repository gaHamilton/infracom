import socket
import threading
import hashlib

BUFF=1024

def cliente(num):
    print("Cliente #",num)
    s = socket.socket()             # Create a socket object
    host = "localhost"  #Ip address that the TCPServer  is there
    port = 9999                     # Reserve a port for your service every new transfer wants a new port or you must wait.

    i=0

    s.connect((host, port))
    s.send("READY".encode())

    # Recbir tipo de archivo
    # s.recv(BUFF)
    # fTipo=s.decode()
    # print("RECIBIDO:",fTipo)

    hashR=""
    sha1=hashlib.sha1()
    with open('Doc/received_file'+str(num)+".txt", 'wb') as f:
        print('file opened -Write')
        while True:
            print('receiving data...',i)
            i+=1
            data = s.recv(BUFF)
            # print('data=%s', (data))
            if not data:
                break

            elif (data.decode().startswith("FINM")):
                hashR = data.decode()
                break
            else:
                sha1.update(data)
                f.write(data)


    hashR=hashR[4:]
    print("Hash Recibido: \n",hashR)

    print("Hash Calculado:\n",sha1.hexdigest())
    # print("Son iguales?\n",hashR==sha1.hexdigest())
    f.close()

    s.send(("Done Client "+str(num)).encode())

    if(hashR==sha1.hexdigest()):
        print("Archivo recibido Exitosamente")
    else:
        print("El Hash del archivo recibido es diferente del calculado")

    s.close()
    print('FIN')


t1 = threading.Thread(target=cliente(1))
# t2 = threading.Thread(target=cliente(2))

# starting thread 1
t1.start()
# starting thread 2
# t2.start()


# both threads completely executed
print("Done!")