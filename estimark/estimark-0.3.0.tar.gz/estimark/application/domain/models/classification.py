from .entity import Entity


class Classification(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.classifier_id = attributes['classifier_id']
        self.task_id = attributes['task_id']
