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
    """
    template_name = 'django_kelove_db/forms/json.html'

    json_editor_config = {
        "mode": "code",
        "modes": ["code", "form", "text", "tree", "view", "preview"],
    }

    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['json_editor_config'] = json.dumps({**self.json_editor_config, **attrs.get('json_editor_config', {})})
        super().__init__(attrs)

    def _get_media(self):
        return Media(
            css={"all": ('django_kelove_db/jsoneditor/jsoneditor.min.css',)},
            js=('django_kelove_db/jsoneditor/jsoneditor.min.js',)
        )

    media = property(_get_media)
