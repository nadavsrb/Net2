import socket

from IOStream import IOStream
from MessageOut import MessageOut

#the out stream is in charge of sending the massages to the client.
class OutStream(IOStream):
    #get the client that it will work with.
    def __init__(self, clSocket: socket.socket):
        self.__clSocket = clSocket
    #this func is incharge of sending the massages.
    #gets a massage and send it to the client in bytes.
    def sendMessage(self, mo: MessageOut):
        #add the end of massage ending to the massage.
        data = bytes(mo) + self.EOM.encode()
        self.__clSocket.send(data)
