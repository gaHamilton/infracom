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
port=20001

def servidor():
    global numClientesC
    global atender
    # TCP ------> socket.AF_INET, socket.SOCK_STREAM
    # UDP ------> socket.AF_INET, socket.SOCK_DGRAM
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip
    s.bind((host, port))

    while True:
        numClientesC += 1
        print("Numero Clientes Conectados: ", numClientesC)
        sha1 = hashlib.sha1()
        while True:
            if (numClientesC >= numClientes or atender):
                print("Starting to send")
                break
        atender = True
        i = 0

        s.send(fileT.encode())

        time.sleep(0.01)

        with open(fileName, 'rb') as f:
            # print("Starting to send")
            while True:
                i += 1
                data = f.read(BUFF)
                if not data:
                    break
                sha1.update(data)

                s.send(data)
            print("Archivo Enviado")

            # Envio de Hash
            has = str(sha1.hexdigest())
            s.send(("FINM" + has).encode())
            f.close()

            print('Fin envio')
            numClientesC -= 1
            print("Numero Clientes Conectados: ", numClientesC)
            break

for i in range(25):
    t= threading.Thread(target=servidor, args=())
    t.start()

