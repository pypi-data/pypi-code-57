import csv
import logging
from typing import Tuple, List

from .annotation import AnnotationObjectDetection
from .base import BaseAnnotationFormat, DatasetImageMapping
from .knowledge_graph import KnowledgeGraph
from remo_app.remo.models import AnnotationSet, DatasetImage, Task, Class
from remo_app.remo.api.constants import TaskType, AnnotationSetType
from remo_app.remo.entities.boundary_box import BoundaryBox
from remo_app.remo.utils import utils
from remo_app.remo.utils.progress_info import ProgressInfo

logger = logging.getLogger('remo_app')


class OpenImagesBase(BaseAnnotationFormat):
    """Abstract base class for OpenImages formats"""

    required_columns = set()

    def __init__(self, data_fp=None, categories_fp=None):
        super().__init__(data_fp)
        self.categories = {} if categories_fp is None else self.parse_categories(categories_fp)

    @staticmethod
    def parse_categories(categories_fp):
        """
        Parses file with categories into dict: category_id - category_name
        :return: dict {category_id: category_name}
        """
        pos = categories_fp.tell()
        categories_fp.seek(0)

        categories = {}
        csv_file = csv.reader(categories_fp, delimiter=',')
        for row in csv_file:
            if len(row) >= 2:
                label = str(row[0]).strip()
                class_name = str(row[1]).strip()
                categories[label] = class_name

        categories_fp.seek(pos)
        return categories

    @classmethod
    def is_applicable(cls, path, fp):
        if utils.is_system_file(path):
            return False

        if not path.endswith('.csv'):
            return False

        pos = fp.tell()
        fp.seek(0)
        csv_reader = csv.reader(fp, delimiter=',')
        cols = next(csv_reader)
        fp.seek(pos)
        return cls.required_columns.issubset(cols)

    def get_category(self, id, default=None):
        if not id.startswith("/m/"):
            return default

        category = self.categories.get(id)
        if category is None:
            category = KnowledgeGraph.search_category(id)

        if category:
            self.categories[id] = category
            return category

        return default


