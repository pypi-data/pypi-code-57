# ==================================================================
#       文 件 名: model.py
#       概    要: 模型基类
#       作    者: IT小强 
#       创建时间: 6/8/20 2:38 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from json import dumps

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel as BaseMPTTModel

from .helper import get_kelove_databases_settings, STATUS_CHOICES


class Model(models.Model):
    """
    数据模型基类
    """

    class Meta:
        abstract = True


class CreatedUserModel(Model):
    """
    添加创建用户外键
    """

    # 创建用户
    created_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('created_user'),
        related_name="%(app_label)s_%(class)s_created_user_set",
        on_delete=get_kelove_databases_settings('FOREIGN_DELETE_TYPE', models.PROTECT),
        db_constraint=get_kelove_databases_settings('DB_CONSTRAINT_USER', False),
        null=True,
        blank=True,
        editable=get_kelove_databases_settings('USER_EDITABLE', False),
        default=None
    )

    class Meta:
        abstract = True


class UpdatedUserModel(Model):
    """
    添加更新用户外键
    """

    # 更新用户
    updated_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('updated_user'),
        related_name="%(app_label)s_%(class)s_updated_user_set",
        on_delete=get_kelove_databases_settings('FOREIGN_DELETE_TYPE', models.PROTECT),
        db_constraint=get_kelove_databases_settings('DB_CONSTRAINT_USER', False),
        null=True,
        blank=True,
        editable=get_kelove_databases_settings('USER_EDITABLE', False),
        default=None
    )

    class Meta:
        abstract = True


class CreatedTimeModel(Model):
    """
    添加创建时间
    """

    # 创建时间
    created_time = models.DateTimeField(verbose_name=_('created_time'), auto_now_add=True, editable=True)

    class Meta:
        abstract = True


class UpdatedTimeModel(Model):
    """
    添加更新时间
    """

    # 更新时间
    updated_time = models.DateTimeField(verbose_name=_('updated_time'), auto_now=True)

    class Meta:
        abstract = True


class StatusModel(Model):
    """
    添加状态字段
    """

    STATUS_CHOICES = get_kelove_databases_settings('STATUS_CHOICES', STATUS_CHOICES)

    # 状态
    status = models.IntegerField(
        verbose_name=_('status'),
        null=False,
        default=0,
        choices=STATUS_CHOICES,
        help_text=_('status') + dumps(dict(STATUS_CHOICES), ensure_ascii=False)
    )

    class Meta:
        abstract = True


class EnabledModel(Model):
    """
    添加是否启用字段
    """

    # 是否启用
    enabled = models.BooleanField(
        verbose_name=_('enabled'),
        default=False,
        db_index=True,
    )

    class Meta:
        abstract = True


class SortModel(Model):
    """
    添加排序字段
    """

    # 排序
    sort = models.IntegerField(
        verbose_name=_('sort'),
        null=False,
        default=0,
    )

    class Meta:
        abstract = True


class NoUserModel(CreatedTimeModel, UpdatedTimeModel, SortModel, StatusModel, EnabledModel):
    """
    数据模型基类（不包括创建用户、更新用户字段）
    """

    class Meta:
        abstract = True


class NoTimeModel(CreatedUserModel, UpdatedUserModel, SortModel, StatusModel, EnabledModel):
    """
    数据模型基类（不包括创建时间、更新时间字段）
    """

    class Meta:
        abstract = True


class OnlyTimeModel(CreatedTimeModel, UpdatedTimeModel):
    """
    数据模型基类（仅包含时间字段）
    """

    class Meta:
        abstract = True


class OnlyUserModel(CreatedUserModel, UpdatedUserModel):
    """
    数据模型基类（仅包含创建、更新用户字段）
    """

    class Meta:
        abstract = True


class AllModel(OnlyUserModel, OnlyTimeModel, StatusModel, EnabledModel, SortModel):
    """
    数据模型基类(添加全部公用字段)
    """

    class Meta:
        abstract = True


class MPTTModel(BaseMPTTModel):
    """
    树形数据模型基类
    """

    level = models.PositiveIntegerField(verbose_name=_('level'), editable=False)

    class Meta:
        abstract = True
