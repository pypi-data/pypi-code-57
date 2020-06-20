# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from django.dispatch import Signal

to_create_todos = Signal(providing_args=["target", "name", "expiration", "user_ids", "url"])
to_cancel_todos = Signal(providing_args=["target", "name"])
todo_done = Signal(providing_args=["target", "name", "user_id"])