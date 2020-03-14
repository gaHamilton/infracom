import socket
import threading
import hashlib

BUFF=1024

def cliente(num):
    print("Cliente #",num)
    s = socket.socket()             # Create a socket object
    host = "localhost"  #Ip address that the TCPServer  is there
    port = 9999                     # Reserve a port for your service every new transfer wants a new port or you must wait.

    i=0

    s.connect((host, port))
    s.send("READY".encode())
    sha1=hashlib.sha1()
    with open('Doc/received_file'+str(num)+".docx", 'wb') as f:
        print('file opened -Write')
        while True:
            print('receiving data...',i)
            i+=1
            data = s.recv(BUFF)
            # print('data=%s', (data))
            if not data:
                break
            sha1.update(data)
            # print("Sha Modificado :",i-1,"Veces")
            # write data to a file
            f.write(data)


    print("Hash Calculado:\n",sha1.hexdigest())
    print("Son iguales?\n",data==sha1)
    f.close()

    s.send("DONE".encode())

    if(data==sha1):
        print("Archivo recibido Exitosamente")
    else:
        print("El Hash del archivo recibido es diferente del calculado")

    s.close()
    print('connection closed')


t1 = threading.Thread(target=cliente(1))
# t2 = threading.Thread(target=cliente(2))

# starting thread 1
t1.start()
# starting thread 2
# t2.start()


# both threads completely executed
print("Done!")