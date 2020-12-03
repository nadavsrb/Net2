import os.path


class FileManager:
    RELATIVE_PATH = "files"
    DEFAULT_SIGN = "/"
    DEFAULT_PATH = "/index.html"
    REDIRECT_STR = "/redirect"
    REDIRECT_STATUS = 301
    FILE_NOT_FOUND_STATUS = 404
    FILE_FOUND_STATUS = 200

    def getLastFileStatus(self) -> int:
        return self.__lastFileStatus

    def getFileData(self, filePath: str) -> bytes:
        self.__lastFileStatus = 0
        data = ""

        if filePath == self.RELATIVE_PATH:
            self.__lastFileStatus = self.REDIRECT_STATUS
            return data.encode()

        if filePath == self.DEFAULT_SIGN:
            filePath = self.DEFAULT_PATH

        filePath = self.RELATIVE_PATH + filePath

        if not os.path.isfile(filePath):
            self.__lastFileStatus = self.FILE_NOT_FOUND_STATUS
            return data.encode()

        self.__lastFileStatus = self.FILE_FOUND_STATUS

        if filePath.endswith(".ico") or filePath.endswith(".jpg"):
            bytesData = b''
            with open(filePath, "rb") as file:
                byte = file.read(1)
                while byte:
                    bytesData += byte
                    byte = file.read(1)
            return bytesData

        with open(filePath) as file:
            data = file.readlines()

        return data.encode()
