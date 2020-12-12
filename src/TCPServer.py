import socket

from ClientHandler import ClientHandler
from InStream import InStream
from OutStream import OutStream

#this class is in charge of handeling the server.
#can start a new server that runs on a specific port.
class TCPServer:
    #define how many clients can wait for the server.
    BACKLOG = 5

    #this func starts a new server, gets a port and a client handler to handle the clients.
    def start(self, port: int, ch: ClientHandler):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind(('', port))
        server.listen(self.BACKLOG)
        #the server is always running waitng for clients.
        while True:
            client, clAddr = server.accept()
            #send the new client to the client handler.
            ch.handleClient(InStream(client), OutStream(client))

            client.close()
