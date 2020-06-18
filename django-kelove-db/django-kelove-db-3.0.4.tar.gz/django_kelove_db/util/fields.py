# ==================================================================
#       文 件 名: fields.py
#       概    要: Fields
#       作    者: IT小强 
#       创建时间: 6/18/20 3:54 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

import json

from django.db.models import Field
from django.utils.translation import gettext_lazy as _

from .forms import JSONFormField


class JSONField(Field):
    """
    JSON 字段
    """
    description = _("JSON")

    def __init__(self, *args, **kwargs):
        self._json_editor_config = kwargs['json_editor_config'] = kwargs.get('json_editor_config', {})
        kwargs.pop('json_editor_config')
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def formfield(self, **kwargs):
        kwargs['form_class'] = JSONFormField
        kwargs['json_editor_config'] = self._json_editor_config
        return super().formfield(**kwargs)

    def to_python(self, value):

        if self.null and value in [None, '']:
            return None

        if isinstance(value, dict) or isinstance(value, list):
            return value

        if isinstance(value, tuple):
            return list(value)

        if isinstance(value, str):
            return json.loads(value)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None:
            return None
        return json.dumps(self.to_python(value))
