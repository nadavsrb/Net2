from InStream import InStream
from MessageHandler import MessageHandler
from OutStream import OutStream

#this class is in charge of the communication with the client.
#gets the messages with the input stream and send them with the output stream.
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
