#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
import datetime

from django_szuprefix.utils.modelutils import JSONField
from django_szuprefix_saas.saas.models import Party
from django.contrib.auth.models import User
from . import choices

class Verify(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "审核"
        ordering = ('-create_time',)

    party = models.ForeignKey(Party, verbose_name=Party._meta.verbose_name, related_name="verifies",
                                   on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name='用户', related_name="verifies", null=True, blank=True,
                                   on_delete=models.PROTECT)
    category = models.CharField("类别", max_length=64)
    name = models.CharField("名称", max_length=256)
    target_type = models.ForeignKey('contenttypes.ContentType', verbose_name='目标', null=True, blank=True,
                                   on_delete=models.PROTECT)
    target_id = models.PositiveIntegerField(verbose_name='目标编号', null=True, blank=True)
    target = GenericForeignKey('target_type', 'target_id')
    content = JSONField("内容", default={})
    status = models.PositiveSmallIntegerField("状态", choices=choices.CHOICES_STATUS, default=choices.STATUS_PENDING)
    operator = models.ForeignKey(User, verbose_name='审核员', related_name="verifies_operated", null=True, blank=True,
                                   on_delete=models.PROTECT)
    reply = models.CharField("答复", max_length=256, blank=True, default='')
    update_time = models.DateTimeField("修改时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __unicode__(self):
        return self.name