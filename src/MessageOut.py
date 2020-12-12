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
