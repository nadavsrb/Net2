import socket

from IOStream import IOStream
from MessageIn import MessageIn

#this class is in charge of handling the input from the client socket.
class InStream(IOStream):
    TIMEOUT_SEC = 1.0
    BUFFER_SIZE = 100
    #gets the client socket in the constructor.
    def __init__(self, clSocket: socket.socket):
        self.__clSocket = clSocket
        self.__nextData = ""
    #get a message from the client and return an input message.
    #add the data from before (the next data) to the data
    #and reset the next data to empty string.
    def getMessage(self) -> MessageIn:
        isTimeout = False
        data = self.__nextData
        self.__nextData = ""

        try:
            #until we haven't reach to the end of the massage we keep reading
            #from the socket.
            while not (self.EOM in data):
                #set a timeout to the client socket.
                self.__clSocket.settimeout(self.TIMEOUT_SEC)

                bytesData = self.__clSocket.recv(self.BUFFER_SIZE)

                if bytesData == b'': #then the client disconnect
                    raise socket.timeout()

                data += bytesData.decode()
                self.__clSocket.settimeout(None)

            index = data.find(self.EOM) + len(self.EOM)
            #if there is more input after the EOM we save it in the next data
            #and save the data before the EOM in the data.
            if index < len(data):
                self.__nextData = data[index:]

            data = data[:index]
        #symbols that we reach the timeout.
        except socket.timeout:
            isTimeout = True
        except: #if got RST message from client
            isTimeout = True
        #return the message out according to the data and if there was a timeout.
        return MessageIn(data, isTimeout)
