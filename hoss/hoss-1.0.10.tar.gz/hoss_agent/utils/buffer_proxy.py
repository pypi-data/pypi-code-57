import wrapt


class BufferProxy(wrapt.ObjectProxy):
    __target__ = None

    def __init__(self, wrapped, target):
        super(BufferProxy, self).__init__(wrapped)
        self.__target__ = target

    def __iter__(self):
        it = iter(self.__wrapped__)
        for chunk in it:
            if isinstance(chunk, str):
                self.__target__.write(chunk.encode("utf-8"))
            else:
                self.__target__.write(chunk)
            yield chunk
