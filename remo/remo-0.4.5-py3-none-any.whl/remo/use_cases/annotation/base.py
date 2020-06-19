import logging
import os
from abc import ABCMeta, abstractmethod
from typing import List

from remo_app.remo.models import AnnotationSet, Class, Task, DatasetImage
from remo_app.remo.api.constants import AnnotationSetType, TaskType
from remo_app.remo.utils.progress_info import ProgressInfo

logger = logging.getLogger('remo_app')


class LazyDatasetImageMapping:
    def __init__(self, dataset_id):
        self.dataset_id = dataset_id
        self.cache = {}

    def get(self, image_name):
        id = self.cache.get(image_name)
        if id:
            return id

        obj = DatasetImage.objects.filter(dataset_id=self.dataset_id, original_name=image_name).first()
        if obj:
            self.cache[image_name] = obj.id
            return obj.id
        return None


class DatasetImageMapping(LazyDatasetImageMapping):
    def __init__(self, dataset_id):
        super().__init__(dataset_id)
        for obj in DatasetImage.objects.filter(dataset_id=self.dataset_id).all():
            self.cache[obj.original_name] = obj.id


class BaseAnnotationFormat(metaclass=ABCMeta):
    """
    Convert annotations data in specific format to annotations records
    """
    task = None

    def __init__(self, data_fp=None):
        self.data_fp = data_fp
        self.errors = []
        self.folder = None
        self.class_encoding = None

    def __str__(self):
        return self.__class__.__name__

    @classmethod
    @abstractmethod
    def is_applicable(cls, path, fp) -> bool:
        """
        Checks whether concrete converter accepts file with given type.
        File pointer may be moved after call
        :param path: relative path of file
        :param fp: file pointer
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def retrieve_annotations(self, images_mapping: dict = None):
        """Returns AnnotationRecord* objects generator"""
        raise NotImplementedError

    @abstractmethod
    def fetch_images_mapping(self, dataset_id) -> dict:
        """
        Get images mapping
        {internal_image_id: DatasetImage_database_id}

        Note: this function can just do query to database or fetch
        images from external CDN depending on format white take much
        time. Therefore it's better not to assume time of function
        executing
        :param dataset_id: Database object id
        :return: {internal_image_id: DatasetImage_database_id}
        """
        raise NotImplementedError

    @staticmethod
    def get_image_id(image_name, images_mapping):
        db_image_id = images_mapping.get(image_name)
        if db_image_id:
            return db_image_id, image_name

        if not isinstance(image_name, str):
            return None, image_name

        _, ext = os.path.splitext(image_name)
        if ext:
            return images_mapping.get(image_name), image_name

        formats = ['.jpg', '.png', '.jpeg', 'tif', '.tiff']
        formats += list(map(lambda v: v.upper(), formats))
        for ext in formats:
            name = "{}{}".format(image_name, ext)
            db_image_id = images_mapping.get(name)
            if db_image_id:
                return db_image_id, name

        return None, image_name

    def decode_class(self, label_names: List[str]) -> (List[str], str):
        """
        Decodes label name to class name based on class encoding

        Return:
            class name
            error
        """
        if not self.class_encoding:
            return label_names, None

        try:
            return list(map(self.class_encoding.decode_class, label_names)), None
        except Exception as err:
            return label_names, str(err)

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

    def encode_classes(self, classes):
        encoded = []
        for class_name in classes:
            label, error = self.encode_class(class_name)
            self.add_error(error)
            encoded.append(label)

        return encoded

    def add_error(self, err):
        if err:
            self.errors.append(err)

    def save_annotations(self, dataset_id, user_id, images_mapping, annotation_set_id=None, skip_new_classes=False) -> int:
        """
        Save annotations to database
        :param dataset_id: Dataset id
        :param user_id: User id for creating annotation sets
        :param images_mapping: mapping {internal_image_id: DatasetImage_database_id}
        :return: count of saved annotations
        """
        annotation_sets = {TaskType(s.task.name): s
                           for s in
                           AnnotationSet.objects.filter(dataset_id=dataset_id)}  # {cv_task: AnnotationSet object}
        if annotation_set_id:
            s = AnnotationSet.objects.get(id=annotation_set_id)
            annotation_sets[TaskType(s.task.name)] = s

        classes_mapping = dict(Class.objects.values_list('name', 'id'))

        counter = 0
        annotations = self.retrieve_annotations()
        progress = ProgressInfo(len(annotations), 'annotations')
        # logger.info(f'Started annotation upload on Dataset {dataset_id} for task: {self.task}')
        for annotation in annotations:
            progress.report()
            db_image_id, image_name = self.get_image_id(annotation.source_image_id, images_mapping)
            if image_name != annotation.source_image_id:
                annotation.source_image_id = image_name

            if db_image_id is None:
                self.add_error(f'Cannot find image in db {annotation.image_name}')
                continue

            if annotation.task_type not in annotation_sets:
                task = Task.objects.get(type=annotation.task_type.name)
                annotation_sets[annotation.task_type] = AnnotationSet.objects.create(
                    name=f'{annotation.task_type.value}',
                    type=AnnotationSetType.image.value,
                    task=task,
                    user_id=user_id,
                    dataset_id=dataset_id
                )

            annotation.write_to_db(
                db_image_id,
                annotation_sets[annotation.task_type].id,
                classes_mapping,
                skip_new_classes
            )
            counter += 1

        return counter
