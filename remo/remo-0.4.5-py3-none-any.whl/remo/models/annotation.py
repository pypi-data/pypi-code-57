from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from jsonfield import JSONField

from remo_app.remo.api.constants import TaskType, AnnotationStatus
from .dataset import DatasetImage, Dataset
from .annotation_set import AnnotationSet
from .classes import Class
from .tag import Tag


# Annotations:
#   - id
#   - dataset_id ? # maybe useful for fast deletion, but CASCADE delete should work; for filter by dataset
#   - image_id              } unique together
#   - annotation_set_id     }
#   - tags: [string]
#   - classes: [string]   # unique set for all annotation objects for giving annotation
#   - task: (object_detection | instance_segmentation | image_classification) ?
#   - data: {
#       objects: [
#         {
#           name: string
#           points: [float]
#           classes: [string]
#         }
#       ]
#     }

class Tracker(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    gallery = JSONField(null=True)

    class Meta:
        db_table = 'tracker'


class NewAnnotation(models.Model):
    dataset = models.ForeignKey(Dataset, models.CASCADE, related_name='new_annotations')
    image = models.ForeignKey(DatasetImage, models.CASCADE, related_name='new_annotations')
    annotation_set = models.ForeignKey(AnnotationSet, models.CASCADE, related_name='new_annotations')
    classes = JSONField(null=True)
    tags = JSONField(null=True)
    task = models.CharField(max_length=255, choices=TaskType.choices())
    data = JSONField(null=True)
    status = models.IntegerField(choices=AnnotationStatus.choices(), default=AnnotationStatus.not_annotated.value)

    class Meta:
        unique_together = (
            ('image', 'annotation_set'),
        )
        db_table = 'new_annotations'

    def delete_objects(self):
        self.classes = []
        self.data = {'objects': []}
        self.status = AnnotationStatus.not_annotated.value
        self.save()

    def has_annotation(self):
        return self.classes or self.data.get('objects', [])

class Annotation(models.Model):
    # XXX: take a look on clone_relations_from hierarchy on relations change
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=AnnotationStatus.choices(), default=AnnotationStatus.not_annotated.value)

    image = models.ForeignKey(DatasetImage, models.CASCADE, related_name='annotations')
    annotation_set = models.ForeignKey(AnnotationSet, models.CASCADE, related_name='annotations')
    classes = models.ManyToManyField(
        Class,
        through='AnnotationClassRel',
        related_name='annotations'
    )
    tags = models.ManyToManyField(
        Tag,
        through='AnnotationTags',
        related_name='annotations'
    )

    class Meta:
        unique_together = (
            # Image may have only one annotation for each annotation_set
            ('image', 'annotation_set'),
        )
        db_table = 'annotations'

    def __str__(self):
        return 'Annotation #{}'.format(self.pk)

    def has_annotation(self):
        return self.classes.count() > 0 or self.annotation_objects.count() > 0

    def delete_objects(self):
        self.classes.clear()
        for obj in self.annotation_objects.all():
            obj.delete()
        self.status = AnnotationStatus.not_annotated.value
        self.save()

    def clone_relations_from(self, instance):
        """
        Clone relations from given Annotation through to CommonClass:
        * AnnotationClassRel
        * AnnotationObject -> AnnotationObjectClassRel
        :param instance: object to be cloned (already saved)
        """
        for rel in instance.annotation_class_rel.all():
            rel.pk = None
            rel.annotation = self
            rel.save()

        for annotation_obj in instance.annotation_objects.all():
            old_obj = annotation_obj.__class__.objects.get(pk=annotation_obj.pk)
            annotation_obj.pk = None
            annotation_obj.annotation = self
            annotation_obj.save()

            for rel in old_obj.annotation_object_class_rel.all():
                rel.pk = None
                rel.annotation_object = annotation_obj
                rel.save()

        return instance


class AnnotationTags(models.Model):
    image = models.ForeignKey(DatasetImage, models.CASCADE, related_name='annotation_tags')
    annotation = models.ForeignKey(Annotation, models.CASCADE, related_name='annotation_tags')
    annotation_set = models.ForeignKey(AnnotationSet, models.CASCADE, related_name='annotation_tags')
    tag = models.ForeignKey(Tag, models.CASCADE, related_name='annotation_tags')

    class Meta:
        db_table = 'annotation_tags'
        unique_together = (
            ('annotation', 'tag'),
        )


class AnnotationClassRel(models.Model):
    # XXX: take a look on Annotation.clone_relations_from hierarchy on relations change
    annotation = models.ForeignKey(Annotation, models.CASCADE, related_name='annotation_class_rel')
    annotation_class = models.ForeignKey(Class, models.CASCADE)
    questionable = models.BooleanField(default=False)
    score = models.FloatField(null=True)

    class Meta:
        db_table = 'annotation_classes'


class AnnotationObject(models.Model):
    """
    Annotation object used in 'object detection',
    'Object segmentation' tasks
    """
    # XXX: take a look on Annotation.clone_relations_from hierarchy on relations change
    annotation = models.ForeignKey(Annotation, models.CASCADE, related_name='annotation_objects')
    classes = models.ManyToManyField(Class, through='AnnotationObjectClassRel')
    name = models.CharField(max_length=255)
    coordinates = JSONField(null=False)
    auto_created = models.BooleanField(default=False)
    position_number = models.PositiveIntegerField()

    class Meta:
        db_table = 'annotation_objects'
        unique_together = (
            ('annotation', 'name'),
        )

    def __str__(self):
        return 'AnnotationObject #{}'.format(self.pk)


class AnnotationObjectClassRel(models.Model):
    # XXX: take a look on Annotation.clone_relations_from hierarchy on relations change
    annotation_object = models.ForeignKey(AnnotationObject, models.CASCADE, related_name='annotation_object_class_rel')
    annotation_class = models.ForeignKey(Class, models.CASCADE)
    questionable = models.BooleanField(default=False)

    class Meta:
        db_table = 'annotation_object_classes'


@receiver(post_save, sender=Annotation)
def save_annotation(sender, instance, **kwargs):
    """ Update last annotated date for related project"""
    instance.annotation_set.last_annotated_date = timezone.now()
    instance.annotation_set.save()
