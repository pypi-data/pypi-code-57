import logging
from abc import ABCMeta, abstractmethod

from remo_app.remo.models import (
    Annotation,
    AnnotationObject,
    AnnotationClassRel,
    AnnotationObjectClassRel,
    AnnotationSet,
    Class
)
from remo_app.remo.api.constants import TaskType, AnnotationStatus
from remo_app.remo.use_cases.classes import capitalize_class_name

logger = logging.getLogger('remo_app')


class AnnotationRecord(metaclass=ABCMeta):
    """Class represents one annotation"""
    __slots__ = ('source_image_id', 'image_name')
    task_type = None

    def __init__(self, source_image_id, *args, **kwargs):
        self.source_image_id = source_image_id
        self.image_name = kwargs.get('image_name', '')

    @abstractmethod
    def write_to_db(self, image_id, annotation_set_id, classes_mapping, skip_new_classes=False) -> Annotation:
        """
        Write current annotation to database. Must be implemented in
        derived classes
        :param image_id: database image id
        :param annotation_set_id: database annotation set id
        :param classes_mapping: mapping dict {class_name: db_class_id}
        :return: created Annotation object
        """
        raise NotImplementedError

    @staticmethod
    def get_or_create_class(class_name) -> Class:
        obj, created = Class.objects.get_or_create(name=class_name)
        return obj

    @staticmethod
    def get_or_create_annotation(image_id, annotation_set_id) -> Annotation:
        db_annotation = Annotation.objects.filter(image_id=image_id,
                                                  annotation_set_id=annotation_set_id)
        if db_annotation.exists():
            db_annotation = db_annotation.first()
        else:
            db_annotation = Annotation.objects.create(
                image_id=image_id,
                status=AnnotationStatus.done.value,
                annotation_set_id=annotation_set_id
            )
        return db_annotation

    def get_class_id(self, class_name, classes_mapping):
        return classes_mapping.get(class_name) or self.get_or_create_class(class_name).id


class AnnotationObjectDetection(AnnotationRecord):
    """Annotation for object detection task"""
    __slots__ = ('annotation_objects',)
    task_type = TaskType.object_detection

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.annotation_objects = []

    def add_annotation_object(self, coordinates) -> int:
        """
        Add annotation object to annotation
        :param coordinates: coordinates object. See AnnotationObject
        :return: internal annotation object id
        """
        coordinates = list(map(lambda val: {'x': int(val['x']), 'y': int(val['y'])}, coordinates))
        self.annotation_objects.append(
            {'coordinates': coordinates, 'classes': set()},
        )

        return len(self.annotation_objects) - 1

    def add_class(self, annotation_object_id, class_name):
        """Add class for given annotation object"""
        if isinstance(class_name, list):
            for name in class_name:
                self._add_class(annotation_object_id, name)
        elif isinstance(class_name, str):
            self._add_class(annotation_object_id, class_name)

    def _add_class(self, annotation_object_id, class_name):
        """Add class for given annotation object"""
        self.annotation_objects[annotation_object_id]['classes'].add(capitalize_class_name(class_name))

    def write_to_db(self, image_id, annotation_set_id, classes_mapping, skip_new_classes=False) -> Annotation:
        db_annotation = self.get_or_create_annotation(image_id, annotation_set_id)

        annotation_set = AnnotationSet.objects.get(id=annotation_set_id)
        annotation_set_classes = {class_obj.name for class_obj in annotation_set.classes.distinct()}

        obj = AnnotationObject.objects.filter(annotation=db_annotation).last()
        idx = 0
        if obj:
            name = obj.name
            try:
                idx = int(name[len('OBJ'):].strip()) + 1
            except Exception:
                idx = 0

        for annotation_obj in self.annotation_objects:
            db_annotation_objs = AnnotationObject.objects.filter(annotation=db_annotation,
                                                                 coordinates=annotation_obj['coordinates'],
                                                                 auto_created=True)
            # add new classes to annotation object
            if db_annotation_objs.exists():
                for obj in db_annotation_objs:
                    current_classes = {class_obj.name for class_obj in obj.classes.distinct()}
                    new_classes = annotation_obj['classes']
                    if current_classes == new_classes:
                        continue

                    add_new_classes = new_classes - current_classes
                    for class_name in add_new_classes:
                        if not skip_new_classes and class_name not in annotation_set_classes:
                            class_id = self.get_class_id(class_name, classes_mapping)
                            annotation_set.classes.add(class_id)
                            annotation_set.save()
                            annotation_set_classes.add(class_name)

                        if class_name in annotation_set_classes:
                            class_id = self.get_class_id(class_name, classes_mapping)
                            AnnotationObjectClassRel.objects.create(
                                annotation_object=obj,
                                annotation_class_id=class_id
                            )

                continue

            # create new annotation object
            for class_name in annotation_obj['classes']:
                if not skip_new_classes and class_name not in annotation_set_classes:
                    class_id = self.get_class_id(class_name, classes_mapping)
                    annotation_set.classes.add(class_id)
                    annotation_set.save()
                    annotation_set_classes.add(class_name)

            allowed_classes = list(
                filter(lambda class_name: class_name in annotation_set_classes, annotation_obj['classes']))
            if allowed_classes:
                while True:
                    try:
                        db_annotation_object = AnnotationObject.objects.create(
                            annotation=db_annotation,
                            name='OBJ {}'.format(idx),
                            coordinates=annotation_obj['coordinates'],
                            auto_created=True,
                            position_number=idx
                        )
                        break
                    except Exception:
                        idx += 1
                        pass
                idx += 1

                # TODO: need to fix issue with not unique name

                for class_name in allowed_classes:
                    class_id = self.get_class_id(class_name, classes_mapping)
                    AnnotationObjectClassRel.objects.create(
                        annotation_object=db_annotation_object,
                        annotation_class_id=class_id
                    )

        return db_annotation


