import socket
import threading
import hashlib
import time

BUFF=1024

def cliente(num, last,lock):
    print("Cliente #",num)
    # TCP ------> socket.AF_INET, socket.SOCK_STREAM
    # UDP ------> socket.AF_INET, socket.SOCK_DGRAM
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "localhost"
    port = 9999

    i=0

    s.connect((host, port))
    s.send("READY".encode())
    print("Listo para recibir")

    data = s.recv(BUFF)
    fTipo=data.decode()

    finT=0

    hashR=""
    sha1=hashlib.sha1()
    with open('Doc/received_file'+str(num)+fTipo, 'wb') as f:
        # print("Starting to write")
        # lock.acquire()
        while True:
            # print('receiving data...',i)
            i+=1
            data = s.recv(BUFF)

            # print('data=%s', (data))
            if not data:
                # lock.release()
                break

            elif (data.__contains__(b"FINM")):
                val=data.find(b"FINM")
                # print(data[0:val])
                # print("--------------------")
                # print(data[val:])
                sha1.update(data[:val])
                hashR = data[val:]
                finT=time.time()

                # lock.release()
                break
            else:
                sha1.update(data)
                f.write(data)

    # print("Paquetes leidos: ",i)
    hashR=hashR[4:].decode()
    # print("Cliente",num,"Hash Recibido: \n",hashR)
    # print("Cliente",num,"Hash Calculado:\n",sha1.hexdigest())

    # print("Son iguales?\n",hashR==sha1.hexdigest())
    f.close()

    notif=""
    if(hashR==sha1.hexdigest()):
        notif="Exito"
        print("Archivo recibido Exitosamente")
    else:
        notif = "Error"
        print("El Hash del archivo recibido es diferente del calculado")

    # Notificacion de recepcion
    s.send(("Cliente " + str(num) + " termino con estado de " + notif).encode())

    # Envio de tiempo
    # Envio de tiempo
    s.send(str(finT).encode())

    # Envio numero de paquetes recibidos
    s.send(str(i).encode())

    # Si es el ultimo, mandar fin para el servidor tambien
    if(last):
        s.send("TERMINATE".encode())
    else:
        s.send("CONTINUE".encode())


    s.close()
    print('FIN')


cantidadCliente=25
lock=threading.Lock()
for i in range(cantidadCliente):
    if(i==cantidadCliente-1):
        t = threading.Thread(target=cliente,args=(i, True,lock))
        t.start()
    else:
        t = threading.Thread(target=cliente,args=(i, False,lock))
        t.start()

print("FIN")