# ==================================================================
#       文 件 名: views.py
#       概    要: 视图
#       作    者: IT小强 
#       创建时间: 6/9/20 5:58 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.shortcuts import render
from django.views.generic import View

from .backends.mysql.doc import Doc
from .util import helper


class MySQLDatabaseDoc(View):
    """
    在线数据库文档
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.doc_title = helper.get_kelove_databases_settings('DOC_TITLE', '数据库设计文档')

    def get(self, request):
        """
        处理GET 请求
        :param request:
        :return:
        """
        doc = Doc()
        doc_data = doc.get_database_doc_data()

        return render(request, 'django_kelove_db/doc_db.html', {"apps": doc_data, 'title': self.doc_title})
