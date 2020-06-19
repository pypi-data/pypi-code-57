from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from djangocomment.managers import CommentModelManager


class CommentModel(models.Model):
    author         = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id      = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    content        = models.TextField(blank=True, null=True)
    parent         = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    datetime       = models.DateTimeField(auto_now_add=True)
    objects        = CommentModelManager()

    def children(self):
        return CommentModel.objects.filter(parent=self)

    def restof(self):
        return list(CommentModel.objects.exclude(parent=self).exclude(parent=None))

    @property
    def is_parent(self):
        if self.parent:
            return True
        return False

    def __str__(self):
        return f"{self.content_type}: {self.object_id}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-pk']