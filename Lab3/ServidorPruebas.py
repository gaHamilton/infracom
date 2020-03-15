import socket
import hashlib
import threading
import time
import datetime
import os
from multiprocessing import Process

global numClientesC


def pedirDatos():
    fileName = ""
    fileT = ""
    entr = int(input("Ingrese archivo que quiere enviar 1 (100 MB) o 2 (250MB)"))
    if (entr == 1):
        fileName = "Doc/Prueba4.mp4"
        fileT = ".mp4"
    elif (entr == 2):
        # TODO aun no hay un archivo de 250 MB, remplazado por uno de prueba de 11MB
        fileName = "Doc/Prueba3.pdf"
        fileT = ".pdf"
    entr = int(input("Ingrese el numero de clientes en simultaneo a enviar el archivo"))
    numClientes = entr
    return fileName, fileT, numClientes


tup = pedirDatos()
fileName = tup[0]
numClientes = tup[2]
fileT = tup[1]
numClientesC=0

def servidor(lock):
    global numClientesC

    print("Server thread listening....")

    while True:
        conn, addr = s.accept()  # Establish connection with client.
        numClientesC += 1
        print("Numero Clientes Conectados: ", numClientesC)
        # print('Got connection from', addr)
        data = conn.recv(BUFF)
        print('Server received', data.decode())

        sha1 = hashlib.sha1()
        if (numClientesC >= numClientes):
            i = 0
            conn.send(fileT.encode())
            # print("Tipo del archivo a enviar: ",fileT.encode())

            # lock.acquire()
            inicioT = time.time()
            with open(fileName, 'rb') as f:
                # print("Starting to send")
                while True:
                    # print('sending data...',i)
                    i += 1
                    data = f.read(BUFF)
                    # print('data=%s', (data))

                    if not data:
                        # lock.release()
                        break
                    sha1.update(data)
                    # print("Sha Modificado :",i-1,"Veces")

                    conn.send(data)
            # print("Paquetes enviados: ",i)
            # print("Hash Calculado:\n",sha1.hexdigest())

            # Envio de Hash
            has = str(sha1.hexdigest())
            conn.send(("FINM" + has).encode())

            f.close()

            # Notificacion de recepcion
            data = conn.recv(BUFF)
            recepcion = data.decode()
            print(recepcion)

            # Notificacion de tiempo
            data = conn.recv(BUFF)
            finT = float(data.decode())
            totalT = finT - inicioT
            # print("Tiempo total:",totalT, "Segundos")

            # Numero de paquetes recibidos por el cliente
            data = conn.recv(BUFF)
            paqRecv = data.decode()


            logDatosCliente(recepcion, totalT, i, paqRecv)


            print('Fin envio')
            numClientesC -= 1
            print("Numero Clientes Conectados: ", numClientesC)

            # Notificacion de fin de cliente o no
            data = conn.recv(BUFF)
            terminS = data.decode()
            # print("Mensaje del cliente: ", terminS)

            conn.close()
            if (terminS == "TERMINATE"):
                print(terminS)
                break
    print("Fin Servidor")


def createLog():
    print("Creando log")

    # Fecha y hora --creacion log
    fecha = datetime.datetime.now()

    logName = "Logs/log" + str(fecha.timestamp()) + ".txt"
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


def logDatosCliente(recepcion, tiempo, numPaqEnv, numPaqRecv):
    # Identifique cada cliente al que se realiza la transferencia de archivos Identifique si la entrega del archivo
    # fue exitosa o no. Tome  los  tiempos  de  transferencia  a  cada  uno  de  los  clientes

    # TODO falta algo de paquetes

    paquetesE="Numero de paquetes enviados por el servidor:" + str(numPaqEnv) + "\n"
    paquetesR="Numero de paquetes recibidos por el cliente:" + str(numPaqRecv) + "\n"
    tiempoT="Tiempo: " + str(tiempo) + " segundos\n"
    separador="----------------------------------------\n"
    logFile = open(logName, "a")
    logFile.write(recepcion+"\n"+paquetesE+paquetesR+tiempoT+separador )
    logFile.close()

# Puerto, buffer
port = 9999
BUFF = 1024

# TCP ------> socket.AF_INET, socket.SOCK_STREAM
# UDP ------> socket.AF_INET, socket.SOCK_DGRAM
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
s.bind((host, port))

# Puede mandarse por parametro el numero de conexiones que se pueden aceptar antes de rechazar nuevas conexiones
s.listen(25)

lock=threading.Lock()

t1 = threading.Thread(target=servidor, args=(lock,))
t2 = threading.Thread(target=servidor, args=(lock,))
t3 = threading.Thread(target=servidor, args=(lock,))
t4 = threading.Thread(target=servidor, args=(lock,))

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

