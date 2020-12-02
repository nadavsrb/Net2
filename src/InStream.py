import socket

from IOStream import IOStream
from MessageIn import MessageIn


class InStream(IOStream):
    TIMEOUT_SEC = 1
    BUFFER_SIZE = 100

    def __init__(self, clSocket: socket.socket):
        self.__clSocket = clSocket
        self.__nextData = ""

    def getMessage(self) -> MessageIn:
        isTimeout = False
        data = self.__nextData
        self.__nextData = ""

        try:

            while not (self.EOM in data):
                self.__clSocket.settimeout(self.TIMEOUT_SEC)
                data += self.__clSocket.recv(self.BUFFER_SIZE).decode()
                self.__clSocket.settimeout(None)

            index = data.find(self.EOM) + len(self.EOM)

            if index < len(data):
                self.__nextData = data[index:]

            data = data[:index]

        except socket.timeout:
            isTimeout = True

        return MessageIn(data, isTimeout)
