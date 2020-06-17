#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
import datetime
from django_szuprefix_saas.saas.models import Party
from django.contrib.auth.models import User


class Todo(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "待办"
        ordering = ('-create_time',)
        unique_together = ('user', 'target_type', 'target_id', 'name')

    party = models.ForeignKey(Party, verbose_name=Party._meta.verbose_name, related_name="todos",
                                   on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name=User._meta.verbose_name, related_name="todos",
                                   on_delete=models.PROTECT)
    name = models.CharField("名称", max_length=255)
    target_type = models.ForeignKey('contenttypes.ContentType', verbose_name='目标', null=True, blank=True,
                                   on_delete=models.PROTECT)
    target_id = models.PositiveIntegerField(verbose_name='目标编号', null=True, blank=True)
    target = GenericForeignKey('target_type', 'target_id')
    url = models.CharField("链接", max_length=255)
    is_done = models.BooleanField("已办", default=False)
    expiration = models.DateTimeField("过期时间", blank=True, null=True, default=datetime.datetime(2048, 8, 8))
    update_time = models.DateTimeField("修改时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

#
# class History(models.Model):
#     class Meta:
#         verbose_name_plural = verbose_name = "待办历史"
#         ordering = ('-create_time',)
#
#     party = models.ForeignKey(Party, verbose_name=Party._meta.verbose_name, related_name="todos")
#     user = models.ForeignKey(User, verbose_name=User._meta.verbose_name, related_name="todos")
#     name = models.CharField("名称", max_length=64)
#     url = models.CharField("链接", max_length=255)
#     todolist_type = models.IntegerField("类型", default=None)
#     is_done = models.BooleanField("是否已办", default=False)
#     is_notice = models.BooleanField("是否通知", default=False)
#     set_lock = models.BooleanField("设为锁定", default=False)
#     expiration = models.DateTimeField("过期时间", blank=True, null=True, default=datetime.datetime(2088, 8, 8))
#     update_time = models.DateTimeField("修改时间", auto_now=True)
#     create_time = models.DateTimeField("创建时间", auto_now_add=True)