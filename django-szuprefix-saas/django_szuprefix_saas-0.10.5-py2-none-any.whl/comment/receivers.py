# -*- coding:utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from . import models
from django.db.models.signals import post_save
import logging

log = logging.getLogger('django')


@receiver(post_save, sender=models.Comment)
def update_comment_reply_count(sender, **kwargs):
    try:
        created = kwargs['created']
        if not created:
            return

        comment = kwargs.pop('instance')
        ctid = ContentType.objects.get_for_model(models.Comment).id
        if comment.content_type_id != ctid:
            return
        from django.db.models import F
        c = int(models.Comment.objects.filter(content_type_id=ctid, object_id=comment.object_id).count())
        models.Comment.objects.filter(id=comment.object_id).update(reply_count=c)
    except Exception, e:
        import traceback
        log.error('receiver update_comment_reply_count error: %s', traceback.format_exc())
