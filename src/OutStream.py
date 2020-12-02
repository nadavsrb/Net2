import socket

from IOStream import IOStream


class OutStream(IOStream):

    def __init__(self, clSocket: socket.socket):
        self.__clSocket = clSocket

    def sendMessage(self, mo: MessageOut):
        data = bytes(mo) + bytes(self.EOM)
        self.__clSocket.send(data)
