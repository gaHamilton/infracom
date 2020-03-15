import socket
import hashlib
import threading
import time
import datetime
import os

lock= threading.Lock()

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
atender=False

def servidor():
    global numClientesC
    global atender

    print("Server listening....")

    while True:
        conn, addr = s.accept()  # Establish connection with client.

        numClientesC += 1
        print("Numero Clientes Conectados: ", numClientesC)
        # print('Got connection from', addr)
        data = conn.recv(BUFF)
        print('Server received', data.decode())
        if(data.decode()=="READY"):
            sha1 = hashlib.sha1()
            while True:
                if (numClientesC >= numClientes):
                    print("Starting to send")
                    break
            atender=True
            i = 0
            conn.send(fileT.encode())
            # print("Tipo del archivo a enviar: ",fileT.encode())


            inicioT = time.time()
            with open(fileName, 'rb') as f:
                # print("Starting to send")
                while True:
                    # print('sending data...',i)
                    i += 1
                    data = f.read(BUFF)
                    # print('data=%s', (data))

                    if not data:
                        break
                    sha1.update(data)
                    # print("Sha Modificado :",i-1,"Veces")

                    conn.send(data)
                    # print("Paquetes enviados: ",i)
                    # print("Hash Calculado:\n",sha1.hexdigest())
                print("Archivo Enviado")
                # Envio de Hash
                has = str(sha1.hexdigest())
                conn.send(("FINM" + has).encode())

                f.close()

                # Notificacion de recepcion
                data = conn.recv(BUFF)
                datosCiente = data.decode().split("/")
                recepcion = datosCiente[1]
                print(recepcion)

                # Notificacion de tiempo
                finT = float(datosCiente[2])
                totalT = finT - inicioT
                # print("Tiempo total:",totalT, "Segundos")

                # Numero de paquetes recibidos por el cliente
                paqRecv = datosCiente[0]

                hashR=datosCiente[4]
                logDatosCliente(recepcion, totalT, i, paqRecv,hashR,has)

                print('Fin envio')
                numClientesC -= 1
                print("Numero Clientes Conectados: ", numClientesC)

                # Notificacion de fin de cliente o no
                terminS = datosCiente[3]
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


def logDatosCliente(recepcion, tiempo, numPaqEnv, numPaqRecv,hashR, hash):
    # Identifique cada cliente al que se realiza la transferencia de archivos Identifique si la entrega del archivo
    # fue exitosa o no. Tome  los  tiempos  de  transferencia  a  cada  uno  de  los  clientes

    with lock:
        paquetesE="Numero de paquetes enviados por el servidor:" + str(numPaqEnv) + "\n"
        paquetesR="Numero de paquetes recibidos por el cliente:" + str(numPaqRecv) + "\n"
        tiempoT="Tiempo: " + str(tiempo) + " segundos\n"
        separador="\n---------------------------------------\n"
        hash="\nHASH calculado en el servidor: \n"+hash
        logFile = open(logName, "a")
        logFile.write(recepcion+"\n"+paquetesE+paquetesR+tiempoT+hashR+hash+separador )
        logFile.close()

# Puerto, buffer
port = 9999
BUFF = 2048

# TCP ------> socket.AF_INET, socket.SOCK_STREAM
# UDP ------> socket.AF_INET, socket.SOCK_DGRAM
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
s.bind((host, port))

# Puede mandarse por parametro el numero de conexiones que se pueden aceptar antes de rechazar nuevas conexiones
s.listen(25)

# servidor()

# t1 = threading.Thread(target=servidor, args=())
# t2 = threading.Thread(target=servidor, args=())
# t3 = threading.Thread(target=servidor, args=())
# t4 = threading.Thread(target=servidor, args=())

# t1.start()
# t2.start()
# t3.start()
# t4.start()

# t1.join()
# t2.join()
# t3.join()
# t4.join()

for i in range(25):
    t= threading.Thread(target=servidor, args=())
    t.start()

