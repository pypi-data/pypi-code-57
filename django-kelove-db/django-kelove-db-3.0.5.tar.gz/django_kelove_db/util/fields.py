# ==================================================================
#       文 件 名: fields.py
#       概    要: Fields
#       作    者: IT小强 
#       创建时间: 6/18/20 3:54 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

import json

from django.core.exceptions import ValidationError
from django.db.models import Field, TextField
from django.utils.translation import gettext_lazy as _

from .forms import JSONFormField, EditorMdFormField
from .helper import get_kelove_databases_settings


class JSONField(Field):
    """
    JSON 字段
    """
    description = _("JSON")

    default_error_messages = {
        'json_decode_error': _('JSON decode error'),
        'invalid': _('“%(value)s” type must be either dict,list,tuple,set,json string.'),
        'invalid_nullable': _('“%(value)s” type must be either dict,list,tuple,set,json string or None.'),
    }

    def __init__(self, *args, **kwargs):
        kwargs['field_settings'] = kwargs.get('field_settings', {})
        self._field_settings = {**get_kelove_databases_settings('JSON_FIELD_SETTINGS', {}), **kwargs['field_settings']}
        kwargs.pop('field_settings')
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def formfield(self, **kwargs):
        kwargs['form_class'] = JSONFormField
        kwargs['field_settings'] = self._field_settings
        return super().formfield(**kwargs)

    def to_python(self, value):

        if self.null and value in [None, '']:
            return None

        if value in self.empty_values:
            return {}

        if isinstance(value, dict) or isinstance(value, list):
            return value

        if isinstance(value, tuple) or isinstance(value, set):
            return list(value)

        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                raise ValidationError(
                    self.error_messages['json_decode_error'],
                    code='invalid',
                    params={'value': value},
                )

        raise ValidationError(
            self.error_messages['invalid_nullable' if self.null else 'invalid'],
            code='invalid',
            params={'value': value},
        )

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None:
            return None
        return json.dumps(self.to_python(value))


class EditorMdField(TextField):
    """

    """
    description = _("Editor Md")

    def __init__(self, *args, **kwargs):
        kwargs['field_settings'] = kwargs.get('field_settings', {})
        self._field_settings = {
            **get_kelove_databases_settings('EDITOR_MD_FIELD_SETTINGS', {}),
            **kwargs['field_settings']
        }
        kwargs.pop('field_settings')
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['form_class'] = EditorMdFormField
        kwargs['field_settings'] = self._field_settings
        return super().formfield(**kwargs)
