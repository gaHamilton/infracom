import socketserver
import time

class Handler_TCPServer(socketserver.BaseRequestHandler):
    """
    The TCP Server class for demonstration.

    Note: We need to implement the Handle method to exchange data
    with TCP client.

    """

    def sendF(self,f):
        print("Envio")
        l = f.read(1024)
        i=0
        while (l):
            print("Envio paquete",i)
            i+=1
            self.request.sendall(l)
            l = f.read(1024)
        print("Fin Envio")
        f.close()

    def handle(self):
        message=""
        while (True):
            # self.request - TCP socket connected to the client
            self.data = self.request.recv(1024)
            print("{} sent:".format(self.client_address[0]))
            print(self.data)
            if(self.data==b'SYN'):
                message="SYN"
                self.request.sendall(message.encode())
                print("Sent:",message)

                self.data = self.request.recv(1024)
                print(self.data)

                if(self.data==b'SYN,ACK'):
                    message = "SYN,ACK"
                    self.request.sendall(message.encode())
                    print("Sent:", message)

                    print("Fin Handshake")

                    message= "Peticion"
                    self.request.sendall(message.encode())
                    print("Sent:", message)

                    self.data = self.request.recv(1024)
                    if(self.data==b'1'):
                        print("Prueba 1")

                        f = open("Doc/Prueba.txt", 'rb')  # open in binary
                        self.sendF(f)
                    elif(self.data==b'2'):
                        print("Prueba2")

                        f = open("Doc/Prueba2.docx", 'rb')  # open in binary
                        self.sendF( f)
                    elif (self.data == b'3'):
                        print("Prueba3")

                        f = open("Doc/Prueba3.pdf", 'rb')  # open in binary
                        self.sendF(f)



if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Init the TCP server object, bind it to the localhost on 9999 port
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()