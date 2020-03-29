import socket
import hashlib
import threading
import time
import datetime
import os

lock = threading.Lock()


def pedirDatos():
    fileName = ""
    fileT = ""
    entr = int(input("Ingrese archivo que quiere enviar 1 (100 MB) o 2 (250MB)"))
    if (entr == 1):
        fileName = "../Doc/Prueba4.mp4"
        fileT = ".mp4"
    elif (entr == 2):
        fileName = "../Doc/Prueba5.mp4"
        fileT = ".mp4"
    elif (entr == 3):
        print("EASTER EGG .... ok no, solo es para hacer pruebas mas rapido .... archivo de 11MB")
        fileName = "../Doc/Prueba3.pdf"
        fileT = ".pdf"
    entr = int(input("Ingrese el numero de clientes en simultaneo a enviar el archivo"))
    numClientes = entr
    return fileName, fileT, numClientes


tup = pedirDatos()
fileName = tup[0]
numClientes = tup[2]
fileT = tup[1]
numClientesC = 0
atender = False


def createLog():
    print("Creando log")

    # Fecha y hora --creacion log
    fecha = datetime.datetime.now()

    logName = "Logs/UDPLog" + str(fecha.timestamp()) + ".txt"
    logFile = open(logName, "a")
    logFile.write("Fecha: " + str(fecha) + "\n")

    # Nombre del archivo y tamanio
    fileN = fileName.split("/")
    fileN = fileN[1]

    logFile.write("Nombre del archivo: " + fileN + "\n")

    fSize = os.path.getsize(fileName)

    logFile.write("Tamanio del archivo: " + str(fSize) + " bytes\n")
    logFile.write("----------------------------------------\n")

    logFile.close()
    return logName


# Crear el archivo de log
logName = createLog()


def logDatosCliente(recepcion, tiempo, numPaqEnv, numPaqRecv, hashR, hash):
    with lock:
        paquetesE = "Numero de paquetes enviados por el servidor:" + str(numPaqEnv) + "\n"
        paquetesR = "Numero de paquetes recibidos por el cliente:" + str(numPaqRecv) + "\n"
        tiempoT = "Tiempo: " + str(tiempo) + " segundos\n"
        separador = "\n---------------------------------------\n"
        hash = "\nHASH calculado en el servidor: \n" + hash
        logFile = open(logName, "a")
        logFile.write(recepcion + "\n" + paquetesE + paquetesR + tiempoT + hashR + hash + separador)
        logFile.close()


host = ""
BUFF = 1024

def servidor(port1,dir):
    global numClientesC
    global atender
    port=20001+port1
    # TCP ------> socket.AF_INET, socket.SOCK_STREAM
    # UDP ------> socket.AF_INET, socket.SOCK_DGRAM
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip
    s.bind((host, port))
    s.sendto(str(port).encode(),dir)
    print("UDP server up and listening at port ",port)

    while True:
        data = s.recvfrom(BUFF)
        mess = data[0]
        dir = data[1]

        print('Server received', mess.decode())

        if (mess.decode() == "READY"):
            numClientesC += 1
            print("Numero Clientes Conectados: ", numClientesC)
            sha1 = hashlib.sha1()
            while True:
                if (numClientesC >= numClientes or atender):
                    print("Starting to send")
                    break
            atender = True
            i = 0

            s.sendto(fileT.encode(), dir)

            time.sleep(0.01)

            inicioT = time.time()
            with open(fileName, 'rb') as f:
                # print("Starting to send")
                while True:
                    i += 1
                    data = f.read(BUFF)
                    if not data:
                        break
                    sha1.update(data)

                    s.sendto(data,dir)
                print("Archivo Enviado")

                # Envio de Hash
                has = str(sha1.hexdigest())
                s.sendto(("FINM" + has).encode(),dir)
                f.close()


                data = s.recvfrom(BUFF)
                # Notificacion de recepcion
                datosCiente = data[0].decode().split("/")
                recepcion = datosCiente[1]
                print(recepcion)

                # Notificacion de tiempo
                finT = float(datosCiente[2])
                totalT = finT - inicioT
                # print("Tiempo total:",totalT, "Segundos")

                # Numero de paquetes recibidos por el cliente
                paqRecv = datosCiente[0]

                hashR = datosCiente[4]
                logDatosCliente(recepcion, totalT, i, paqRecv, hashR, has)

                print('Fin envio')
                numClientesC -= 1
                print("Numero Clientes Conectados: ", numClientesC)

                # Notificacion de fin de cliente o no
                terminS = datosCiente[3]
                # print("Mensaje del cliente: ", terminS)

                if (terminS == "TERMINATE"):
                    print(terminS)
                    s.close()
                    print("Fin Servidor en puerto ",port)
                    break



port1=20001
# TCP ------> socket.AF_INET, socket.SOCK_STREAM
# UDP ------> socket.AF_INET, socket.SOCK_DGRAM
s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
s.bind((host, port1))
i=1
while True:
    data = s.recvfrom(BUFF)
    mess = data[0]
    dir = data[1]

    if (mess.decode() == "REQUEST"):
        if(i==25):
            i=0
        t = threading.Thread(target=servidor, args=(i,dir))
        i += 1
        t.start()

    if (mess.decode() == "END"):
        print("FIN CONEXIONES")
        break

# for i in range(1):
#     t= threading.Thread(target=servidor, args=(i))
#     t.start()