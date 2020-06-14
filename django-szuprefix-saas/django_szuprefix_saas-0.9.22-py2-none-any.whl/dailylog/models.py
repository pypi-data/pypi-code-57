# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from django.db import models
from django.utils.functional import cached_property
from django.contrib.contenttypes.fields import GenericForeignKey

from django_szuprefix_saas.saas.models import Party
from django.contrib.auth.models import User
from django_szuprefix.utils import modelutils


class DailyLog(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "日志"
        unique_together = ('the_date', 'user')

    party = models.ForeignKey(Party, verbose_name=Party._meta.verbose_name, related_name="dailylog_dailylogs",
                              on_delete=models.PROTECT)
    the_date = models.DateField('日期', db_index=True)
    user = models.ForeignKey(User, verbose_name=User._meta.verbose_name, related_name="dailylog_dailylogs",
                             on_delete=models.PROTECT)
    context = modelutils.JSONField("详情", blank=True, default={})
    create_time = models.DateTimeField("创建时间", auto_now_add=True, db_index=True)
    update_time = models.DateTimeField("创建时间", auto_now=True)

    def __unicode__(self):
        return '%s dailylog @ %s' % (self.user, self.the_date.isoformat())

class Stat(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "统计"
        unique_together = ('the_date', 'owner_type', 'owner_id', 'metics')

    party = models.ForeignKey(Party, verbose_name=Party._meta.verbose_name, related_name="dailylog_stats",
                              on_delete=models.PROTECT)
    the_date = models.DateField('日期', db_index=True)
    owner_type = models.ForeignKey('contenttypes.ContentType', verbose_name='归类', null=True, blank=True,
                                   on_delete=models.PROTECT)
    owner_id = models.PositiveIntegerField(verbose_name='属主编号', null=True, blank=True)
    owner = GenericForeignKey('owner_type', 'owner_id')
    metics = models.CharField('指标', max_length=128)
    value = models.PositiveIntegerField('数值', default=0)
    user_count = models.PositiveIntegerField('用户数', default=0)
    update_time = models.DateTimeField("创建时间", auto_now=True)

class Record(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "记录"
        unique_together = ('the_date', 'owner_type', 'owner_id', 'metics', 'user')

    party = models.ForeignKey(Party, verbose_name=Party._meta.verbose_name, related_name="dailylog_records",
                              on_delete=models.PROTECT)
    the_date = models.DateField('日期', db_index=True)
    owner_type = models.ForeignKey('contenttypes.ContentType', verbose_name='归类', null=True, blank=True,
                                   on_delete=models.PROTECT)
    owner_id = models.PositiveIntegerField(verbose_name='属主编号', null=True, blank=True)
    owner = GenericForeignKey('owner_type', 'owner_id')
    owner_name = models.CharField('属主名称', max_length=256, blank=True, default='')
    owner_group = models.CharField('属主分组', max_length=256, blank=True, default='')
    metics = models.CharField('指标', max_length=128)
    user = models.ForeignKey(User, verbose_name=User._meta.verbose_name, related_name="dailylog_records",
                             on_delete=models.PROTECT)
    user_name = models.CharField('用户姓名', max_length=256, blank=True, default='')
    user_group = models.CharField('用户分组', max_length=256, blank=True, default='')
    value = models.PositiveIntegerField('数值', default=0)


    def save(self, **kwargs):
        self.user_name = self.user.get_full_name()
        self.user_group = unicode(self.user.as_school_student.classes.first()) if hasattr(self.user, 'as_school_student') else ''
        self.owner_name = unicode(self.owner)
        self.owner_group = unicode(self.owner.owner) if hasattr(self.owner, 'owner') else ''
        return super(Record, self).save(**kwargs)



class Performance(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "表现"
        # unique_together = ('party', 'user', 'paper')
        ordering = ('-update_time',)

    party = models.ForeignKey(Party, verbose_name=Party._meta.verbose_name, related_name="dailylog_performances",
                              on_delete=models.PROTECT)
    owner_type = models.ForeignKey('contenttypes.ContentType', verbose_name='归类', null=True, blank=True,
                                   on_delete=models.PROTECT)
    owner_id = models.PositiveIntegerField(verbose_name='属主编号', null=True, blank=True)
    owner = GenericForeignKey('owner_type', 'owner_id')
    owner_name = models.CharField('属主名称', max_length=256, blank=True, default='')
    owner_group = models.CharField('属主分组', max_length=256, blank=True, default='')
    user = models.ForeignKey(User, verbose_name=User._meta.verbose_name, related_name="dailylog_performances",
                             on_delete=models.PROTECT)
    user_name = models.CharField('用户姓名', max_length=256, blank=True, default='')
    user_group = models.CharField('用户分组', max_length=256, blank=True, default='')
    detail = modelutils.JSONField('详情', default={}, blank=True)
    target = models.PositiveIntegerField("目标", default=0, blank=True)
    accomplish = models.PositiveIntegerField("完成", default=0, blank=True)
    accumulate = models.PositiveIntegerField("累计完成", default=0, blank=True)
    percent = models.PositiveSmallIntegerField('完成百分比', default=0)
    times = models.PositiveSmallIntegerField('次数', default=0)
    score = models.PositiveSmallIntegerField("得分", default=0, blank=True, null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True, db_index=True)

    def __unicode__(self):
        return "%s by %s" % (self.owner_name, self.user_name)

    def save(self, **kwargs):
        self.user_name = self.user.get_full_name()
        self.user_group = unicode(self.user.as_school_student.classes.first()) if hasattr(self.user, 'as_school_student') else ''
        self.owner_name = unicode(self.owner)
        self.owner_group = unicode(self.owner.owner) if hasattr(self.owner, 'owner') else ''
        d = self.detail
        self.target = d.get('target', 0)
        ps = d.get('parts', [])
        self.accomplish = len(set(ps))
        self.accumulate = len(ps)
        self.percent = int(self.accomplish*100/self.target) if self.target else 0
        self.score = d.get('score')
        self.times = d.get('times', 0)
        return super(Performance, self).save(**kwargs)
