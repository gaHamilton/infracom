import socket
import hashlib
import time

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

print('Server listening....')

# print(fileName," ----",fileT," ----- ",numClientes)

while True:
    conn, addr = s.accept()     # Establish connection with client.

    # numClientesC+=1
    # print("Numero Clientes Conectados: ",numClientesC)
    # print('Got connection from', addr)

    if(numClientesC>=numClientes):
        i=0
        # conn.send(fileT.encode())
        # print("Tipo del archivo a enviar: ",fileT.encode())

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
                conn.send(data)


        # print("Paquetes enviados: ",i)
        f.close()
        print('Fin envio')
        # numClientesC -= 1
        # print("Numero Clientes Conectados: ", numClientesC)
        conn.close()