from abc import ABCMeta, abstractmethod

from remo_app.remo.api.constants import StrEnumChoices
from remo_app.remo.use_cases.annotation.imagenet_cache import parse_categories
from remo_app.remo.use_cases.annotation.knowledge_graph import KnowledgeGraph


class ClassEncodingType(StrEnumChoices):
    custom = 'custom'
    autodetect = 'autodetect'
    google_knowledge_graph = 'GoogleKnowledgeGraph'
    word_net = 'WordNet'


types = [ClassEncodingType.word_net, ClassEncodingType.google_knowledge_graph]


class AbstractClassEncoding(metaclass=ABCMeta):

    @abstractmethod
    def encode_class(self, class_name: str) -> str:
        """
        Converts class name to label or id
        """
        raise NotImplementedError

    @abstractmethod
    def decode_class(self, label_name: str) -> str:
        """
        Converts label or class id to class name
        """
        raise NotImplementedError


class BaseClassEncoding(AbstractClassEncoding):
    # def __init__(self):
    #     """
    #     decoding - dict of pairs {label: class}
    #     encoding - dict of pairs {class: label}
    #     """
    #     self.decoding = {}
    #     self.encoding = {}

    def encode_class(self, class_name: str) -> str:
        if class_name in self.encoding:
            return self.encoding[class_name]
        raise Exception(f'Class {class_name} not found in encoding list')

    def decode_class(self, label_name: str) -> str:
        if label_name in self.decoding:
            return self.decoding[label_name]
        raise Exception(f'Label {label_name} not found in decoding list')


class CustomClassEncoding(BaseClassEncoding):

    def __init__(self, classes: dict):
        """
        classes - dict of pairs {label: class}
        """
        self.decoding = classes
        self.encoding = {
            class_name: label_name
            for label_name, class_name in classes.items()
        }


class WordNetClassEncoding(BaseClassEncoding):

    def __init__(self):
        self.decoding = parse_categories()
        self.encoding = {}
        for label_name, classes in self.decoding.items():
            for class_name in classes:
                self.encoding[class_name] = label_name


class GoogleKnowledgeGraphClassEncoding(AbstractClassEncoding):

    def encode_class(self, class_name: str) -> str:
        category_id = KnowledgeGraph.search_category_id(class_name)
        if category_id:
            return category_id
        raise Exception(f'Class {class_name} not found in encoding list')

    def decode_class(self, label_name: str) -> str:
        class_name = KnowledgeGraph.search_category(label_name)
        if class_name:
            return class_name
        raise Exception(f'Label {label_name} not found in decoding list')
