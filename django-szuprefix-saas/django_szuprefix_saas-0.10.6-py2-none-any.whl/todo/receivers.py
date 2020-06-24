# -*- coding:utf-8 -*-
from django.dispatch import receiver
from . import signals, helper
from .signals import to_create_todos


@receiver(to_create_todos, sender=None)
def create_todos(sender, **kwargs):
    print 'create_todos'
    return helper.create_todos(**kwargs)

# to_create_todos.connect(create_todos)
# print 'receivers'

@receiver(signals.todo_done, sender=None)
def create_todos(sender, **kwargs):
    helper.todo_done(**kwargs)
