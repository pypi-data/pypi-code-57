# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from . import models


def write_favorite_note(user, d):
    n=d.get('note')
    f, created = models.Favorite.objects.get_or_create(
        user=user,
        content_type=d['content_type'],
        object_id=d['object_id'],
        defaults=dict(
            notes={n.get('anchor')}
        )
    )
    if created:
        return f
    f.notes
    models.Favorite.objects.update_or_create(content_type=d.get)
