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
