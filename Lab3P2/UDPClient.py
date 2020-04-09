import datetime
import os
import socket
import threading
import hashlib
import time

BUFF = 1024
lock = threading.Lock()


def cliente(num, last, lock):
    datosLog = ""
    mensajesConsola = []
    mensajesConsola.append("Cliente #" + str(num))

    # TCP ------> socket.AF_INET, socket.SOCK_STREAM
    # UDP ------> socket.AF_INET, socket.SOCK_DGRAM
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(10)
    host = "127.0.0.1"
    HostPort = (host, 20001)
    i = 0

    # Pedir puerto por donde se va a comunicar con el thread del servidor que le es asignado
    s.sendto("REQUEST".encode(), HostPort)
    data = s.recvfrom(BUFF)
    HostPort = (data[1])
    # print("HOSTPORT--->   ",HostPort)
    s.sendto("READY".encode(), HostPort)

    mensajesConsola.append("Listo para recibir")
    print("Listo para recibir")
    fTipo = ""
    while True:
        data = s.recvfrom(BUFF)
        if (data[0].__contains__(b".")):
            fTipo = data[0].decode()
            break
    # print("TIPO:",fTipo)
    finT = 0

    timeout=True

    hashR = ""
    sha1 = hashlib.sha1()
    fileName = "Recibido/received_file" + str(num) + fTipo
    with open(fileName, 'wb') as f:
        mensajesConsola.append("Recibiendo archivo")
        print("Recibiendo archivo", num)
        while True:
            # print('receiving data...',i)
            i += 1
            try:
                data = s.recvfrom(BUFF)
            except:
                finT = time.time()
                hashR = "TIMEOUT"
                timeout=False
                print("SALGO CON EXCEPCION")
                break

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
    mensajesConsola.append("Archivo recibido")
    print("ARCHIVO RECIVIDO", num)
    # Numero de paquetes recibidos
    datosLog += str(i) + "/"

    if timeout:
        hashR = hashR[4:].decode()
    mensajesConsola.append("Cliente" + str(num) + "Hash Recibido: \n" + str(hashR))
    mensajesConsola.append("Cliente" + str(num) + "Hash Calculado:\n" + str(sha1.hexdigest()))
    print("HASH RECIBIDO", num)
    notif = ""
    if (hashR == sha1.hexdigest()):
        notif = "Exito"
        mensajesConsola.append("Archivo recibido Exitosamente")
    else:
        notif = "Error"
        mensajesConsola.append("El Hash del archivo recibido es diferente del calculado")
    print("NOTIF")
    # Notificacion de recepcion
    mensajesConsola.append("Envio de notificacion")
    recepcion = "Cliente " + str(num) + " termino con estado de " + notif
    datosLog += recepcion + "/"

    # Envio de tiempo
    datosLog += str(finT) + "/"

    # Mandar Terminate para terminar el servidor en el puerto en que se encuentre
    datosLog += "TERMINATE/"

    datosLog += "Hash calculado por el cliente: \n" + str(hashR)

    # print(datosLog)
    s.sendto(datosLog.encode(), HostPort)
    print("ENVIO DATOS")

    logDatosCliente(recepcion, i, hashR, sha1.hexdigest(), fileName)

    for i in mensajesConsola:
        print(i)

    # s.close()


def createLog():
    print("Creando log")

    # Fecha y hora --creacion log
    fecha = datetime.datetime.now()

    logName = "LogsCliente/UDPlogC" + str(fecha.timestamp()) + ".txt"
    logFile = open(logName, "a")
    logFile.write("Fecha: " + str(fecha) + "\n")

    logFile.write("----------------------------------------\n")

    logFile.close()
    return logName


cantidadCliente = 25
lock = threading.Lock()
file = createLog()


def logDatosCliente(recepcion, numPaqRecv, hashR, hash, fileName):
    with lock:
        # # Nombre del archivo y tamanio
        fileN = fileName.split("/")
        fileN = "Nombre del archivo " + fileN[1] + "\n"
        fSize = os.path.getsize(fileName)
        size = "Tamanio del archivo: " + str(fSize) + " bytes\n"

        paquetesR = "Numero de paquetes recibidos por el cliente:" + str(numPaqRecv) + "\n"
        separador = "\n---------------------------------------\n"
        hash = "\nHASH calculado en el cliente: \n" + hash
        hashR = "\nHASH calculado en el servidor: \n" + hashR
        logFile = open(file, "a")
        logFile.write(fileN + size + recepcion + "\n" + paquetesR + hashR + hash + separador)
        logFile.close()


for i in range(cantidadCliente):
    if (i == cantidadCliente - 1):
        t = threading.Thread(target=cliente, args=(i, True, lock))
        t.start()
    else:
        t = threading.Thread(target=cliente, args=(i, False, lock))
        t.start()

# print("FIN")
