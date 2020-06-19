from remo_app.remo.models import Annotation, AnnotationSet, Dataset, AnnotationSetStatistics
from .jobs.update_annotation_set_statistics import update_annotation_set_statistics


def copy_annotation_set(original: AnnotationSet) -> AnnotationSet:
    # TODO: with new dataset_id might be issues with not matching images
    copy = original
    original = original.__class__.objects.get(pk=original.pk)
    copy.pk = None
    copy.name = gen_unique_annotation_set_name(copy.name, copy.dataset)
    copy.save()

    copy.classes.set(original.classes.all())

    for annotation in original.annotations.all():
        copy_annotation(annotation, copy)

    copy_annotation_set_statistics(original, copy)
    copy_new_annotations(original, copy)
    return copy


def gen_unique_annotation_set_name(name: str, dataset: Dataset) -> str:
    while True:
        name = 'Copy {}'.format(name)
        if AnnotationSet.objects.filter(dataset=dataset, name=name).exists():
            continue
        return name


def copy_annotation_set_statistics(original: AnnotationSet, dst: AnnotationSet) -> AnnotationSetStatistics:
    stat = AnnotationSetStatistics.objects.filter(annotation_set=original).first()
    if not stat:
        return update_annotation_set_statistics(dst)

    copy = stat
    copy.pk = None
    copy.annotation_set = dst
    copy.save()
    return copy


def copy_annotation(original: Annotation, annotation_set: AnnotationSet) -> Annotation:
    copy = original
    original = original.__class__.objects.get(pk=original.pk)
    copy.pk = None
    copy.annotation_set = annotation_set
    copy.save()

    copy_annotation_classes(original, copy)
    copy_annotation_tags(original, copy)
    copy_annotation_objects(original, copy)
    return copy


def copy_annotation_classes(original: Annotation, dst: Annotation):
    for rel in original.annotation_class_rel.all():
        rel.pk = None
        rel.annotation = dst
        rel.save()


def copy_annotation_tags(original: Annotation, dst: Annotation):
    for rel in original.annotation_tags.all():
        rel.pk = None
        rel.annotation = dst
        rel.annotation_set = dst.annotation_set
        rel.save()


def copy_annotation_objects(original: Annotation, dst: Annotation):
    for annotation_obj in original.annotation_objects.all():
        original_obj = annotation_obj.__class__.objects.get(pk=annotation_obj.pk)
        annotation_obj.pk = None
        annotation_obj.annotation = dst
        annotation_obj.save()

        for rel in original_obj.annotation_object_class_rel.all():
            rel.pk = None
            rel.annotation_object = annotation_obj
            rel.save()


def copy_new_annotations(original: AnnotationSet, dst: AnnotationSet):
    for annotation in original.new_annotations.all():
        annotation.pk = None
        annotation.annotation_set = dst
        annotation.save()
