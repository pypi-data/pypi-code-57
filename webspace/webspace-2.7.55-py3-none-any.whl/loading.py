from django.conf import settings
from django.utils.module_loading import import_string


def get_class(module_label, classname, module_prefix='oscar.apps'):
    return get_classes(module_label, [classname], module_prefix)[0]


def get_class_loader():
    return import_string(settings.OSCAR_DYNAMIC_CLASS_LOADER)


def get_classes(module_label, classnames, module_prefix='webspace'):
    class_loader = get_class_loader()
    return class_loader(module_label, classnames, module_prefix)
