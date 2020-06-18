# ==================================================================
#       文 件 名: forms.py
#       概    要: Forms
#       作    者: IT小强 
#       创建时间: 6/18/20 10:56 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.forms.fields import Field

from .widgets import JSONWidget


class JSONFormField(Field):
    """
     JSON 表单字段
    """

    def __init__(self, **kwargs):
        self._json_editor_config = kwargs['json_editor_config'] = kwargs.get('json_editor_config', {})
        kwargs.pop('json_editor_config')
        kwargs['widget'] = JSONWidget({'json_editor_config': self._json_editor_config})
        super().__init__(**kwargs)
