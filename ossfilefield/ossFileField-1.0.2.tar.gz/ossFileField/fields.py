#! -*- coding: utf-8 -*-
from django.db import models

from .widgets import OssFileWidget
from .forms import OssFileFormField


class OssFileField(models.FileField):
    widget_clz = OssFileWidget
    form_field_clz = OssFileFormField

    def __init__(self, verbose_name=None, name=None, file_type='image', max_file_size=None, **kwargs):
        self.file_type = file_type
        self.max_file_size = max_file_size
        super(OssFileField, self).__init__(verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        self.form_field_clz.file_type = self.file_type
        self.form_field_clz.max_file_size = self.max_file_size
        kwargs.update({
            'form_class': self.form_field_clz,
            'widget': self.widget_clz(attrs={'file_type': self.file_type, 'max_file_size': self.max_file_size})
        })
        return super(OssFileField, self).formfield(**kwargs)
