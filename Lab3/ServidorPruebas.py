import socket
import hashlib

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

print(fileName," ----",fileT," ----- ",numClientes)

while True:
    conn, addr = s.accept()     # Establish connection with client.

    numClientesC+=1
    print("Numero Clientes Conectados: ",numClientesC)
    # print('Got connection from', addr)
    data = conn.recv(BUFF)
    print('Server received', repr(data))

    # Enviar tipo de archivo
    # conn.send(fileT.encode())


    sha1 = hashlib.sha1()
    if(numClientesC>numClientes):
        i=0
        with open(fileName , 'rb') as f:
            print('file opened -Read')
            while True:
                print('sending data...',i)
                i += 1
                data = f.read(BUFF)
                # print('data=%s', (data))

                if not data:
                    break
                sha1.update(data)
                # print("Sha Modificado :",i-1,"Veces")
                # write data to a file
                conn.send(data)



        print("Hash Calculado:",sha1.hexdigest())
        has=str(sha1.hexdigest())

        # data=conn.recv(BUFF)
        print(data)

        print(has.encode())

        # TODO si se envia, el cliente y el servidor tienen hash distintos, si no se envia, el hash es igual pero no
        #  se ha enviado
        # conn.send(has.encode())
        f.close()

        print('Done sending')
        numClientesC -= 1
        print("Numero Clientes Conectados: ", numClientesC)
        conn.close()