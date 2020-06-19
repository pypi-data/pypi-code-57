from .jobs.update_annotation_set_statistics import update_annotation_set_statistics
from .jobs.update_dataset_statistics import update_dataset_statistics
from .query_builder import QueryBuilder, transform_filter_to_condition
from ..models.annotation import NewAnnotation, AnnotationSet, Class, AnnotationObjectClassRel, AnnotationClassRel


def delete_class_in_annotation_set(annotation_set_id, class_id):
    _delete_class_in_annotations(annotation_set_id, class_id)
    _delete_class_in_new_annotations(annotation_set_id, class_id)

    annotation_set = AnnotationSet.objects.get(id=annotation_set_id)
    update_annotation_set_statistics(annotation_set)
    update_dataset_statistics(annotation_set.dataset)


def _delete_class_in_new_annotations(annotation_set_id, class_id):
    class_obj = Class.objects.get(id=class_id)
    class_name = class_obj.name

    qb = QueryBuilder("SELECT id FROM new_annotations")
    qb.condition(QueryBuilder.Condition("annotation_set_id", "=", annotation_set_id))
    qb.condition(transform_filter_to_condition({
        "condition": "is", "pattern": class_name, "name": "class"
    }))

    annotations = NewAnnotation.objects.raw(qb.query())
    for annotation in annotations:
        classes = annotation.classes
        classes.remove(class_name)
        annotation.classes = classes

        objects = annotation.data.get('objects')
        result = []
        for obj in objects:
            classes = obj['classes']
            if class_name not in classes:
                result.append(obj)
                continue

            if len(classes) == 1:
                # skip obj with no classes
                continue

            classes.remove(class_name)
            obj['classes'] = classes
            result.append(obj)
        annotation.data = {'objects': result}
        annotation.save()


def _delete_class_in_annotations(annotation_set_id, class_id):
    annotation_set = AnnotationSet.objects.get(id=annotation_set_id)

    class_obj = Class.objects.get(id=class_id)
    annotation_set.classes.remove(class_obj)
    annotation_set.save()

    objs = AnnotationObjectClassRel.objects.filter(
        annotation_object__annotation__annotation_set_id=annotation_set_id,
        annotation_class_id=class_id
    )
    for obj in objs:
        annotation_obj = obj.annotation_object
        obj.delete()
        if annotation_obj.classes.count() == 0:
            annotation_obj.delete()

    objs = AnnotationClassRel.objects.filter(
        annotation__annotation_set_id=annotation_set_id,
        annotation_class_id=class_id
    )
    for obj in objs:
        obj.delete()
