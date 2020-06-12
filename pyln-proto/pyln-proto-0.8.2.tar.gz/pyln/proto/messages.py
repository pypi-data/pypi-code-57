import sys

class Message(object):
    def __init__(self, messagetype, **kwargs):
        self.messagetype = messagetype
        self.fields = {}

## Get the current module so we can append newly generated classes to it
mod = sys.modules[Message.__module__]

for name in ['A', 'B', 'C']:
    setattr(mod, name, Message(name))

print(dir(mod))
