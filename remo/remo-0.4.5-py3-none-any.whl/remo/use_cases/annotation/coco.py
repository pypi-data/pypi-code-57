import io
import logging
from typing import List, Dict

import ijson
import requests
from django.conf import settings
from ijson.backends.python import UnexpectedSymbol

from .annotation import AnnotationInstanceSegmentation, AnnotationObjectDetection
from .base import BaseAnnotationFormat
from .coco_categories import COCO_CATEGORIES
from remo_app.remo.api.constants import TaskType
from remo_app.remo.models import DatasetImage, AnnotationObject, Annotation
from remo_app.remo.utils import utils
from .export_tags import JSON
from .json import BaseExporter
from ...unpacker.unpackers import Downloader

logger = logging.getLogger('remo_app')


class CocoBase(BaseAnnotationFormat):
    """Abstract base class for COCO formats"""

    expected_keys = set()

    def __init__(self, data_fp=None):
        super().__init__(data_fp)
        self.coco_images = {}  # coco_id: file_name

    @classmethod
    def is_applicable(cls, path, fp):
        if utils.is_system_file(path):
            return False

        if not path.endswith('.json'):
            return False

        pos = fp.tell()
        fp.seek(0)

        viewed_keys = set()
        ok = False
        try:
            for current, event, value in ijson.parse(fp):
                if current:
                    viewed_keys.add(current)

                if viewed_keys >= cls.expected_keys:
                    ok = True
                    break
        except ijson.backend.UnexpectedSymbol:
            pass

        fp.seek(pos)
        return ok


