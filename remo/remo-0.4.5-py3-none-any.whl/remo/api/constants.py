from enum import Enum


class EnumChoices(Enum):
    @classmethod
    def choices(cls):
        """
        'choices' must be an iterable containing
        (actual value, human readable name) tuples
        """
        return tuple([(item.name, item.value) for item in cls])

    @classmethod
    def choices_subset(cls, values):
        return tuple([(item.name, item.value) for item in cls if item.value in values])

    @classmethod
    def by_name(cls, name):
        if name in cls._member_map_:
            return cls._member_map_[name]

        # still not found -- try _missing_ hook
        return cls._missing_(name)


class StrEnumChoices(str, EnumChoices):
    """Enum where members are also (and must be) strs"""

    def __str__(self):
        return self.value


class IntEnumChoices(int, EnumChoices):
    """Enum where members are also (and must be) ints"""

    @classmethod
    def choices(cls):
        """
        'choices' must be an iterable containing
        (actual value, human readable name) tuples
        """
        return tuple([(item.value, item.name) for item in cls])

    def __str__(self):
        return self.name


class AnnotationStatus(IntEnumChoices):
    not_annotated = -1
    skipped = 0
    done = 1


default_status = AnnotationStatus.not_annotated


class AnnotationSetType(StrEnumChoices):
    image = 'Image'


class TaskType(StrEnumChoices):
    object_detection = 'Object detection'
    instance_segmentation = 'Instance segmentation'
    image_classification = 'Image classification'


class ToolType(StrEnumChoices):
    rectangle = 'rectangle'
    polygon = 'polygon'


task_tools_mapping = {
    TaskType.object_detection: ToolType.rectangle,
    TaskType.instance_segmentation: ToolType.polygon,
}


class JobStatus(StrEnumChoices):
    unknown = 'unknown'
    queued = 'queued'
    in_progress = 'in progress'
    done = 'done'
    failed = 'failed'


class JobType(StrEnumChoices):
    unknown = 'unknown'
    upload_dataset = 'upload dataset'
