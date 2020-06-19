from remo_app.remo.models import AnnotationSet, Class, AnnotationObjectClassRel, AnnotationClassRel
from remo_app.remo.models.annotation import NewAnnotation
from .jobs.update_annotation_set_statistics import update_annotation_set_statistics
from .jobs.update_dataset_statistics import update_dataset_statistics
from .query_builder import QueryBuilder, transform_filter_to_condition


def rename_class_in_annotation_set(annotation_set_id, class_id, new_class_id):
    _rename_class_in_annotations(annotation_set_id, class_id, new_class_id)
    _rename_class_in_new_annotations(annotation_set_id, class_id, new_class_id)

    annotation_set = AnnotationSet.objects.get(id=annotation_set_id)
    update_annotation_set_statistics(annotation_set)
    update_dataset_statistics(annotation_set.dataset)


def _rename_class_in_new_annotations(annotation_set_id, class_id, new_class_id):
    class_obj = Class.objects.get(id=class_id)
    new_class_obj = Class.objects.get(id=new_class_id)

    old_class = class_obj.name
    new_class = new_class_obj.name

    qb = QueryBuilder("SELECT id FROM new_annotations")
    qb.condition(QueryBuilder.Condition("annotation_set_id", "=", annotation_set_id))
    qb.condition(transform_filter_to_condition({
        "condition": "is", "pattern": old_class, "name": "class"
    }))

    annotations = NewAnnotation.objects.raw(qb.query())
    for annotation in annotations:
        classes = annotation.classes
        classes.remove(old_class)
        if new_class not in classes:
            classes.append(new_class)
        annotation.classes = classes

        objects = annotation.data.get('objects')
        for obj in objects:
            classes = obj['classes']
            if old_class not in classes:
                continue

            classes.remove(old_class)
            if new_class not in classes:
                classes.append(new_class)
            obj['classes'] = classes
        annotation.data = {'objects': objects}
        annotation.save()


def _rename_class_in_annotations(annotation_set_id, class_id, new_class_id):
    annotation_set = AnnotationSet.objects.get(id=annotation_set_id)
    classes = {class_obj.id for class_obj in annotation_set.classes.distinct()}
    if new_class_id not in classes:
        annotation_set.classes.add(new_class_id)

    class_obj = Class.objects.get(id=class_id)
    annotation_set.classes.remove(class_obj)
    annotation_set.save()

    objs = AnnotationObjectClassRel.objects.filter(
        annotation_object__annotation__annotation_set_id=annotation_set_id,
        annotation_class_id=class_id
    )
    for obj in objs:
        obj.annotation_class_id = new_class_id
        obj.save()

    objs = AnnotationClassRel.objects.filter(
        annotation__annotation_set_id=annotation_set_id,
        annotation_class_id=class_id
    )
    for obj in objs:
        obj.annotation_class_id = new_class_id
        obj.save()
