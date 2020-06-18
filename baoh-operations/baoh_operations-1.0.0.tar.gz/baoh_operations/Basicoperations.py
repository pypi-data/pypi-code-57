from .Operations import Operations

class BasicOps(Operations):
    def __init__(self):
        super().__init__()

    def add(self, a, b):
        return a+b