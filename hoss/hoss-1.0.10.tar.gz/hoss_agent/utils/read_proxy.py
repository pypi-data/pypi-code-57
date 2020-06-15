import io
import wrapt


class ReadProxy(wrapt.ObjectProxy):
    __target__ = None

    def __init__(self, wrapped, target):
        super(ReadProxy, self).__init__(wrapped)
        self.__encode = isinstance(wrapped, io.TextIOBase)
        self.__target__ = target

    def read(self, amt=None):
        data = self.__wrapped__.read(amt)
        if self.__encode:
            self.__target__.write(data.encode("utf-8"))
        else:
            if isinstance(data, str):
                self.__target__.write(data.encode("utf-8"))
            else:
                self.__target__.write(data)
        return data
