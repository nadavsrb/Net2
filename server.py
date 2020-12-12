import sys
import socket
from abc import ABCMeta
import os.path

#this class is incharge of the files.
#gets a filepath and read the file.
#has also a file status that symbols the status of the last file it read.
class FileManager:
    RELATIVE_PATH = "files"
    DEFAULT_SIGN = "/"
    DEFAULT_PATH = "/index.html"
    REDIRECT_STR = "/redirect"
    REDIRECT_STATUS = 301
    FILE_NOT_FOUND_STATUS = 404
    FILE_FOUND_STATUS = 200

    #define the status as 0 (differnt from the real statuses).
    def __init__(self):
        self.__lastFileStatus = 0
    #return the status from the last file.
    def getLastFileStatus(self) -> int:
        return self.__lastFileStatus

    #this func gets a file path and return the data inside as bytes.
    #read the file as required, first of all check for spasific path,
    #otherwise read the file regulary.
    def getFileData(self, filePath: str) -> bytes:
        self.__lastFileStatus = 0
        data = ""
        #check if the file path is redirect, if so returns empty string
        #and change the status.
        if filePath == self.REDIRECT_STR:
            self.__lastFileStatus = self.REDIRECT_STATUS
            return data.encode()
        #if the path is "/" change the path into 'index.html'
        if filePath == self.DEFAULT_SIGN:
            filePath = self.DEFAULT_PATH
        #search the file from the 'files' folder.
        filePath = self.RELATIVE_PATH + filePath

        #if the file doesn't exist return empty string and change the status.
        if not os.path.isfile(filePath):
            self.__lastFileStatus = self.FILE_NOT_FOUND_STATUS
            return data.encode()
        #change the status to 'OK' because the file exist and we don't redirect.
        self.__lastFileStatus = self.FILE_FOUND_STATUS
        #if the file is '.ico' or '.jpg' we read it in binary, otherwise as a string.
        if filePath.endswith(".ico") or filePath.endswith(".jpg"):
            bytesData = b''
            with open(filePath, "rb") as file:
                byte = file.read(1)
                while byte:
                    bytesData += byte
                    byte = file.read(1)
            return bytesData

        with open(filePath) as file:
            data = file.read()

        return data.encode()


#this class is in charge of the message for the client.
#it build the massage and can return it in bytes.
class MessageOut:
    NEW_LINE = "\r\n"
    EMPTY_LINE = ""
    SPACE = " "
    CON_STR = "Connection: "
    CLOSE_STR = "close"
    KEEP_STR = "keep-alive"
    PROTOCOL_STR = "HTTP/1.1 "
    CON_LEN_STR = "Content-Length: "
    LOC_STR = "Location: "
    REDIRECT_FILE_PATH = "/result.html"
    THERE_IS_DATA = 200

    #the message out gets a status, the state of the connection and the data
    #in order to build the massage for the client.
    def __init__(self, statusNum: int, isClConClose: bool, data: bytes):
        self.__statusNum = statusNum

        self.__isConClose = False
        #if the status is differnt from 200, or the connection status is close
        #update the client connection and closing it.
        if isClConClose or statusNum != self.THERE_IS_DATA:
            self.__isConClose = True
        
        self.__data = data
    #this funct returns the status as string.
    def __getStatusStr(self) -> str:
        #a map that for each status in int has his massage in string.
        strStatus = {
            200: "OK",
            404: "Not Found",
            301: "Moved Permanently",
        }

        # if didn't fined key would return empty string.
        return strStatus.get(self.__statusNum, self.EMPTY_LINE)
    #this func returns the 'special' lines that relate to the status.
    def __getOtherLines(self) -> str:
        otherLines = {
            200: self.NEW_LINE + self.CON_LEN_STR + str(len(self.__data)),
            301: self.NEW_LINE + self.LOC_STR + self.REDIRECT_FILE_PATH,
        }

        # if didn't fined key would return empty string.
        return otherLines.get(self.__statusNum, self.EMPTY_LINE)
    #return the message in bytes.
    def __bytes__(self):
        statusStr = self.__getStatusStr()

        #if the status is not from the defined statuses.
        if statusStr == self.EMPTY_LINE:
            raise RuntimeError("ERROR: MessageOut: GOT UNKNOWN STATUS!")
        #build the message as required in the protocol.
        data = self.PROTOCOL_STR + str(self.__statusNum) + self.SPACE + statusStr

        conStatus = self.KEEP_STR
        if self.__isConClose:
            conStatus = self.CLOSE_STR

        data += self.NEW_LINE + self.CON_STR + conStatus

        data += self.__getOtherLines()

        dataBytes = data.encode()
        #add the data if the status is 200.
        if self.__statusNum == self.THERE_IS_DATA:
            dataBytes += self.NEW_LINE.encode() + self.NEW_LINE.encode() + self.__data

        return dataBytes
    #returs if the connection is close.
    def getIsConClose(self):
        return self.__isConClose


