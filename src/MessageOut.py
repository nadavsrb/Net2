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

    def __init__(self, statusNum: int, isConClose: bool, data: bytes):
        self.__statusNum = statusNum
        self.__isConClose = isConClose
        self.__data = data

    def __getStatusStr(self) -> str:
        strStatus = {
            200: "OK",
            404: "Not Found",
            301: "Moved Permanently",
        }

        # if didn't fined key would return empty string.
        return strStatus.get(self.__statusNum, self.EMPTY_LINE)

    def __getOtherLines(self) -> str:
        otherLines = {
            200: self.NEW_LINE + self.CON_LEN_STR + str(len(self.__data)),
            301: self.NEW_LINE + self.LOC_STR + self.REDIRECT_FILE_PATH,
        }

        # if didn't fined key would return empty string.
        return otherLines.get(self.__statusNum, self.EMPTY_LINE)

    def __bytes__(self):
        statusStr = self.__getStatusStr()

        if statusStr == self.EMPTY_LINE:
            raise RuntimeError("ERROR: MessageOut: GOT UNKNOWN STATUS!")

        data = self.PROTOCOL_STR + str(self.__statusNum) + self.SPACE + statusStr

        conStatus = self.KEEP_STR
        if self.__isConClose:
            conStatus = self.CLOSE_STR

        data += self.NEW_LINE + self.CON_STR + conStatus

        data += self.__getOtherLines()

        dataBytes = bytes(data)

        if self.__statusNum == self.THERE_IS_DATA:
            dataBytes += bytes(self.NEW_LINE) + self.__data

        return dataBytes
