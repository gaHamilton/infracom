import socket
import threading
import hashlib
import time

BUFF=1024

def cliente(num):
    print("Cliente #",num)
    s = socket.socket()             # Create a socket object
    host = "localhost"  #Ip address that the TCPServer  is there
    port = 9999                     # Reserve a port for your service every new transfer wants a new port or you must wait.

    i=0

    s.connect((host, port))
    s.send("READY".encode())
    print("Conexion con el servidor lista")

    data = s.recv(BUFF)
    fTipo=data.decode()
    print("Tipo del archivo a recibir:",fTipo)

    finT=0

    hashR=""
    sha1=hashlib.sha1()
    with open('Doc/received_file'+str(num)+fTipo, 'wb') as f:
        print('file opened -Write')
        while True:
            # print('receiving data...',i)
            i+=1
            data = s.recv(BUFF)
            # print('data=%s', (data))
            if not data:
                break

            elif (data.__contains__(b"FINM")):
                val=data.find(b"FINM")
                # print(data[0:val])
                # print("--------------------")
                # print(data[val:])
                sha1.update(data[:val])
                hashR = data[val:]
                finT=time.time()
                break
            else:
                sha1.update(data)
                f.write(data)


    print("Paquetes leidos: ",i)
    hashR=hashR[4:].decode()
    print("Hash Recibido: \n",hashR)

    print("Hash Calculado:\n",sha1.hexdigest())
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
    s.send(("Client " + str(num) + " termino con estado de " + notif).encode())

    # Envio de tiempo
    print(str(finT))
    s.send(str(finT).encode())

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