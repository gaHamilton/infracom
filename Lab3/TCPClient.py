import socket

host_ip, server_port = "127.0.0.1", 9999


# Initialize a TCP client socket using SOCK_STREAM
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:




    # Establish connection to TCP server and exchange data
    tcp_client.connect((host_ip, server_port))

    message = "SYN"
    tcp_client.sendall(message.encode())
    print("Sent:",message)

    while True:
        received = tcp_client.recv(1024)
        print(received)
        if(received==b'SYN'):
            message = "SYN,ACK"
            tcp_client.sendall(message.encode())
            print("Sent:", message)

            received = tcp_client.recv(1024)
            print(received)
            if(received==b'SYN,ACK'):

                print("Fin Handshake")

                received = tcp_client.recv(1024)
                print(received)
                if(received==b'Peticion'):
                    entr=int(input("Ingrese prueba a realizar (1 o 2)"))
                    if(entr==1):
                        message="1"
                        tcp_client.sendall(message.encode())
                        print("Sent:", message)

                        f = open("Doc/Recibido3.pdf", "wb")

                    elif(entr==2):
                        message = "2"
                        tcp_client.sendall(message.encode())
                        print("Sent:", message)

                        f = open("Doc/Recibido2.docx", "wb")



                received = tcp_client.recv(1024)
                while(received):
                    # print("Recibo paquete")
                    f.write(received)
                    received = tcp_client.recv(1024)

                f.close()

finally:
    print("Fin Recibo3")

    tcp_client.close()
