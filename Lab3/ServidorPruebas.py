import socket
import hashlib
import time
import datetime
import os

global numClientesC
BUFF=1024

port = 9999
s = socket.socket()
host = ""
s.bind((host, port))
s.listen(25)

def pedirDatos():
    fileName = ""
    fileT = ""
    entr=int(input("Ingrese archivo que quiere enviar 1 (100 MB) o 2 (250MB)"))
    if(entr==1):
        fileName="Doc/Prueba4.mp4"
        fileT=".mp4"
    elif(entr==2):
        # TODO aun no hay un archivo de 250 MB, remplazado por uno de prueba de 11MB
        fileName="Doc/Prueba3.pdf"
        fileT=".pdf"
    entr = int(input("Ingrese el numero de clientes en simultaneo a enviar el archivo"))
    numClientes=entr
    return fileName,fileT,numClientes


tup=pedirDatos()
fileName=tup[0]
numClientes=tup[2]
fileT=tup[1]
numClientesC=0

def createLog():
    print("Creando log")

    # Fecha y hora --creacion log
    fecha = datetime.datetime.now()

    logName="Logs/log" + str(fecha.timestamp())+ ".txt"
    logFile = open(logName, "w")
    logFile.write("Fecha: "+str(fecha)+"\n")

    # Nombre del archivo y tamanio
    fileN=fileName.split("/")
    fileN=fileN[1]

    logFile.write("Nombre del archivo: "+fileN+"\n")

    fSize=os.path.getsize(fileName)

    logFile.write("Tamanio del archivo: "+str(fSize)+" bytes\n")
    logFile.write("----------------------------------------\n")

    return logFile,logName


logFile,logName=createLog()


def logDatosCliente(recepcion, tiempo):
    # Identifique cada cliente al que se realiza la transferencia de archivos Identifique si la entrega del archivo
    # fue exitosa o no. Tome  los  tiempos  de  transferencia  a  cada  uno  de  los  clientes

    # TODO falta algo de paquetes

    logFile=open(logName, "a")
    logFile.write(recepcion+"\n")
    logFile.write("Tiempo: "+str(tiempo)+" segundos\n")
    logFile.write("----------------------------------------\n")


print('Server listening....')

# print(fileName," ----",fileT," ----- ",numClientes)

while True:
    conn, addr = s.accept()     # Establish connection with client.

    numClientesC+=1
    print("Numero Clientes Conectados: ",numClientesC)
    # print('Got connection from', addr)
    data = conn.recv(BUFF)
    print('Server received', data.decode())

    sha1 = hashlib.sha1()
    if(numClientesC>=numClientes):
        i=0
        conn.send(fileT.encode())
        print("Tipo del archivo a enviar: ",fileT.encode())

        inicioT = time.time()
        with open(fileName , 'rb') as f:
            print('file opened -Read')
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


        print("Paquetes enviados: ",i)
        print("Hash Calculado:\n",sha1.hexdigest())
        has=str(sha1.hexdigest())

        conn.send(("FINM"+has).encode())

        f.close()

        # Notificacion de recepcion
        data=conn.recv(BUFF)
        recepcion=data.decode()
        print(recepcion)

        # Notificacion de tiempo
        data = conn.recv(BUFF)
        finT=float(data.decode())
        totalT=finT-inicioT
        print("Tiempo total:",totalT, "Segundos")

        logDatosCliente(recepcion,totalT)

        print('Fin envio')
        numClientesC -= 1
        print("Numero Clientes Conectados: ", numClientesC)

        # Notificacion de fin de cliente o no
        data=conn.recv(BUFF)
        terminS=data.decode()
        print("Mensaje del cliente: ",terminS)

        conn.close()
        logFile.close()
        if(terminS=="TERMINATE"):
            break
print("Fin Servidor")