from InStream import InStream
from MessageHandler import MessageHandler
from OutStream import OutStream


class ClientHandler:

    def __init__(self, mh: MessageHandler):
        self.__mh = mh

    def handleClient(self, input: InStream, output: OutStream):
        while True:
            inMessage = input.getMessage()

            if inMessage.getIsTimeout():
                return

            outMessage = self.__mh.handleMessage(inMessage)
            output.sendMessage(outMessage)
