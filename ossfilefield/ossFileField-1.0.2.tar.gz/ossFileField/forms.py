#! -*- coding: utf-8 -*-
from django import forms

from .widgets import OssFileWidget


class OssFileFormField(forms.URLField):
    # 默认值设置
    file_type = 'image'
    max_file_size = ''
    widget = OssFileWidget

    def __init__(self, *args, **kwargs):
        kwargs["widget"] = OssFileWidget(
            attrs={
                'file_type': self.file_type,
                'max_file_size': self.max_file_size
            }
        )
        super(OssFileFormField, self).__init__(*args, **kwargs)
