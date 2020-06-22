from enum import Enum

class JsonEnum(Enum):
    def toJson(self):
        return self.value
