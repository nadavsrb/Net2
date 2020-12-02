class MessageIn:
    STR_BEFORE_PATH = "GET "
    STR_AFTER_PATH = " HTTP/1.1"
    STR_BEFORE_CON = "Connection: "
    CLOSE_STR = "close"
    KEEP_STR = "keep-alive"

    def __init__(self, data: str, isTimeout: bool):
        self.__isTimeout = isTimeout
        self.__isConClose = False
        self.__filePath = ""

        self.__initialize(data)

    def __initialize(self, data: str):
        if self.__isTimeout:
            return

        startPathIndex = data.find(self.STR_BEFORE_PATH) + len(self.STR_BEFORE_PATH)
        endPathIndex = data.find(self.STR_AFTER_PATH)
        startConIndex = data.find(self.STR_BEFORE_CON) + len(self.STR_BEFORE_CON)

        if startPathIndex == -1 or endPathIndex == -1 or startConIndex == -1:
            print("Client sent a non valid message, disconnecting from client...")  # should stay??????
            self.__isConClose = True  # would make us to disconnect the client
            return

        if data.startswith(self.CLOSE_STR, startConIndex):
            self.__isConClose = True
        elif not data.startswith(self.KEEP_STR, startConIndex):  # isConClose = False in default
            print("Client sent a non valid message, disconnecting from client...")  # should stay??????
            self.__isConClose = True  # would make us to disconnect the client
            return

        self.__filePath = data[startPathIndex:endPathIndex]
