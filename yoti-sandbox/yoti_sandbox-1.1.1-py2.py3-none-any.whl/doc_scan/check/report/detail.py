from yoti_python_sdk.utils import YotiSerializable


class SandboxDetail(YotiSerializable):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def to_json(self):
        return {"name": self.name, "value": self.value}
