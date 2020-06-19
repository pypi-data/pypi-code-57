from abc import ABCMeta, abstractmethod

from remo_app.remo.models import AnnotationObject, Annotation, AnnotationClassRel, DatasetImage, AnnotationSet
from remo_app.remo.models.annotation import AnnotationTags, NewAnnotation
from remo_app.remo.api.constants import TaskType
from remo_app.remo.use_cases.annotation.export_tags import JSON


class BaseExporter(metaclass=ABCMeta):
    """
    Convert annotations data in specific format to annotations records
    """

    task = None

    def __init__(self):
        self.class_encoding = None
        self.errors = []

    def __str__(self):
        return self.__class__.__name__

    def encode_class(self, class_name: str) -> (str, str):
        """
        Encodes class name to label name based on class encoding

        Return:
            label name
            error
        """
        if not self.class_encoding:
            return class_name, None

        try:
            label_name = self.class_encoding.encode_class(class_name)
            return label_name, None
        except Exception as err:
            return class_name, str(err)

    def add_error(self, err):
        if err:
            self.errors.append(err)

    def encode_classes(self, classes):
        encoded = []
        for class_name in classes:
            label, error = self.encode_class(class_name)
            self.add_error(error)
            encoded.append(label)

        return encoded


class RemoBase(BaseExporter):
    expected_keys = {
        'item.file_name',
        'item.height',
        'item.width',
        'item.tags',
        'item.task',
    }

    def parse_base_annotation(self, annotation, full_path=False):
        image = annotation.image
        file_name = image.original_name
        if full_path and image.image_object.local_image:
            file_name = image.image_object.local_image

        return {
            'file_name': file_name,
            'height': image.image_object.height,
            'width': image.image_object.width,
            'tags': list(AnnotationTags.objects.filter(annotation=annotation).values_list('tag__name', flat=True).all()),
            'task': self.task.value,
        }

    def new_parse_base_annotation(
        self, image: DatasetImage, annotation_set: AnnotationSet = None, full_path=False
    ):
        file_name = image.original_name
        if full_path and image.image_object.local_image:
            file_name = image.image_object.local_image

        tags = []
        if annotation_set:
            annotation = NewAnnotation.objects.filter(image=image, annotation_set=annotation_set).first()
            if annotation:
                tags = annotation.tags

        return {
            'file_name': file_name,
            'height': image.image_object.height,
            'width': image.image_object.width,
            'tags': tags,
            'task': self.task.value,
        }

    def export_annotations(
        self,
        annotation_set,
        export_coordinates='pixel',
        full_path=False,
        export_classes=False,
        export_without_annotations=False,
    ):
        if self.task.name != annotation_set.task.type:
            return

        output = []
        annotated = set()
        for annotation in Annotation.objects.filter(annotation_set=annotation_set):
            if not annotation.has_annotation():
                continue
            annotated.add(annotation.image.id)
            output.append(
                self.parse_annotation(
                    annotation,
                    export_coordinates=export_coordinates,
                    full_path=full_path,
                    export_classes=export_classes,
                )
            )

        if export_without_annotations:
            for img in DatasetImage.objects.filter(dataset=annotation_set.dataset).all():
                if img.id not in annotated:
                    output.append(self.empty_annotation(img, annotation_set, full_path=full_path))

        return JSON.buffer(output)

    @abstractmethod
    def parse_annotation(self, annotation, export_coordinates='pixel', full_path=False, export_classes=False):
        raise NotImplementedError

    def empty_annotation(self, image: DatasetImage, annotation_set: AnnotationSet, full_path=False):
        result = self.new_parse_base_annotation(image, annotation_set, full_path=full_path)
        result['annotations'] = []
        return result


class RemoJsonObjectDetection(RemoBase):
    task = TaskType.object_detection
    expected_keys = {
        *RemoBase.expected_keys,
        'item.annotations.item.classes',
        'item.annotations.item.bbox',
    }

    def parse_annotation_object_classes(self, obj):
        classes = obj.classes.values_list('name', flat=True).all()
        return self.encode_classes(classes)

    def parse_annotation_objects(self, objs, export_coordinates='pixel'):
        annotations = []
        for obj in objs:
            annotations.append(self.parse_annotation_object(obj, export_coordinates=export_coordinates))
        return annotations

    def parse_annotation(self, annotation, export_coordinates='pixel', full_path=False, export_classes=False):
        result = self.parse_base_annotation(annotation, full_path=full_path)
        result['annotations'] = self.parse_annotation_objects(
            AnnotationObject.objects.filter(annotation=annotation), export_coordinates=export_coordinates
        )
        return result

    def parse_annotation_object(self, obj, export_coordinates='pixel'):
        _min, _max = obj.coordinates
        if export_coordinates == 'pixel':
            bbox = {
                'xmin': int(_min['x']),
                'ymin': int(_min['y']),
                'xmax': int(_max['x']),
                'ymax': int(_max['y']),
            }
        else:  # if export_coordinates == 'percent':
            width, height = obj.annotation.image.dimensions()
            bbox = {
                'xmin': float(_min['x']) / width,
                'ymin': float(_min['y']) / height,
                'xmax': float(_max['x']) / width,
                'ymax': float(_max['y']) / height,
            }

        return {'classes': self.parse_annotation_object_classes(obj), 'bbox': bbox}


class RemoJsonInstanceSegmentation(RemoJsonObjectDetection):
    task = TaskType.instance_segmentation
    expected_keys = {
        *RemoBase.expected_keys,
        'item.annotations.item.classes',
        'item.annotations.item.segments',
    }

    def parse_annotation_object(self, obj, export_coordinates='pixel'):
        if export_coordinates == 'pixel':
            segments = [{'x': int(p['x']), 'y': int(p['y'])} for p in obj.coordinates]
        else:  # if export_coordinates == 'percent'
            width, height = obj.annotation.image.dimensions()
            segments = [{'x': float(p['x']) / width, 'y': float(p['y']) / height} for p in obj.coordinates]

        return {'classes': self.parse_annotation_object_classes(obj), 'segments': segments}


class RemoJsonImageClassification(RemoBase):
    task = TaskType.image_classification
    expected_keys = {
        *RemoBase.expected_keys,
        'item.classes',
    }

    def parse_annotation_classes(self, annotation):
        classes = (
            AnnotationClassRel.objects.filter(annotation=annotation)
            .values_list('annotation_class__name', flat=True)
            .all()
        )
        return self.encode_classes(classes)

    def parse_annotation(self, annotation, export_coordinates='pixel', full_path=False, export_classes=False):
        result = self.parse_base_annotation(annotation, full_path=full_path)
        result['classes'] = self.parse_annotation_classes(annotation)
        return result
