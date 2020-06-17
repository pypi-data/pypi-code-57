from .file_conversion import yaml2dict, py2dict, json2dict
import os.path as osp


class DictWrapper(dict):
    """
    Wrap a dictionary object so that we can access
    values as attributes
    """

    def __missing__(self, name):
        raise KeyError(name)

    def __getattr__(self, name):
        value = super(DictWrapper, self).__getitem__(name)
        return value

    def __setattr__(self, name, value):
        super(DictWrapper, self).__setitem__(name, value)


class ConfigLoader(object):
    """
    Load config from files in python/yaml/json format
    """

    @staticmethod
    def from_file(file_path: str):
        assert isinstance(file_path, str)
        extension = osp.splitext(file_path)[1].lower()

        if extension == '.py':
            dictionary = py2dict(file_path)
        elif extension == '.yaml':
            dictionary = yaml2dict(file_path)
        elif extension == '.json':
            dictionary = json2dict(file_path)
        else:
            raise Exception('File type is not supported yet.')

        return DictWrapper(dictionary)

    @staticmethod
    def from_dict(dictionary: dict):
        assert isinstance(dictionary, dict)
        return DictWrapper(dictionary)
