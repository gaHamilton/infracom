import datetime
import os
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
    # host = "34.228.233.12"
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
        if(data.__contains__(b".")):
            fTipo = data
            break
    # print("TIPO:",fTipo)
    finT=0

    hashR=""
    sha1=hashlib.sha1()
    fileName="Doc/received_file"+str(num)+fTipo.decode()
    with open(fileName, 'wb') as f:
        mensajesConsola.append("Recibiendo archivo")
        with lock:
            while True:
                # print('receiving data...',i)
                i+=1
                data = s.recv(BUFF)

                if not data:
                    break

                elif (data.__contains__(b"FINM")):
                    val=data.find(b"FINM")
                    sha1.update(data[:val])
                    hashR = data[val:]
                    finT=time.time()

                    break
                else:
                    sha1.update(data)
                    f.write(data)
    f.close()
    mensajesConsola.append("Archivo recibido")

    # Numero de paquetes recibidos
    datosLog+=str(i)+"/"

    hashR=hashR[4:].decode()
    mensajesConsola.append("Cliente"+str(num)+"Hash Recibido: \n"+str(hashR))
    mensajesConsola.append("Cliente"+str(num)+"Hash Calculado:\n"+str(sha1.hexdigest()))

    notif=""
    if(hashR==sha1.hexdigest()):
        notif="Exito"
        mensajesConsola.append("Archivo recibido Exitosamente")
    else:
        notif = "Error"
        mensajesConsola.append("El Hash del archivo recibido es diferente del calculado")

    # Notificacion de recepcion
    mensajesConsola.append("Envio de notificacion")
    recepcion="Cliente " + str(num) + " termino con estado de " + notif
    datosLog+=recepcion+"/"

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
    logDatosCliente(recepcion,i,hashR,sha1.hexdigest(),fileName)

    s.close()
    mensajesConsola.append('FIN')
    for i in mensajesConsola:
        print(i)

def createLog():
    print("Creando log")

    # Fecha y hora --creacion log
    fecha = datetime.datetime.now()

    logName = "LogsCliente/logC" + str(fecha.timestamp()) + ".txt"
    logFile = open(logName, "a")
    logFile.write("Fecha: " + str(fecha) + "\n")

    logFile.write("----------------------------------------\n")

    logFile.close()
    return logName

cantidadCliente=25
lock=threading.Lock()
file=createLog()

def logDatosCliente(recepcion, numPaqRecv,hashR, hash,fileName):

    with lock:
        # # Nombre del archivo y tamanio
        fileN=fileName.split("/")
        fileN = "Nombre del archivo "+fileN[1]+"\n"
        fSize = os.path.getsize(fileName)
        size="Tamanio del archivo: " + str(fSize) + " bytes\n"

        paquetesR="Numero de paquetes recibidos por el cliente:" + str(numPaqRecv) + "\n"
        separador="\n---------------------------------------\n"
        hash="\nHASH calculado en el cliente: \n"+hash
        hashR="\nHASH calculado en el servidor: \n"+hashR
        logFile = open(file, "a")
        logFile.write(fileN+size+recepcion+"\n"+paquetesR+hashR+hash+separador )
        logFile.close()

for i in range(cantidadCliente):
    if(i==cantidadCliente-1):
        t = threading.Thread(target=cliente,args=(i, True,lock))
        t.start()
    else:
        t = threading.Thread(target=cliente,args=(i, False,lock))
        t.start()

# print("FIN")