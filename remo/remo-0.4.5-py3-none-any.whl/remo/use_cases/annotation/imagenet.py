import logging
from xml.etree.ElementTree import parse

from .annotation import AnnotationImageClassification
from .imagenet_cache import ImagenetMetadata
from .base import LazyDatasetImageMapping
from .pascal_voc import PascalVOCBase
from remo_app.remo.api.constants import TaskType

logger = logging.getLogger('remo_app')


class PascalVocXmlImageClassification(PascalVOCBase):
    task = TaskType.image_classification
    required_tags = {'filename', 'size', 'object'}

    @staticmethod
    def parse_filename(root):
        try:
            return root.find('filename').text

        except AttributeError:
            return

    @staticmethod
    def parse_category_id(obj):
        try:
            category_id = obj.find('name').text
            return category_id
        except AttributeError:
            return

    def retrieve_annotations(self):
        pos = self.data_fp.tell()
        self.data_fp.seek(0)
        tree = parse(self.data_fp)
        root = tree.getroot()

        image_name = self.parse_filename(root)

        if not image_name:
            self.data_fp.seek(pos)
            return
        # image_name = f'{image_name}.JPEG'
        annotation = AnnotationImageClassification(image_name, image_name=image_name)
        score = 1.0

        for obj in root.findall('object'):
            category_id = self.parse_category_id(obj)
            if not category_id:
                continue

            categories = ImagenetMetadata.search_category(category_id)
            if len(categories):
                annotation.add_class(categories, score)
            else:
                class_name, err = self.decode_class(category_id)
                self.add_error(err)
                if not class_name:
                    continue

                annotation.add_class(class_name, score)

        self.data_fp.seek(pos)
        return [annotation]

    def fetch_images_mapping(self, dataset_id):
        return LazyDatasetImageMapping(dataset_id)