#this class is in charge of holding the data of the
#massage from the client (the input).
class MessageIn:
    STR_BEFORE_PATH = "GET "
    STR_AFTER_PATH = " HTTP/1.1"
    STR_BEFORE_CON = "Connection: "
    CLOSE_STR = "close"
    KEEP_STR = "keep-alive"
    #the constructor gets the data as string and if there was a timeout.
    def __init__(self, data: str, isTimeout: bool):
        self.__isTimeout = isTimeout
        self.__isConClose = False
        self.__filePath = ""

        self.__initialize(data)

    def __initialize(self, data: str):
        #check if there was a timeout.
        if self.__isTimeout:
            return

        # if not timeout we should print the data:
        print(data)

        startPathIndex = data.find(self.STR_BEFORE_PATH) + len(self.STR_BEFORE_PATH)
        endPathIndex = data.find(self.STR_AFTER_PATH)
        startConIndex = data.find(self.STR_BEFORE_CON) + len(self.STR_BEFORE_CON)
        #if one of the parts that the message should include wasn't found disconnect from the client.
        if startPathIndex == -1 or endPathIndex == -1 or startConIndex == -1:
            # Client sent a non valid message, disconnecting from client...
            self.__isTimeout = True
            return
        #check the connection status.
        if data.startswith(self.CLOSE_STR, startConIndex):
            self.__isConClose = True
        elif not data.startswith(self.KEEP_STR, startConIndex):  # isConClose = False in default
            # Client sent a non valid message, disconnecting from client...
            self.__isTimeout = True
            return
        #gets the file path from the input.
        self.__filePath = data[startPathIndex:endPathIndex]

    #this func returns if there was a timeout
    def getIsTimeout(self):
        return self.__isTimeout
    #this func returns if the connection is close.
    def getIsConClose(self):
        return self.__isConClose
    #this func returns the path to the file.
    def getFilePath(self):
        return self.__filePath


#an abstract class for the streams.
#has only the symbol EOM that represent the end of a massage.
class IOStream:
    __metaclass__ = ABCMeta

    EOM = "\r\n\r\n"




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


#this class is in charge of handling the messages.
#can get an input message and with his file manager returns an output message.
class MessageHandler:
    #gets a file manager.
    def __init__(self, fm: FileManager):
        self.__fm = fm
    #this func handles the message.
    def handleMessage(self, input: MessageIn) -> MessageOut:
        #if there was a timeout in the input throw an exception.
        if input.getIsTimeout():
            raise RuntimeError("ERROR: MessageHandler: GOT A TIMEOUT MESSAGE")
        #read the file with his file manager.
        data = self.__fm.getFileData(input.getFilePath())

        return MessageOut(self.__fm.getLastFileStatus(), input.getIsConClose(), data)

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
        #return the message out according to the data and if there was a timeout.
        return MessageIn(data, isTimeout)

#this class is in charge of the communication with the client.
#gets the messages with the input stream and send them with the output stream.
class ClientHandler:

    # initialize the client handler with a massage handler that will
    # handle the input and output.
    def __init__(self, mh: MessageHandler):
        self.__mh = mh

    # handle a new client until there is a timeout or the client said to close the connection.
    def handleClient(self, input: InStream, output: OutStream):
        while True:
            inMessage = input.getMessage()
            # disconnect from the client if there is a timeout.
            if inMessage.getIsTimeout():
                return

            outMessage = self.__mh.handleMessage(inMessage)
            output.sendMessage(outMessage)
            # check if the client said to close the connection.
            if outMessage.getIsConClose():
                return


#this class is in charge of handeling the server.
#can start a new server that runs on a specific port.
class TCPServer:
    #define how many clients can wait for the server.
    BACKLOG = 5

    #this func starts a new server, gets a port and a client handler to handle the clients.
    def start(self, port: int, ch: ClientHandler):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind(('', port))
        server.listen(self.BACKLOG)
        #the server is always running waitng for clients.
        while True:
            client, clAddr = server.accept()
            #send the new client to the client handler.
            ch.handleClient(InStream(client), OutStream(client))

            client.close()

def main(argv):
    #check if the number of args are correct.
    if len(argv) != 1:
        raise RuntimeError("ERROR: expecting 1 argument\n")

    port = int(argv[0])
    #check if the number of the port is valid.
    if port < 1024 or port > 65535:
        raise RuntimeError("ERROR: this server port should be in the range of 1024 - 65535\n")

    fm = FileManager()
    mh = MessageHandler(fm)
    ch = ClientHandler(mh)
    server = TCPServer()
    #start a new  TCP server with the port from the argv and the client handler.
    server.start(port, ch)


if __name__ == "__main__":
    main(sys.argv[1:])
