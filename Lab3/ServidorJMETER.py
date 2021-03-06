import socket
import hashlib
import threading
import time
import datetime
import os

lock= threading.Lock()

def pedirDatos():
    fileName = ""
    entr = int(input("Ingrese archivo que quiere enviar 1 (100 MB) o 2 (250MB)"))
    if (entr == 1):
        fileName = "../Doc/Prueba4.mp4"
    elif (entr == 2):
        fileName = "../Doc/Prueba.txt"

    return fileName


tup = pedirDatos()
fileName = tup
numClientesC=0
atender=False

def servidor():
    global numClientesC
    global fileName
    print("Server listening....")

    while True:
        conn, addr = s.accept()  # Establish connection with client.

        numClientesC += 1
        print("Numero Clientes Conectados: ", numClientesC)
        with open(fileName, 'rb') as f:
            while True:
                data = f.read(BUFF)
                if not data:
                    break
                conn.send(data)
            f.close()

            print("Fin envio")
            numClientesC -= 1
            print("Numero Clientes Conectados: ", numClientesC)

            conn.close()

# Puerto, buffer
port = 9999
BUFF = 2048

# TCP ------> socket.AF_INET, socket.SOCK_STREAM
# UDP ------> socket.AF_INET, socket.SOCK_DGRAM
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
s.bind((host, port))

# Por parametro el numero de conexiones que se pueden aceptar antes de rechazar nuevas conexiones
s.listen()

for i in range(25):
    t= threading.Thread(target=servidor, args=())
    t.start()

