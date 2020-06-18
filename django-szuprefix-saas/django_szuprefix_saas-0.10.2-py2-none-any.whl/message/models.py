# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.functional import cached_property

from django_szuprefix_saas.saas.models import Party
from django.contrib.auth.models import User


class Task(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "任务"
        ordering = ('-create_time',)

    party = models.ForeignKey(Party, verbose_name=Party._meta.verbose_name, related_name="message_tasks",
                              on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name=User._meta.verbose_name, related_name="message_tasks",
                             on_delete=models.PROTECT)
    target_user_tags = models.CharField('目标人群标签', max_length=255, help_text="符合标签的人才能收到信息.<p>"
                                                                            "例子:<p>老师:张三,李四,赵五<p>学生:*<p>学生.年级:大一,大二<p>学生.入学届别:2019届<p>学生.班级:2018级数字媒体201801班,2018级数字媒体201804班")
    target_user_count = models.PositiveIntegerField('目标参与人数', default=0, blank=True)
    category = models.CharField("消息类型", max_length=32, blank=True, default='系统消息')
    title = models.CharField("标题", max_length=256, blank=True)
    content = models.TextField("内容", blank=True, null=True)
    link = models.CharField("连接", max_length=256, blank=True, null=True, default='')
    is_force = models.BooleanField("必填", default=False, blank=True)
    unique_id = models.CharField("排重", max_length=32, null=True, blank=True, db_index=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    send_time = models.DateTimeField("发送时间", null=True, blank=True, help_text="预定发送时间, 默认马上发送.")
    is_sent = models.BooleanField("已发送", default=True, blank=True)
    is_active = models.BooleanField("有效", default=True)

    def __unicode__(self):
        return self.title

    @cached_property
    def target_user_ids(self):
        from django_szuprefix.auth.helper import find_user_ids_by_tag
        tags = self.target_user_tags
        if tags:
            return set(find_user_ids_by_tag(tags))
        return set()

    @cached_property
    def read_user_count(self):
        return self.messages.filter(is_read=True).count()

    def revoke(self):
        from .helper import revoke_messages
        revoke_messages(self.messages.all())

    def send(self):
        from .helper import revoke_messages
        from datetime import datetime
        revoke_messages(self.messages.filter(is_active=True).exclude(id__in=self.target_user_ids))
        for uid in self.target_user_ids:
            Message.objects.update_or_create(
                receiver=User.objects.get(id=uid),
                task=self,
                sender=self.user,
                defaults=dict(
                    is_active=self.is_active,
                    is_force=self.is_force,
                    is_read=False,
                    read_time=None,
                    create_time=datetime.now()
                )
            )
        self.is_sent = True
        self.send_time = datetime.now()
        self.save()

    def save(self, **kwargs):
        self.target_user_count = len(self.target_user_ids)
        if not self.is_active:
            self.revoke()
        return super(Task, self).save(**kwargs)


class Message(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "消息"
        ordering = ('-create_time',)

    party = models.ForeignKey(Party, verbose_name=Party._meta.verbose_name, related_name="messages",
                              on_delete=models.PROTECT)
    receiver = models.ForeignKey(User, verbose_name='接收者', related_name="messages_received",
                                 on_delete=models.PROTECT)
    sender = models.ForeignKey(User, verbose_name='发送者', related_name="messages_sent",
                               on_delete=models.PROTECT)
    task = models.ForeignKey(Task, verbose_name=Task._meta.verbose_name, related_name="messages", null=True, blank=True,
                             on_delete=models.PROTECT)
    title = models.CharField("标题", max_length=256, blank=True)
    unique_id = models.CharField("排重", max_length=32, null=True, blank=True, db_index=True)
    is_force = models.BooleanField("必填", default=False, blank=True)
    is_active = models.BooleanField("有效", default=True)
    is_read = models.BooleanField("已读", default=False, blank=True, db_index=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    read_time = models.DateTimeField("阅读时间", null=True, blank=True)

    def save(self, **kwargs):
        if self.task:
            self.party = self.task.party
            self.title = self.task.title
            self.is_force = self.is_force if self.is_force is not None else self.task.is_force
            self.is_active = self.is_active if self.is_active is not None else self.task.is_active
        return super(Message, self).save(**kwargs)

    def __unicode__(self):
        return "%s: %s " % (self.receiver.get_full_name(), self.title)