class OpenImagesCsvObjectDetection(OpenImagesBase):
    task = TaskType.object_detection
    required_columns = {'ImageID', 'Source', 'LabelName', 'Confidence', 'XMin', 'XMax', 'YMin', 'YMax', 'IsOccluded',
                        'IsTruncated', 'IsGroupOf', 'IsDepiction', 'IsInside'}

    @staticmethod
    def parse_filename(header: List[str], row: List[str]) -> str:
        try:
            return row[header.index('ImageID')]
        except ValueError:
            return ''

    @staticmethod
    def parse_bbox(header: List[str], row: List[str]) -> List[float]:
        """
        Parses box coordinates
        :param header: csv file header
        :param row: csv file row
        :return: xmin: float, ymin: float, xmax: float, ymax: float
        """
        values = []
        for column in ('XMin', 'YMin', 'XMax', 'YMax'):
            try:
                val = row[header.index(column)]
                val = float(val)
            except ValueError:
                val = 0
            values.append(val)
        return values

    def parse_annotation_object(self, header: List[str], row: List[str]) -> Tuple[str, BoundaryBox]:
        try:
            category_id = row[header.index('LabelName')]
        except ValueError:
            category_id = 'N/A'

        box = BoundaryBox(*self.parse_bbox(header, row))
        return category_id, box

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

        progress = ProgressInfo(rows_number, items='annotation objs')

        header = None
        while not header:
            header = next(csv_reader)

        annotation = None
        rows_skipped = 0
        skipped_dimensions = set()

        for row in csv_reader:
            progress.report()

            image_name = self.parse_filename(header, row)
            if not image_name:
                self.add_error(f'Failed parse image name from row: {row}')
                rows_skipped += 1
                continue

            db_image_id, image_name = self.get_image_id(image_name, images_mapping)
            if db_image_id is None:
                rows_skipped += 1
                self.add_error(f'Cannot find image in db {image_name}')
                continue

            if not annotation:
                annotation = AnnotationObjectDetection(image_name)
            elif annotation.source_image_id != image_name:
                yield annotation
                annotation = AnnotationObjectDetection(image_name)

            category_id, box = self.parse_annotation_object(header, row)

            dimensions = imgs.get(db_image_id)
            if not dimensions:
                skipped_dimensions.add(f'id:{db_image_id} - {image_name}')
                continue

            box.scale_coordinates(*dimensions)
            obj_id = annotation.add_annotation_object(box.data)

            category = self.get_category(category_id)
            class_name, err = self.decode_class(category)
            self.add_error(err)
            if not class_name:
                continue

            annotation.add_class(obj_id, class_name)

        self.data_fp.seek(pos)

        if skipped_dimensions:
            self.add_error(f'Failed to find dimensions for images in db: {skipped_dimensions}')

        if rows_skipped:
            self.add_error(f'Skipped #{rows_skipped} rows')

        if annotation:
            yield annotation

    def fetch_images_mapping(self, dataset_id):
        return DatasetImageMapping(dataset_id)

    def save_annotations(self, dataset_id, user_id, images_mapping: dict, annotation_set_id=None, skip_new_classes=False) -> int:
        """
        Save annotations to database
        :param dataset_id: Dataset id
        :param user_id: User id for creating annotation sets
        :param images_mapping: mapping {internal_image_id: DatasetImage_database_id}
        :return: count of saved annotations
        """
        classes_mapping = dict(Class.objects.values_list('name', 'id'))
        annotation_set = self.get_or_create_annotation_set(dataset_id, user_id, annotation_set_id=annotation_set_id)

        return sum(
            self.save_single_annotation(annotation, images_mapping, classes_mapping, annotation_set.id, skip_new_classes)
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

    def save_single_annotation(self, annotation, images_mapping, classes_mapping, annotation_set_id, skip_new_classes=False):
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

    @staticmethod
    def scale_coordinate_down(coordinate, factor):
        if coordinate:
            return round(coordinate / factor, 6)
        return coordinate

    def export_annotations(self, dataset_image_ids):
        """Create a dataframe ready to be exported as a CSV file."""
        annotation_cols = ['ImageID', 'Source', 'LabelName', 'Confidence', 'XMin', 'XMax', 'YMin', 'YMax', 'IsOccluded',
                           'IsTruncated', 'IsGroupOf', 'IsDepiction', 'IsInside']
        category_cols = ['category_id', 'category_name']

        # TODO: rewrite with csv lib

        # annotations = pd.DataFrame(columns=annotation_cols)
        # categories = pd.DataFrame(columns=category_cols)
        #
        # task = Task.objects.get(type=self.task.name)
        # for image_id in dataset_image_ids:
        #     image = DatasetImage.objects.get(id=image_id)
        #     annotation_set = AnnotationSet.objects.get(dataset=image.dataset, task=task)
        #     annotation = Annotation.objects.get(image=image_id, annotation_set=annotation_set)
        #     annotation_objs = AnnotationObject.objects.filter(annotation=annotation)
        #
        #     width, height = image.image_object.width, image.image_object.height
        #
        #     for obj in annotation_objs:
        #         category_name = obj.classes.first()
        #         category_id = KnowledgeGraph.search_category_id(category_name)
        #
        #         annotation_row = {
        #             'ImageID': annotation.image.original_name.replace('.jpg', ''),
        #             'Source': 'freeform',
        #             'LabelName': category_id,
        #             'Confidence': 1,
        #             'XMin': self.scale_coordinate_down(obj.coordinates[0].get('x'), width),
        #             'XMax': self.scale_coordinate_down(obj.coordinates[1].get('x'), width),
        #             'YMin': self.scale_coordinate_down(obj.coordinates[0].get('y'), height),
        #             'YMax': self.scale_coordinate_down(obj.coordinates[1].get('y'), height),
        #             'IsOccluded': '',
        #             'IsTruncated': '',
        #             'IsGroupOf': '',
        #             'IsDepiction': '',
        #             'IsInside': ''
        #         }
        #         category_row = {
        #             'category_id': category_id,
        #             'category_name': category_name
        #         }
        #
        #         annotation_frame = pd.DataFrame([annotation_row], columns=annotation_cols)
        #         category_frame = pd.DataFrame([category_row], columns=category_cols)
        #         annotations = pd.concat([annotations, annotation_frame], axis=0, ignore_index=True)
        #         categories = pd.concat([categories, category_frame], axis=0, ignore_index=True)
        #
        # annotations = (annotations.to_csv(index=None))
        # categories = (categories.drop_duplicates().to_csv(index=None))
        # return annotations, categories
