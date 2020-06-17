from pythontools.core import logger

class Event:

    def __init__(self, name, function, scope="global"):
        self.name = name
        self.function = function
        self.scope = scope

    def call(self, *args, **kwargs):
        self.function(*args, **kwargs)

events = []

def registerEvent(event):
    events.append(event)

def unregisterEvent(event):
    for e in events:
        if e == event:
            events.remove(e)

def call(name, *args, scope="global", **kwargs):
    try:
        for event in events:
            if event.name == name and event.scope == scope:
                event.call(*args, **kwargs)
    except Exception as e:
        logger.log("§cEvent '" + name + "' throw exception: " + str(e))