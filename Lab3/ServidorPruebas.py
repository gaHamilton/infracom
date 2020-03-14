import socket
import hashlib

BUFF=1024

port = 9999
s = socket.socket()
host = ""
s.bind((host, port))
s.listen(25)

print('Server listening....')

numClientes=0

while True:
    conn, addr = s.accept()     # Establish connection with client.
    numClientes+=1
    print("Numero Clientes: ",numClientes)
    # print('Got connection from', addr)
    data = conn.recv(BUFF)
    print('Server received', repr(data))


    sha1 = hashlib.sha1()
    if(numClientes>0):
        i=0
        with open('Doc/Prueba2.docx' , 'rb') as f:
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
        numClientes -= 1
        print("Numero Clientes: ", numClientes)
        conn.close()