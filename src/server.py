import sys

from ClientHandler import ClientHandler
from FileManager import FileManager
from MessageHandler import MessageHandler
from TCPServer import TCPServer


def main(argv):
    if len(argv) != 1:
        raise RuntimeError("ERROR: expecting 1 argument\n")

    port = int(argv[0])
    if port < 1024 or port > 65535:
        raise RuntimeError("ERROR: this server port should be in the range of 1024 - 65535\n")

    fm = FileManager()
    mh = MessageHandler(fm)
    ch = ClientHandler(mh)
    server = TCPServer()

    server.start(port, ch)


if __name__ == "__main__":
    main(sys.argv[1:])