class CocoJsonInstanceSegmentation(CocoBase):
    task = TaskType.instance_segmentation
    annotation_class = AnnotationInstanceSegmentation
    expected_keys = {
        'annotations.item.id',
        'annotations.item.image_id',
        'annotations.item.category_id',
        'annotations.item.segmentation',
        'annotations.item.area',
        'annotations.item.bbox',
        'annotations.item.iscrowd',
    }

    def retrieve_annotations(self, images_mapping: dict = None):
        pos = self.data_fp.tell()
        categories = self._parse_categories()

        self.data_fp.seek(0)
        # logger.info(f'Retrieving annotations: {self.__class__.__name__}')

        annotations = {}  # Annotations dict {image_id: annotation}
        for item in self._annotation_items():
            image_id, category_id = item['image_id'], item['category_id']
            category = categories.get(category_id, 'none')

            class_name, err = self.decode_class(category)
            self.add_error(err)
            if not class_name:
                class_name = 'none'

            annotation = annotations.get(image_id)
            if not annotation:
                annotation = self.annotation_class(
                    image_id, image_name=self.coco_images.get(image_id, image_id)
                )
                annotations[image_id] = annotation
            self._build_annotation(item, annotation, class_name)

        self.data_fp.seek(pos)
        return annotations.values()

    def _build_annotation(self, item, annotation, category):
        segmentation = item['segmentation']  # type: list
        if isinstance(segmentation, list) and item['iscrowd'] == 0:  # polygon
            # TODO: fix store segmentations together
            for segmentation_item in segmentation:
                obj_id = annotation.add_annotation_object(
                    [
                        {'x': float(x), 'y': float(y)}
                        for x, y in zip(segmentation_item[::2], segmentation_item[1::2])
                    ]  # reshape with 2
                )
                annotation.add_class(obj_id, category)

    def _parse_categories(self):
        self.data_fp.seek(0)

        categories = {}
        items = ijson.items(self.data_fp, 'categories.item')
        while True:
            try:
                category = next(items)
            except (ijson.backends.python.UnexpectedSymbol, StopIteration):
                break
            categories[category['id']] = category['name']

        if not categories:
            raise Exception('Empty list of categories')

        return categories

    def _annotation_items(self):
        self.data_fp.seek(0)
        items = ijson.items(self.data_fp, 'annotations.item')
        while True:
            try:
                yield next(items)
            except (ijson.backends.python.UnexpectedSymbol, StopIteration):
                break

    def fetch_images_mapping(self, dataset_id):
        pos = self.data_fp.tell()

        mapping = {}  # {coco_image_id: db_image_id}
        images = self._parse_images()
        for img in images:
            coco_image_id, file_name = img['id'], img['file_name']
            self.coco_images[coco_image_id] = file_name

            urls = [img[key] for key in ('coco_url', 'flickr_url', 'url') if key in img]
            db_image_id, err = self._get_dataset_image_id(dataset_id, file_name, urls)
            if db_image_id:
                mapping[coco_image_id] = db_image_id
            self.add_error(err)

        self.data_fp.seek(pos)
        return mapping

    def download_images(self, dataset_id, download_dir) -> Dict[str, List[str]]:
        pos = self.data_fp.tell()

        errors = {}
        images = self._parse_images()
        for img in images:
            coco_image_id, file_name = img['id'], img['file_name']
            if self._find_dataset_image(dataset_id, file_name):
                continue

            urls = [str(img[key]).strip() for key in ('coco_url', 'flickr_url', 'url') if key in img]
            urls = list(filter(lambda url: len(url), urls))

            if not urls:
                errors[file_name] = ['No valid url']
                continue

            for url in urls:
                try:
                    Downloader(url, download_dir, filename=file_name, verbose=False).download()
                except Exception as err:
                    img_errors = errors.get(file_name, [])
                    img_errors.append(f'Failed to download from URL: {url}')
                    errors[file_name] = img_errors
                    continue
                break

        self.data_fp.seek(pos)
        return errors

    def _parse_images(self):
        self.data_fp.seek(0)
        images = ijson.items(self.data_fp, 'images.item')
        result = []
        while True:
            try:
                result.append(next(images))
            except (UnexpectedSymbol, StopIteration):
                break
        return result

    def _get_dataset_image_id(self, dataset_id, file_name, urls):
        image_id = self._find_dataset_image(dataset_id, file_name)
        if image_id:
            return image_id, ''

        buffer, err = self._download_image(file_name, urls)
        if err:
            return None, err

        return self._save_image_from_buffer(buffer, dataset_id, file_name)

    @staticmethod
    def _find_dataset_image(dataset_id, file_name):
        dataset_image = DatasetImage.objects.filter(dataset_id=dataset_id, original_name=file_name).first()
        if dataset_image:
            return dataset_image.id

    def _download_image(self, file_name, urls):
        buffer = io.BytesIO()
        logger.debug('Downloading image %s', file_name)
        buffer, downloaded_bytes = self._download_to_file(urls, buffer)

        msg = ''
        if downloaded_bytes == 0:
            msg = "Failed to download image {}".format(file_name)
            logger.error(msg)
            buffer = None
        return buffer, msg

    def _save_image_from_buffer(self, buffer, dataset_id, file_name):
        buffer.seek(0)
        dataset_image = DatasetImage(dataset_id=dataset_id, folder=self.folder)

        msg = ''
        image_id = None
        try:
            dataset_image = dataset_image.upload_image_from_buffer(buffer, file_name)
            if dataset_image.is_new():
                dataset_image.save()
            image_id = dataset_image.id
        except Exception as err:
            msg = "Failed to upload image: {}, ERROR: {}".format(file_name, err)
            logger.error(msg)

        return image_id, msg

    def _download_to_file(self, urls, fp):
        """
        Download data from urls list which will be successful.
        The function does not follows redirects
        :param urls: list with urls to try
        :param fp: file pointer
        :return: (file pointer, downloaded_bytes)
        """
        downloaded_bytes = 0
        urls = list(filter(lambda url: len(url), map(lambda url: str(url).strip(), urls)))

        if not len(urls):
            logger.warning('Empty URL list')
            return fp, downloaded_bytes

        for url in urls:
            fp.seek(0)
            fp.truncate(0)
            try:
                downloaded_bytes = self._download(url, fp)
                if downloaded_bytes:
                    break
            except FileSizeExceeds:
                logger.warning('URL %s: file size exceeds MAX_EXTERNAL_DOWNLOAD_IMAGE_SIZE, abort', url)

        return fp, downloaded_bytes

    def _download(self, url, fp):
        chunk_size = 8192
        downloaded_bytes = 0
        try:
            with requests.get(url, stream=True) as resp:
                if resp.status_code != 200:
                    return downloaded_bytes

                content_size = int(resp.headers.get('content-length', 0))
                if content_size > settings.MAX_EXTERNAL_DOWNLOAD_IMAGE_SIZE:
                    raise FileSizeExceeds()

                for chunk in resp.iter_content(chunk_size=chunk_size):
                    if chunk:
                        if downloaded_bytes + len(chunk) > settings.MAX_EXTERNAL_DOWNLOAD_IMAGE_SIZE:
                            raise FileSizeExceeds()

                        fp.write(chunk)
                        downloaded_bytes += len(chunk)
        except Exception as err:
            logger.error(f'Failed to download from URL: {url}. Error: {err}')
        return downloaded_bytes

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

        exporter = coco_exporter(self.task)
        return exporter.export_annotations(
            annotation_set,
            export_coordinates=export_coordinates,
            full_path=full_path,
            export_classes=export_classes,
            export_without_annotations=export_without_annotations,
        )


