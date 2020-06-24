from .entity import Entity


class Link(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.source = attributes['source']
        self.target = attributes['target']
