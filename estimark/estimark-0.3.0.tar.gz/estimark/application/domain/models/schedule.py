from .entity import Entity


class Schedule(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.name = attributes.get('name')
        self.state = attributes.get('state', '')
