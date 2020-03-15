import socket
import threading
import hashlib
import time

BUFF=2048
lock= threading.Lock()

def cliente(num, last,lock):
    datosLog=""
    mensajesConsola=[]
    mensajesConsola.append("Cliente #"+str(num))

    # TCP ------> socket.AF_INET, socket.SOCK_STREAM
    # UDP ------> socket.AF_INET, socket.SOCK_DGRAM
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "localhost"
    port = 9999

    i=0

    s.connect((host, port))
    mensajesConsola.append("Conexion con el servidor")
    s.send("READY".encode())
    mensajesConsola.append("Listo para recibir")

    fTipo=""
    while True:
        data = s.recv(BUFF)
        if(data.decode().__contains__(".")):
            fTipo = data.decode()
            break
    print("TIPO:",fTipo)
    finT=0

    hashR=""
    sha1=hashlib.sha1()
    with open('Doc/received_file'+str(num)+fTipo, 'wb') as f:
        mensajesConsola.append("Recibiendo archivo")
        with lock:
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
    mensajesConsola.append("Archivo recibido")
    datosLog+=str(i)+"/"

    # print("Paquetes leidos: ",i)
    # print(hashR[4:])
    hashR=hashR[4:].decode()
    mensajesConsola.append("Cliente"+str(num)+"Hash Recibido: \n"+str(hashR))
    mensajesConsola.append("Cliente"+str(num)+"Hash Calculado:\n"+str(sha1.hexdigest()))

    # print("Son iguales?\n",hashR==sha1.hexdigest())
    f.close()

    notif=""
    if(hashR==sha1.hexdigest()):
        notif="Exito"
        mensajesConsola.append("Archivo recibido Exitosamente")
    else:
        notif = "Error"
        mensajesConsola.append("El Hash del archivo recibido es diferente del calculado")

    # Notificacion de recepcion
    mensajesConsola.append("Envio de notificacion")
    datosLog+="Cliente " + str(num) + " termino con estado de " + notif+"/"

    # Envio de tiempo
    datosLog+=str(finT)+"/"

    # Si es el ultimo, mandar fin para el servidor tambien
    if(last):
        datosLog+="TERMINATE/"
    else:
        datosLog+="CONTINUE/"

    datosLog+="HASH calculado en el cliente\n"+str(sha1.hexdigest())

    # print(datosLog)
    s.send(datosLog.encode())
    s.close()
    mensajesConsola.append('FIN')
    for i in mensajesConsola:
        print(i)


cantidadCliente=25
lock=threading.Lock()
for i in range(cantidadCliente):
    if(i==cantidadCliente-1):
        t = threading.Thread(target=cliente,args=(i, True,lock))
        t.start()
    else:
        t = threading.Thread(target=cliente,args=(i, False,lock))
        t.start()

# print("FIN")