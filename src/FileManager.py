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
