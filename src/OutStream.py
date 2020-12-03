import socket

from IOStream import IOStream
from MessageOut import MessageOut


class OutStream(IOStream):

    def __init__(self, clSocket: socket.socket):
        self.__clSocket = clSocket

    def sendMessage(self, mo: MessageOut):
        data = bytes(mo) + self.EOM.encode()
        self.__clSocket.send(data)