def coco_exporter(task):
    if task == TaskType.instance_segmentation:
        return COCOInstanceSegmentationExporter()
    elif task == TaskType.object_detection:
        return COCOObjectDetectionExporter()


class CategoriesLookup:
    key_id = 'id'
    key_name = 'name'
    key_supercategory = 'supercategory'

    def __init__(self):
        self.lookup = {}
        self.coco_lookup = {
            category[self.key_name]: {
                self.key_id: category[self.key_id],
                self.key_supercategory: category[self.key_supercategory],
            }
            for category in COCO_CATEGORIES
        }

        self.max_id = max(category[self.key_id] for category in COCO_CATEGORIES)

    def get_category_id(self, name):
        category = self.lookup.get(name)
        if category:
            return category[self.key_id]

        category = self.coco_lookup.get(name)
        if category:
            self.lookup[name] = category
            return category[self.key_id]

        self.max_id += 1
        self.lookup[name] = {
            self.key_id: self.max_id,
            self.key_supercategory: name,
        }
        return self.max_id

    def export(self):
        return [
            {
                self.key_supercategory: category[self.key_supercategory],
                self.key_id: category[self.key_id],
                self.key_name: name,
            }
            for name, category in self.lookup.items()
        ]


class COCOInstanceSegmentationExporter(BaseExporter):
    def __init__(self):
        super().__init__()
        self.categories = CategoriesLookup()

    def gen_empty_meta_info(self):
        return {
            'info': {
                'description': '',
                'url': '',
                'version': '',
                'year': '',
                'contributor': '',
                'date_created': '',
            },
            'licences': [{'url': '', 'id': '', 'name': ''}],
        }

    def parse_image_info(self, image, full_path=False):

        file_name = image.original_name
        if full_path and image.image_object.local_image:
            file_name = image.image_object.local_image

        return {
            'license': 0,
            'file_name': file_name,
            'height': image.image_object.height,
            'width': image.image_object.width,
            'date_captured': '',
            'url': '',
            'id': image.id,
        }

    def parse_segments(self, coordinates):
        return [self.parse_segment(coordinates)]

    def calc_area(self, image, segments):
        # height = image.image_object.height
        # width = image.image_object.width

        # import pycocotools.mask as mask
        # rles = mask.frPyObjects(segments, height, width)
        # rle = mask.merge(rles)
        # area = mask.area([rle])
        # return float(area[0])
        return 0

    def parse_segment(self, coordinates):
        segment = []
        for point in coordinates:
            segment.append(point.get('x', 0))
            segment.append(point.get('y', 0))
        return segment

    def get_coordinates(self, annotation, obj, export_coordinates='pixel'):
        image = annotation.image

        coordinates = []
        width, height = image.dimensions()
        for p in obj.coordinates:
            if export_coordinates == 'pixel':
                coordinates.append({'x': int(p['x']), 'y': int(p['y'])})
            elif export_coordinates == 'percent':
                coordinates.append({'x': float(p['x']) / width, 'y': float(p['y']) / height})
        return coordinates

    def get_bbox_segments_area(self, annotation, obj, export_coordinates='pixel'):
        image = annotation.image
        coordinates = self.get_coordinates(annotation, obj, export_coordinates=export_coordinates)
        segments = self.parse_segments(coordinates)
        area = self.calc_area(image, segments)
        bbox = self.calc_bbox(segments)
        return bbox, segments, area

    def empty_annotation(self, image: DatasetImage):
        return {
            'segmentation': [],
            'area': 0,
            'iscrowd': 0,
            'image_id': image.id,
            'bbox': [],
            'id': 0,
            'category_id': 0,
        }

    def parse_annotation_object(self, annotation, obj, export_coordinates='pixel'):
        bbox, segments, area = self.get_bbox_segments_area(
            annotation, obj, export_coordinates=export_coordinates
        )
        result = {
            'segmentation': segments,
            'area': area,
            'iscrowd': 0,
            'image_id': annotation.image.id,
            'bbox': bbox,
            'id': obj.id,
        }

        # TODO: check if we need convert to lower case, I guess it's neeed only for COCO categories
        classes = self.lower_case(self.parse_annotation_object_classes(obj))
        classes = self.encode_classes(classes)

        category_id = 0
        if len(classes):
            category_id = self.categories.get_category_id(classes[0])
            unique_classes = set(classes[1:])
            if classes[0] in unique_classes:
                unique_classes.remove(classes[0])
                other_categories = [self.categories.get_category_id(name) for name in unique_classes]
                result['other_categories'] = other_categories
        result['category_id'] = category_id

        return result

    @staticmethod
    def parse_annotation_object_classes(obj):
        return obj.classes.values_list('name', flat=True).all()

    @staticmethod
    def lower_case(items):
        return list(map(lambda x: x.lower(), items))

    @staticmethod
    def calc_bbox(segments):
        total_min_x, total_max_x, total_min_y, total_max_y = [None] * 4
        for segment in segments:
            min_x, max_x = min(segment[::2]), max(segment[::2])
            min_y, max_y = min(segment[1::2]), max(segment[1::2])

            if not total_min_x or min_x < total_min_x:
                total_min_x = min_x
            if not total_max_x or max_x > total_max_x:
                total_max_x = max_x
            if not total_min_y or min_y < total_min_y:
                total_min_y = min_y
            if not total_max_y or max_y > total_max_y:
                total_max_y = max_y

        x, y, width, height = total_min_x, total_min_y, total_max_x - total_min_x, total_max_y - total_min_y
        return [x, y, width, height]

    def export_annotations(
        self,
        annotation_set,
        export_coordinates='pixel',
        full_path=False,
        export_classes=False,
        export_without_annotations=False,
    ):
        output = self.gen_empty_meta_info()
        images = []
        annotations = []
        annotated = set()

        for annotation in Annotation.objects.filter(annotation_set=annotation_set):
            if not annotation.has_annotation():
                continue

            annotated.add(annotation.image.id)
            images.append(self.parse_image_info(annotation.image, full_path=full_path))
            for obj in AnnotationObject.objects.filter(annotation=annotation):
                annotations.append(
                    self.parse_annotation_object(annotation, obj, export_coordinates=export_coordinates)
                )

        if export_without_annotations:
            for img in DatasetImage.objects.filter(dataset=annotation_set.dataset).all():
                if img.id not in annotated:
                    images.append(self.parse_image_info(img, full_path=full_path))
                    annotations.append(
                        self.empty_annotation(img)
                    )

        output['images'] = images
        output['annotations'] = annotations
        output['categories'] = self.categories.export()
        return JSON.buffer(output)


