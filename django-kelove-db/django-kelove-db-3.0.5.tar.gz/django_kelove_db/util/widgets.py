# ==================================================================
#       文 件 名: widgets.py
#       概    要: Widgets
#       作    者: IT小强 
#       创建时间: 6/18/20 10:54 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

import json

from django.forms import Widget, Media


class JSONWidget(Widget):
    """
    JSON 表单组件
    https://github.com/josdejong/jsoneditor
    """
    template_name = 'django_kelove_db/forms/json.html'

    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['field_settings'] = json.dumps(attrs.get('field_settings', {}))
        super().__init__(attrs)

    def _get_media(self):
        return Media(
            css={"all": ('django_kelove_db/jsoneditor/jsoneditor.min.css',)},
            js=('django_kelove_db/jsoneditor/jsoneditor.min.js',)
        )

    media = property(_get_media)


class EditorMdWidget(Widget):
    """
    EditorMd 表单组件
    https://github.com/pandao/editor.md
    """
    template_name = 'django_kelove_db/forms/editor_md.html'

    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['field_settings'] = json.dumps(attrs.get('field_settings', {}))
        super().__init__(attrs)

    def _get_media(self):
        return Media(
            css={"all": ('django_kelove_db/editor_md/css/editormd.min.css',)},
            js=('django_kelove_db/jquery/jquery-3.5.1.min.js', 'django_kelove_db/editor_md/editormd.min.js')
        )

    media = property(_get_media)
