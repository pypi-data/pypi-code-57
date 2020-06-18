# ==================================================================
#       文 件 名: helper.py
#       概    要: 助手工具
#       作    者: IT小强 
#       创建时间: 6/8/20 2:37 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from importlib import import_module

from django.conf import settings

STATUS_CHOICES: list = [(-1, '草稿'), (0, '待审'), (1, '通过'), (2, '驳回')]


def load_object(path: str):
    """
    Load an object given its absolute object path, and return it.
    object can be a class, function, variable or an instance.
    path ie: 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware'
    """

    dot = path.rindex('.')
    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)
    return getattr(mod, name)


def get_kelove_databases_settings(key: str = None, default=None):
    """
    获取配置
    :param key:
    :param default:
    :return:
    """
    try:
        kelove_databases_settings = settings.KELOVE_DATABASES
    except AttributeError:
        kelove_databases_settings = {}

    if not isinstance(kelove_databases_settings, dict):
        kelove_databases_settings = {}

    default_kelove_databases_settings = {
        'FOREIGN_DELETE_TYPE': 'django.db.models.deletion.PROTECT',
        'DB_CONSTRAINT': False,
        'DB_CONSTRAINT_USER': False,
        'USER_EDITABLE': False,
        'STATUS_CHOICES': STATUS_CHOICES
    }
    kelove_databases_settings = {**default_kelove_databases_settings, **kelove_databases_settings}

    if isinstance(kelove_databases_settings['FOREIGN_DELETE_TYPE'], str):
        kelove_databases_settings['FOREIGN_DELETE_TYPE'] = load_object(kelove_databases_settings['FOREIGN_DELETE_TYPE'])

    if key is None:
        return kelove_databases_settings
    else:
        return kelove_databases_settings.get(key, default)