class AnnotationInstanceSegmentation(AnnotationObjectDetection):
    """Annotation for object segmentation task"""
    task_type = TaskType.instance_segmentation


class AnnotationImageClassification(AnnotationRecord):
    """Annotation for image classification task"""
    __slots__ = ('classes',)
    task_type = TaskType.image_classification

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classes = {}

    def add_class(self, class_name, score):
        """Add class for annotation"""
        if isinstance(class_name, list):
            for name in class_name:
                self._add_class(name, score)
        elif isinstance(class_name, str):
            self._add_class(class_name, score)

    def _add_class(self, class_name, score):
        """Add class for annotation"""
        name = capitalize_class_name(class_name)
        self.classes[name] = {'score': score}

    def write_to_db(self, image_id, annotation_set_id, classes_mapping, skip_new_classes=False) -> Annotation:
        db_annotation = self.get_or_create_annotation(image_id, annotation_set_id)

        annotation_set = AnnotationSet.objects.get(id=annotation_set_id)
        annotation_set_classes = {class_obj.name for class_obj in annotation_set.classes.distinct()}

        class_rels = AnnotationClassRel.objects.filter(annotation=db_annotation)
        current_classes = {class_rel.annotation_class.name: class_rel.score for class_rel in class_rels.all()}

        epsilon = 1e-4
        for class_name, class_data in self.classes.items():
            if not skip_new_classes and class_name not in annotation_set_classes:
                class_id = self.get_class_id(class_name, classes_mapping)
                annotation_set.classes.add(class_id)
                annotation_set.save()
                annotation_set_classes.add(class_name)

            class_id = self.get_class_id(class_name, classes_mapping)
            score = class_data['score']

            # update score for existing obj
            if class_name in current_classes:
                current_score = current_classes.get(class_name)
                if abs(current_score - score) > epsilon:
                    rel = AnnotationClassRel.objects.get(
                        annotation=db_annotation,
                        annotation_class=class_id,
                    )
                    rel.score = score
                    rel.save()
                continue

            # add new obj
            if class_name in annotation_set_classes:
                AnnotationClassRel.objects.create(
                    annotation=db_annotation,
                    annotation_class_id=class_id,
                    score=score
                )

        return db_annotation
