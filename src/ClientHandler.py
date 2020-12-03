from InStream import InStream
from OutStream import OutStream


class ClientHandler:

    def __init__(self, mh: MessageHandeler):
        self._mh = mh

    def handleClient(self, input: InStream, output: OutStream):
        while True:
            inMessage = input.getMessage()

            if inMessage.getIsTimeout():
                return

            outMessage = self._mh.handleMessage(inMessage)
            output.sendMessage(outMessage)
