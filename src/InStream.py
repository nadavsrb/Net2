import socket

from IOStream import IOStream


class InStream(IOStream):
    TIMEOUT_SEC = 1
    BUFFER_SIZE = 100

    def __init__(self, clSocket):
        self._clSocket = clSocket
        self._nextData = ""

    def getMassage(self):
        isTimeout = False
        data = self._nextData
        self._nextData = ""

        try:

            while not (self.EOM in data):
                self._clSocket.settimeout(self.TIMEOUT_SEC)
                data += self._clSocket.recv(self.BUFFER_SIZE).decode()
                self._clSocket.settimeout(None)

            index = data.find(self.EOM) + len(self.EOM)

            if index < len(data):
                self._nextData = data[index:]

            data = data[:index]

        except socket.timeout:
            isTimeout = True

        return InMassage(data, isTimeout)
