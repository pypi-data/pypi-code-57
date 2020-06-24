from .entity import Entity


class Slot(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.name = attributes.get('name', '')
        self.task_id = attributes['task_id']
        self.schedule_id = attributes['schedule_id']
        self.start = attributes['start']
        self.end = attributes['end']
