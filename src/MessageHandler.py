from FileManager import FileManager
from MessageIn import MessageIn
from MessageOut import MessageOut

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
