from remo_app.remo.models import AnnotationSet, AnnotationTags, Tag
from .jobs.update_annotation_set_statistics import update_annotation_set_statistics
from .query_builder import QueryBuilder, transform_filter_to_condition
from ..models.annotation import NewAnnotation


def rename_tag_in_annotation_set(annotation_set_id, tag_id, new_tag_id):
    _rename_tag_in_annotations(annotation_set_id, tag_id, new_tag_id)
    _rename_tag_in_new_annotations(annotation_set_id, tag_id, new_tag_id)

    annotation_set = AnnotationSet.objects.get(id=annotation_set_id)
    update_annotation_set_statistics(annotation_set)


def _rename_tag_in_annotations(annotation_set_id, tag_id, new_tag_id):
    tags = AnnotationTags.objects.filter(annotation_set_id=annotation_set_id, tag_id=tag_id)
    for tag in tags:
        if AnnotationTags.objects.filter(annotation=tag.annotation, tag_id=new_tag_id).first():
            tag.delete()
        else:
            tag.tag_id = new_tag_id
            tag.save()


def _rename_tag_in_new_annotations(annotation_set_id, tag_id, new_tag_id):
    tag_obj = Tag.objects.get(id=tag_id)
    new_tag_obj = Tag.objects.get(id=new_tag_id)

    old_tag = tag_obj.name
    new_tag = new_tag_obj.name

    qb = QueryBuilder("SELECT id FROM new_annotations")
    qb.condition(QueryBuilder.Condition("annotation_set_id", "=", annotation_set_id))
    qb.condition(transform_filter_to_condition({
        "condition": "is", "pattern": old_tag, "name": "tag"
    }))

    annotations = NewAnnotation.objects.raw(qb.query())
    for annotation in annotations:
        tags = annotation.tags
        tags.remove(old_tag)
        if new_tag not in tags:
            tags.append(new_tag)
        annotation.tags = tags
        annotation.save()
