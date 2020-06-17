from abc import ABC, abstractmethod
class uploader(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def uploadFile(self, fileName, remotePath, **kwargs):
        pass

if __name__ == "__main__":
    a = uploader()