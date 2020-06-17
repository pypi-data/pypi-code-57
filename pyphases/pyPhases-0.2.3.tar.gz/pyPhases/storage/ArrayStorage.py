from .Storage import Storage
from ..Data import DataNotFound

class ArrayStorage(Storage):
    array = {}

    def __init__(self, basePath="."):
        self.basePath = basePath

    def read(self, path):
        path = self.getPath(path)
        if(not path in self.array):
            raise DataNotFound("Data was not found:" + path)
        return self.array[path]

    def write(self, path, data):
        path = self.getPath(path)
        self.array[path] = data
