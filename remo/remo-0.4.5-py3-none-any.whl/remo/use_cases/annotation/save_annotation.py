# import threading

from remo_app.remo.api.constants import TaskType
from remo_app.remo.models import Annotation, AnnotationObject
from remo_app.remo.models.annotation import NewAnnotation, AnnotationClassRel

# lock = threading.Lock()
# Probably was needed for sqlite

def update_new_annotation(annotation: Annotation):

    # with lock:
    if annotation is None:
        return

    image = annotation.image
    annotation_set = annotation.annotation_set

    new_annotation = NewAnnotation()
    qs = NewAnnotation.objects.filter(image_id=image.id, annotation_set_id=annotation_set.id)
    if qs:
        new_annotation = qs.first()
    new_annotation.annotation_set_id = annotation_set.id
    new_annotation.image_id = image.id
    new_annotation.dataset_id = image.dataset.id
    new_annotation.tags = [obj.name for obj in annotation.tags.distinct()]
    new_annotation.task = annotation_set.task.type
    new_annotation.status = annotation.status

    objs = AnnotationObject.objects.filter(annotation_id=annotation.id)
    objects = []
    classes = set()
    if new_annotation.task == TaskType.image_classification.name:
        annotation_classes = AnnotationClassRel.objects.filter(annotation_id=annotation.id)
        obj_classes = [rel.annotation_class.name for rel in annotation_classes]
        objects.append({
            'classes': obj_classes
        })
        classes = classes.union(obj_classes)
    else:
        for obj in objs:
            obj_classes = [c.name for c in obj.classes.all()]
            objects.append({
                'name': obj.name,
                'coordinates': obj.coordinates,
                'classes': obj_classes
            })
            classes = classes.union(obj_classes)
    new_annotation.classes = list(classes)
    new_annotation.data = {'objects': objects}
    new_annotation.save()
