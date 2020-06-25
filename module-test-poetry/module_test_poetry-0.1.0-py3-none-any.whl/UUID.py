import uuid


class UUID:
    def __init__(self):
        self.value = uuid.uuid4()

    def get_value(self):
        return self.value
