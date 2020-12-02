from socket import socket

from IOStream import IOStream


class InStream(IOStream):
    TIMEOUT_SEC = 1
    BUFFER_SIZE = 100

    def __init__(self, clSocket: socket):
        self._clSocket = clSocket
        self._nextData = ""

    def getMassage(self):
        isTimeout = False
        data = ""

        try:
            while not (self.EOM in data):
                self._clSocket.settimeout(self.TIMEOUT_SEC)
                data += self._clSocket.recv(self.BUFFER_SIZE).decode()
                self._clSocket.settimeout(None)

        except socket.timeout:
            isTimeout = True

        return InMassage(data, isTimeout)
