from django.db import models
from django.contrib.contenttypes.models import ContentType


class CommentModelManager(models.Manager):
    def filter_comments_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        return super().filter(content_type=content_type, object_id=object_id).filter(parent=None)