class Model:

    def __init__(self, name):
        self.name = name

    def __call__(self, pretrained=False, *args, **kwargs):
        return Model(self.name + ("_trained" if pretrained else ""))

