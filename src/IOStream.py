from abc import ABCMeta

#an abstract class for the streams.
#has only the symbol EOM that represent the end of a massage.
class IOStream:
    __metaclass__ = ABCMeta

    EOM = "\r\n\r\n"
