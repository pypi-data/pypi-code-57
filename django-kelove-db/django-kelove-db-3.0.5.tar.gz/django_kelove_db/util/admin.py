# ==================================================================
#       文 件 名: admin.py
#       概    要: 后台管理基类
#       作    者: IT小强 
#       创建时间: 6/15/20 4:21 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from django.contrib import admin

from mptt.admin import MPTTModelAdmin


class ModelAdmin(admin.ModelAdmin):
    """
    后台管理基类
    """


class ModelAdminWithUser(ModelAdmin):
    """
    后台管理基类（自动写入创建用户ID和更新用户ID）
    """

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        自动写入创建用户ID和更新用户ID
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        if request.user:
            user = request.user
            obj.updated_user = user
            if not change:
                obj.created_user = user
        super().save_model(request, obj, form, change)


class ModelAdminMPTT(MPTTModelAdmin):
    """
    后台管理基类(支持树形结构)
    """


class ModelAdminMPTTWithUser(ModelAdminMPTT):
    """
     后台管理基类(支持树形结构)（自动写入创建用户ID和更新用户ID）
    """

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        自动写入创建用户ID和更新用户ID
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        if request.user:
            user = request.user
            obj.updated_user = user
            if not change:
                obj.created_user = user
        super().save_model(request, obj, form, change)
