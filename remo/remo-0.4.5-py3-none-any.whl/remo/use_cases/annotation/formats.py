from .simple_instance_segmentation import PlainCsvInstanceSegmentation
from .simple_image_classification import PlainCsvImageClassification
from .simple_open_images import PlainCsvObjectDetection
from .coco import CocoJsonInstanceSegmentation, CocoJsonObjectDetection
from .json import RemoJsonObjectDetection, RemoJsonInstanceSegmentation, RemoJsonImageClassification
from .open_images import OpenImagesCsvObjectDetection
from .pascal_voc import PascalVocXmlObjectDetection
from .imagenet import PascalVocXmlImageClassification

formats = {}
for annotation_format in [PascalVocXmlImageClassification, OpenImagesCsvObjectDetection, PascalVocXmlObjectDetection,
                          CocoJsonObjectDetection, CocoJsonInstanceSegmentation, PlainCsvObjectDetection,
                          PlainCsvImageClassification, PlainCsvInstanceSegmentation]:
    arr = formats.get(annotation_format.task, [])
    arr.append(annotation_format)
    formats[annotation_format.task] = arr


def get_supported_formats(task):
    return formats.get(task, [])


export_formats = {
    'json': {
        RemoJsonObjectDetection.task: RemoJsonObjectDetection,
        RemoJsonInstanceSegmentation.task: RemoJsonInstanceSegmentation,
        RemoJsonImageClassification.task: RemoJsonImageClassification,
    },
    'coco': {
        CocoJsonObjectDetection.task: CocoJsonObjectDetection,
        CocoJsonInstanceSegmentation.task: CocoJsonInstanceSegmentation,
    },
    'csv': {
        PlainCsvImageClassification.task: PlainCsvImageClassification,
        PlainCsvObjectDetection.task: PlainCsvObjectDetection,
        PlainCsvInstanceSegmentation.task: PlainCsvInstanceSegmentation,
    }
}


def get_exporter(task, name='json'):
    exporters = export_formats.get(name)
    if exporters:
        return exporters.get(task)
    return
