# -*- coding:utf-8 -*- 
__author__ = 'denishuang'
from . import models
from django.contrib.auth.models import User
from ..saas.helper import get_default_party
from django.db.models import Q


def get_user(u):
    if isinstance(u, int):
        return User.objects.get(id=u)
    if hasattr(u, 'user'):
        return u.user
    return u


def get_users(us):
    if not isinstance(us, (list, tuple, set)):
        us = [us]
    us = [get_user(r) for r in us]
    return us


def create_task(target_user_tags, title, content=None, sender=None, link=None, is_force=False, category=None,
                send_time=None, unique_id=None, party=None):
    if party is None:
        if sender is None:
            party = get_default_party()
        else:
            party = sender.as_saas_worker.party if hasattr(sender, 'as_saas_worker') else get_default_party()
    if sender is None:
        sender = party.master.user

    vs = dict(target_user_tags=target_user_tags,
              title=title,
              content=content,
              category=category if category else ('系统消息' if sender.is_superuser else '用户消息'),
              link=link,
              is_force=is_force,
              send_time=send_time,
              is_sent=False)
    if unique_id:
        task, created = models.Task.objects.update_or_create(
            party=party,
            user=sender,
            unique_id=unique_id,
            defaults=vs
        )
    else:
        task = models.Task.objects.create(
            party=party,
            user=sender,
            **vs
        )
    if send_time is None:
        task.send()
    return task


def send_message(sender, receivers, title, is_force=False, unique_id=None, party=None):
    if party is None:
        party = sender.as_saas_worker.party if hasattr(sender, 'as_saas_worker') else get_default_party()
    for user in get_users(receivers):
        vs = dict(
            sender=sender,
            title=title,
            is_read=False,
            is_force=is_force
        )
        if unique_id:
            models.Message.objects.update_or_create(
                party=party,
                receiver=user,
                unique_id=unique_id,
                defaults=vs
            )
        else:
            models.Message.objects.create(
                party=party,
                receiver=user,
                **vs
            )


def revoke_messages(qset):
    qset.filter(is_read=False).delete()
    qset.filter(is_read=True).update(is_active=False)


def revoke_message(receiver, unique_id):
    if not unique_id:
        raise Exception("unique_id can not be empty")
    revoke_messages(models.Message.objects.filter(receiver=receiver, unique_id=unique_id))


def send_task_messages(tasks=None):
    if tasks is None:
        from datetime import datetime
        tasks = models.Task.objects.filter(is_sent=False).filter(
            Q(send_time__isnull=True) | Q(send_time__lt=datetime.now()))
    for t in tasks.filter(is_active=True):
        t.send()
        print t
