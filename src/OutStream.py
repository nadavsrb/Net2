import socket

from IOStream import IOStream


class OutStream(IOStream):

    def __init__(self, clSocket):
        self._clSocket = clSocket

    def sendMessage(self, mo):
        data = repr(mo) + self.EOM
        self._clSocket.send(data.encode())
