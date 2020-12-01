import socket


class TCPServer:
    BACKLOG = 5

    def start(self, port, ch):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind(('', port))
        server.listen(self.BACKLOG)

        while True:
            client, clAddr = server.accept()

            try:
                ch.handleClient(InStream(client), OutStream(client))
            except socket.timeout:
                pass  # we catch the timeout exception and continue.

            client.close()
