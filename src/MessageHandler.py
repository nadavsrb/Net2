from FileManager import FileManager
from MessageIn import MessageIn
from MessageOut import MessageOut


class MessageHandler:
    def __init__(self, fm: FileManager):
        self.__fm = fm

    def handleMessage(self, input: MessageIn) -> MessageOut:
        if input.getIsTimeout():
            raise RuntimeError("ERROR: MessageHandler: GOT A TIMEOUT MESSAGE")

        data = self.__fm.getFileData(input.getFilePath())

        return MessageOut(self.__fm.getLastFileStatus(), input.getIsConClose(), data)
