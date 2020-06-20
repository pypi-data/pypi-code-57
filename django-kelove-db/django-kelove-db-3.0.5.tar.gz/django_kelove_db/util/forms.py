# ==================================================================
#       文 件 名: forms.py
#       概    要: Forms
#       作    者: IT小强 
#       创建时间: 6/18/20 10:56 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.forms.fields import Field

from .widgets import JSONWidget, EditorMdWidget


class JSONFormField(Field):
    """
    JSON 表单字段
    """

    def __init__(self, **kwargs):
        self._field_settings = kwargs['field_settings'] = kwargs.get('field_settings', {})
        kwargs.pop('field_settings')
        kwargs['widget'] = JSONWidget({'field_settings': self._field_settings})
        super().__init__(**kwargs)


class EditorMdFormField(Field):
    """
    EditorMd 表单字段
    """

    def __init__(self, **kwargs):
        self._field_settings = kwargs['field_settings'] = kwargs.get('field_settings', {})
        kwargs.pop('field_settings')
        kwargs.pop('max_length')
        kwargs['widget'] = EditorMdWidget({'field_settings': self._field_settings})
        super().__init__(**kwargs)
