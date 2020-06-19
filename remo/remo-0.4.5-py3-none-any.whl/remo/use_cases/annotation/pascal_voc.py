import logging
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import Element, SubElement, tostring

from .annotation import AnnotationObjectDetection
from .base import BaseAnnotationFormat, LazyDatasetImageMapping
from remo_app.remo.models import DatasetImage, Task, AnnotationObject, Annotation, AnnotationSet
from remo_app.remo.api.constants import TaskType
from remo_app.remo.utils import utils

logger = logging.getLogger('remo_app')


class PascalVOCBase(BaseAnnotationFormat):
    """Abstract base class for PascalVOC formats"""

    required_tags = set()

    @classmethod
    def is_applicable(cls, path, fp):
        if utils.is_system_file(path):
            return False

        if not path.endswith('.xml'):
            return False

        pos = fp.tell()
        fp.seek(0)
        tree = parse(fp)
        root = tree.getroot()
        tags = {node.tag for node in root.iter('*')}
        fp.seek(pos)
        return cls.required_tags.issubset(tags)


class PascalVocXmlObjectDetection(PascalVOCBase):
    task = TaskType.object_detection
    required_tags = {'filename', 'size', 'object'}

    @staticmethod
    def parse_filename(root):
        try:
            return root.find('filename').text

        except AttributeError:
            return

    @staticmethod
    def parse_boundary_box(bndbox):
        xmin, ymin, xmax, ymax = [float(bndbox.find(val).text) for val in ('xmin', 'ymin', 'xmax', 'ymax')]
        return [{'x': xmin, 'y': ymin}, {'x': xmax, 'y': ymax}]

    @staticmethod
    def parse_object(obj):
        try:
            category = obj.find('name').text
            box = PascalVocXmlObjectDetection.parse_boundary_box(obj.find('bndbox'))
            return category, box
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

        annotation = AnnotationObjectDetection(image_name, image_name=image_name)

        for obj in root.findall('object'):
            annotation_obj = self.parse_object(obj)
            if not annotation_obj:
                continue
            category, box = annotation_obj
            obj_id = annotation.add_annotation_object(box)

            class_name, err = self.decode_class(category)
            self.add_error(err)
            if not class_name:
                continue

            annotation.add_class(obj_id, class_name)

        self.data_fp.seek(pos)
        return [annotation]

    def fetch_images_mapping(self, dataset_id):
        return LazyDatasetImageMapping(dataset_id)

    def export_annotations(self, dataset_image_ids):
        """Create a ready to be exported xml file."""
        task = Task.objects.get(type=self.task.name)
        xml_list = []
        for image_id in dataset_image_ids:
            image = DatasetImage.objects.get(id=image_id)
            annotation_set = AnnotationSet.objects.get(dataset=image.dataset, task=task)
            annotation = Annotation.objects.get(image=image_id, annotation_set=annotation_set)
            annotation_objs = AnnotationObject.objects.filter(annotation=annotation)

            width = image.image_object.width
            height = image.image_object.height
            folder = image.folder
            fileName = annotation.image.original_name

            node_root = Element('annotation')
            if folder is not None:
                node_folder = SubElement(node_root, 'folder')
                node_folder.text = str(folder)

            node_filename = SubElement(node_root, 'filename')
            node_filename.text = fileName

            node_size = SubElement(node_root, 'size')
            node_width = SubElement(node_size, 'width')
            node_width.text = str(width)

            node_height = SubElement(node_size, 'height')
            node_height.text = str(height)

            node_depth = SubElement(node_size, 'depth')
            node_depth.text = 'Unspecified'

            for obj in annotation_objs:
                name = obj.classes.first()

                node_object = SubElement(node_root, 'object')
                node_name = SubElement(node_object, 'name')
                node_name.text = str(name)
                node_bndbox = SubElement(node_object, 'bndbox')
                node_xmin = SubElement(node_bndbox, 'xmin')
                node_xmin.text = str(int(obj.coordinates[0].get('x', None)))
                node_ymin = SubElement(node_bndbox, 'ymin')
                node_ymin.text = str(int(obj.coordinates[0].get('y', None)))
                node_xmax = SubElement(node_bndbox, 'xmax')
                node_xmax.text = str(int(obj.coordinates[1].get('x', None)))
                node_ymax = SubElement(node_bndbox, 'ymax')
                node_ymax.text = str(int(obj.coordinates[1].get('y', None)))

            xml = tostring(node_root, method="xml")
            xml_list.append(xml)
        return xml_list
