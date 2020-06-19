import csv
import io
import logging
import os
from typing import Tuple, List

from remo_app.remo.models.annotation import NewAnnotation
from .open_images import OpenImagesBase
from .annotation import AnnotationInstanceSegmentation
from .base import DatasetImageMapping
from remo_app.remo.models import AnnotationSet, DatasetImage, Task, Class
from remo_app.remo.api.constants import TaskType, AnnotationSetType
from remo_app.remo.utils import utils
from remo_app.remo.utils.progress_info import ProgressInfo

logger = logging.getLogger('remo_app')


class PlainCsvInstanceSegmentation(OpenImagesBase):
    task = TaskType.instance_segmentation

    # required fields
    file_name = 'file_name'
    class_name = 'class_name'
    coordinates = 'coordinates'

    file_name_variations = {
        'image', 'image_id', 'image id', 'file_name', 'filename', 'file', 'file name', 'file_path', 'path',
        'file path'
    }

    class_name_variations = {
        'class', 'label', 'name', 'class_name', 'class name', 'label_name', 'label name', 'category',
        'classes'
    }

    coordinates_variations = {
        'coordinates',
    }

    variations = {
        file_name: file_name_variations,
        class_name: class_name_variations,
        coordinates: coordinates_variations,
    }

    @classmethod
    def is_applicable(cls, path, fp):
        if utils.is_system_file(path):
            return False

        _, ext = os.path.splitext(path)
        if ext not in ('.csv', '.txt'):
            return False

        pos = fp.tell()
        fp.seek(0)
        csv_reader = csv.reader(fp, delimiter=',')
        header = None
        while not header:
            header = next(csv_reader)
        fp.seek(pos)

        header = cls.read_header(header)
        n = len(cls.variations)
        return len(header) == n and len(set(header.values())) == n

    @classmethod
    def match_field_name(cls, name):
        for field_name, field_variations in cls.variations.items():
            if name.lower() in field_variations:
                return field_name

    @classmethod
    def read_header(cls, cols):
        ids = {}
        for idx, col in enumerate(cols):
            field = cls.match_field_name(col)
            if field:
                ids[field] = idx
        return ids

    def parse_filename(self, header: dict, row: List[str]) -> str:
        try:
            return row[header[self.file_name]]
        except ValueError:
            return ''

    def parse_coordinates(self, header: dict, row: List[str]) -> List[float]:
        """
        Parses coordinates
        :param header: csv file header
        :param row: csv file row
        :return: xmin: float, ymin: float, xmax: float, ymax: float
        """
        try:
            coordinates = row[header[self.coordinates]]
            coordinates = coordinates.split(';')
            values = list(map(float, coordinates))
        except ValueError:
            values = [0, 0]
        return values

    def parse_annotation_object(self, header: dict, row: List[str]) -> Tuple[List[str], List[float]]:
        try:
            category_ids = row[header[self.class_name]]
            category_ids = category_ids.split(';')
        except ValueError:
            category_ids = ['N/A']

        categories = [self.get_category(category_id, default=category_id) for category_id in category_ids]
        coordinates = self.parse_coordinates(header, row)
        return categories, coordinates

    def retrieve_annotations(self, images_mapping: dict = None, dataset_id=None):
        pos = self.data_fp.tell()
        self.data_fp.seek(0)
        csv_reader = csv.reader(self.data_fp, delimiter=',')
        rows_number = sum(1 for line in csv_reader) - 1
        self.data_fp.seek(0)

        imgs = {}
        for obj in DatasetImage.objects.filter(dataset_id=dataset_id).all():
            image = obj.image_object
            imgs[obj.id] = (image.width, image.height)

        # logger.info(f'Retrieving annotations: {self.__class__.__name__}')

        progress = ProgressInfo(rows_number, items='annotation objs')

        header = None
        while not header:
            header = next(csv_reader)
        header = self.read_header(header)

        annotation = None
        rows_skipped = 0
        for row in csv_reader:
            if len(row) == 0:
                continue

            progress.report(rows_skipped=rows_skipped)
            image_name = self.parse_filename(header, row)
            if not image_name:
                rows_skipped += 1
                logger.error(f'Failed parse image name from row {row}')
                continue

            db_image_id, image_name = self.get_image_id(image_name, images_mapping)
            if db_image_id is None:
                rows_skipped += 1
                self.add_error(f'Cannot find image in db {image_name}')
                continue

            if not annotation:
                annotation = AnnotationInstanceSegmentation(image_name, image_name=image_name)
            elif annotation.source_image_id != image_name:
                yield annotation
                annotation = AnnotationInstanceSegmentation(image_name, image_name=image_name)

            annotation_obj = self.parse_annotation_object(header, row)
            if not annotation_obj:
                rows_skipped += 1
                logger.error(f'Failed parse annotation_obj from row {row}')
                continue

            dimensions = imgs.get(db_image_id)
            if not dimensions:
                rows_skipped += 1
                self.add_error(f'Cannot find image in db {image_name}')
                continue
            image_width, image_height = dimensions
            categories, coordinates = annotation_obj
            data = [
                    {'x': float(x), 'y': float(y)}
                    for x, y in zip(coordinates[::2], coordinates[1::2])
                ]  # reshape with 2
            if any(v['x'] > 1 or v['y'] > 1 for v in data):
                return
            for v in data:
                v['x'] = v['x'] * image_width
                v['y'] = v['y'] * image_height

            obj_id = annotation.add_annotation_object(data)
            class_names, err = self.decode_class(categories)
            self.add_error(err)

            if not class_names:
                rows_skipped += 1
                continue
            for class_name in class_names:
                annotation.add_class(obj_id, class_name)

        self.data_fp.seek(pos)

        if annotation:
            yield annotation

    def fetch_images_mapping(self, dataset_id):
        return DatasetImageMapping(dataset_id)

    def save_annotations(self, dataset_id, user_id, images_mapping: dict, annotation_set_id=None,
                         skip_new_classes=False) -> int:
        """
        Save annotations to database
        :param dataset_id: Dataset id
        :param user_id: User id for creating annotation sets
        :param images_mapping: mapping {internal_image_id: DatasetImage_database_id}
        :return: count of saved annotations
        """
        classes_mapping = dict(Class.objects.values_list('name', 'id'))
        annotation_set = self.get_or_create_annotation_set(dataset_id, user_id,
                                                           annotation_set_id=annotation_set_id)

        # logger.info(f'Started annotation upload on Dataset {dataset_id} for task: {self.task}')
        return sum(
            self.save_single_annotation(annotation, images_mapping, classes_mapping, annotation_set.id,
                                        skip_new_classes)
            for annotation in self.retrieve_annotations(images_mapping, dataset_id)
        )

    def get_or_create_annotation_set(self, dataset_id, user_id, annotation_set_id=None):
        if annotation_set_id:
            return AnnotationSet.objects.get(id=annotation_set_id)

        task = Task.objects.get(type=self.task.name)
        annotation_set = AnnotationSet.objects.filter(dataset_id=dataset_id, task=task).first()
        if not annotation_set:
            annotation_set = AnnotationSet.objects.create(
                name=f'{self.task.value}',
                type=AnnotationSetType.image.value,
                task=task,
                user_id=user_id,
                dataset_id=dataset_id
            )

        return annotation_set

    def save_single_annotation(self, annotation, images_mapping, classes_mapping, annotation_set_id,
                               skip_new_classes=False):
        db_image_id, image_name = self.get_image_id(annotation.source_image_id, images_mapping)
        if db_image_id is None:
            self.add_error(f'Cannot find image in db {annotation.image_name}')
            return 0

        annotation.write_to_db(
            db_image_id,
            annotation_set_id,
            classes_mapping,
            skip_new_classes
        )
        return 1


    def export_annotations(self, annotation_set, export_coordinates='pixel', full_path=False, export_classes=False, export_without_annotations=False):
        """
        Exports annotations in CSV format
        """
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['file_name', 'classes', 'coordinates'])

        annotated = set()
        for annotation in NewAnnotation.objects.filter(annotation_set=annotation_set):
            if not annotation.has_annotation():
                continue

            annotated.add(annotation.image.id)
            file_name = self.get_file_name(annotation.image, full_path)
            width, height = annotation.image.dimensions()
            for obj in annotation.data.get('objects', []):
                coordinates = obj.get('coordinates', [])
                points = self.export_coordinates(coordinates, width, height, export_coordinates)
                classes = obj.get('classes', [])
                encoded = self.encode_classes(classes)
                classes_csv = "; ".join(encoded)
                points_csv = "; ".join(map(str, points))
                writer.writerow([file_name, classes_csv, points_csv])

        if export_without_annotations:
            for img in DatasetImage.objects.filter(dataset=annotation_set.dataset).all():
                if img.id not in annotated:
                    writer.writerow([self.get_file_name(img, full_path), '', ''])

        return output.getvalue()

    def export_coordinates(self, coordinates, width, height, export_coordinates='pixel'):
        points = []
        mapper = {
            'pixel': lambda p: (int(p['x']), int(p['y'])),
            'percent': lambda p: (float(p['x']) / width, float(p['y']) / height)
        }.get(export_coordinates)

        for p in coordinates:
            points.extend(mapper(p))
        return points

    def get_file_name(self, image: DatasetImage, full_path=False):
        file_name = image.original_name

        if full_path and image.image_object.local_image:
            file_name = image.image_object.local_image
        return file_name
