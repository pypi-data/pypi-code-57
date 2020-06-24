# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from . import models


def create_todos(target=None, name=None, url=None, expiration=None, user_ids=[]):
    from django.contrib.auth.models import User
    ctype = ContentType.objects.get_for_model(target)
    for id in user_ids:
        user = User.objects.filter(id=id).first()
        if not user:
            continue
        models.Todo.objects.get_or_create(
            party=target.party,
            target_type=ctype,
            target_id=target.id,
            user=user,
            name=name,
            defaults=dict(
                url=url,
                is_done=False,
                expiration=expiration
            )
        )

def cancel_todos(target, name=None):
    ctype = ContentType.objects.get_for_model(target)
    qd = dict(target_type=ctype,
              target_id=target.id)
    if name is not None:
        qd['name'] = name
    from datetime import datetime
    models.Todo.objects.filter(**qd).update(expiration=datetime.now())

def todo_done(target, user, name=None):
    ctype = ContentType.objects.get_for_model(target)
    qd = dict(target_type=ctype,
              target_id=target.id,
              user=user)
    if name is not None:
        qd['name'] = name
    models.Todo.objects.filter(**qd).update(is_done=True)
