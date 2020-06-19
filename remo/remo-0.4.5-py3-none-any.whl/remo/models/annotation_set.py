from django.conf import settings
from django.db import models
from jsonfield import JSONField

from remo_app.remo.api.constants import AnnotationSetType
from .dataset import Dataset
from .task import Task
from .classes import Class


class AnnotationSet(models.Model):
    # XXX: take a look on clone_relations_from hierarchy on relations change
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    # Release date for annotation set which belongs to public dataset
    released_at = models.DateTimeField(null=True, blank=True)
    last_annotated_date = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=AnnotationSetType.choices())
    task = models.ForeignKey(Task, models.CASCADE, null=True, related_name='annotation_sets')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, related_name='annotation_sets')
    dataset = models.ForeignKey(Dataset, models.CASCADE, null=False, related_name='annotation_sets')
    classes = models.ManyToManyField(Class, related_name='annotation_sets')

    def clone_relations_from(self, instance):
        """
        Clone relations from given AnnotationSet
        :param instance: object to be cloned (already saved)
        :return:
        """
        self.classes.set(instance.classes.all())
        # Don't copy tags here cause deeds doing in DatasetImage's method
        # self.tag_set.set(instance.tag_set.all())

        return instance

    def __str__(self):
        return 'AnnotationSet #{}'.format(self.pk)

    class Meta:
        unique_together = (
            # Dataset may have only unique annotation set names
            ('dataset', 'name'),
        )
        ordering = ('id',)
        db_table = 'annotation_sets'


class AnnotationSetStatistics(models.Model):
    annotation_set = models.ForeignKey(AnnotationSet, models.CASCADE, related_name='statistics')
    dataset = models.ForeignKey(Dataset, models.CASCADE, null=True, related_name='statistics')
    tags = JSONField(null=True)
    classes = JSONField(null=True)
    top3_classes = JSONField(null=True)
    total_classes = models.IntegerField(default=0)
    total_annotation_objects = models.IntegerField(default=0)
    total_annotated_images = models.IntegerField(default=0)
    skipped_images = models.IntegerField(default=0)

    class Meta:
        db_table = 'annotation_set_statistics'
