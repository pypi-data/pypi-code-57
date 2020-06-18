# ==================================================================
#       文 件 名: urls.py
#       概    要: 路由
#       作    者: IT小强 
#       创建时间: 6/9/20 5:57 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.urls import path

from .views import MySQLDatabaseDoc

urlpatterns = [
    path('mysql', MySQLDatabaseDoc.as_view()),
]