class COCOObjectDetectionExporter(COCOInstanceSegmentationExporter):
    def get_bbox_segments_area(self, annotation, obj, export_coordinates='pixel'):
        coordinates = self.get_coordinates(annotation, obj, export_coordinates=export_coordinates)
        segments = self.parse_segments(coordinates)
        area = self.calc_area(coordinates)
        bbox = self.calc_bbox(coordinates)
        return bbox, segments, area

    def unpack_coordinates(self, coordinates):
        xmin = coordinates[0].get('x', 0)
        ymin = coordinates[0].get('y', 0)
        xmax = coordinates[1].get('x', 0)
        ymax = coordinates[1].get('y', 0)
        return xmin, ymin, xmax, ymax

    def parse_segment(self, coordinates):
        xmin, ymin, xmax, ymax = self.unpack_coordinates(coordinates)
        return [xmin, ymin, xmin, ymax, xmax, ymax, xmax, ymin]

    def calc_area(self, coordinates):
        xmin, ymin, xmax, ymax = self.unpack_coordinates(coordinates)
        height = ymax - ymin
        width = xmax - xmin
        return height * width

    def calc_bbox(self, coordinates):
        xmin, ymin, xmax, ymax = self.unpack_coordinates(coordinates)
        height = ymax - ymin
        width = xmax - xmin
        return [xmin, ymin, width, height]


class FileSizeExceeds(Exception):
    pass


class CocoJsonObjectDetection(CocoJsonInstanceSegmentation):
    task = TaskType.object_detection
    annotation_class = AnnotationObjectDetection

    def _build_annotation(self, item, annotation, category):
        bbox = item['bbox']  # type: list
        x, y, width, height = bbox
        obj_id = annotation.add_annotation_object(
            [{'x': float(x), 'y': float(y)}, {'x': float(x + width), 'y': float(y + height)},]
        )
        annotation.add_class(obj_id, category)
