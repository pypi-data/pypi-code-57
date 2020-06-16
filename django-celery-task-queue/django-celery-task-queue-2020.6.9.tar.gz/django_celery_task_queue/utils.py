import django.apps

from .models import AbstractTask

def get_task_models():
    models = []
    for model in django.apps.apps.get_models():
        if issubclass(model,AbstractTask) and not model._meta.abstract:
            models.append(model)
    return models

def register_task(app,task):
    app.task(task.as_func(),name=task.model.get_task_name())

def register_tasks(app,tasks):
    for task in tasks:
        app.task(task.as_func(),name=task.model.get_task_name())
