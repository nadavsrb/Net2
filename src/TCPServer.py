import socket

from ClientHandler import ClientHandler
from InStream import InStream
from OutStream import OutStream


class TCPServer:
    BACKLOG = 5

    def start(self, port: int, ch: ClientHandler):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind(('', port))
        server.listen(self.BACKLOG)

        while True:
            client, clAddr = server.accept()

            ch.handleClient(InStream(client), OutStream(client))

            client.close()
