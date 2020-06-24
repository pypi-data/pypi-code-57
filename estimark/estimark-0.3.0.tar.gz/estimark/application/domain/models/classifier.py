from .entity import Entity


class Classifier(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.name = attributes['name']
        self.amount = attributes['amount']
        self.units = attributes.get('units', 'days')
