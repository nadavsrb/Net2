from InStream import InStream
from MessageHandler import MessageHandler
from OutStream import OutStream


class ClientHandler:

    # initialize the client handler with a massage handler that will
    # handle the input and output.
    def __init__(self, mh: MessageHandler):
        self.__mh = mh

    # handle a new client until there is a timeout or the client said to close the connection.
    def handleClient(self, input: InStream, output: OutStream):
        while True:
            inMessage = input.getMessage()
            # disconnect from the client if there is a timeout.
            if inMessage.getIsTimeout():
                return

            outMessage = self.__mh.handleMessage(inMessage)
            output.sendMessage(outMessage)
            # check if the client said to close the connection.
            if outMessage.getIsConClose():
                return
