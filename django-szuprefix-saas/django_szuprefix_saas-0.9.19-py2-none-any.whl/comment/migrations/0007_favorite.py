# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-05-20 03:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_szuprefix.utils.modelutils


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('saas', '0008_auto_20200515_1420'),
        ('comment', '0006_auto_20200331_0355'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('object_name', models.CharField(blank=True, db_index=True, max_length=256, null=True, verbose_name='\u540d\u79f0')),
                ('notes', django_szuprefix.utils.modelutils.JSONField(blank=True, default={}, verbose_name='\u7b14\u8bb0')),
                ('create_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u6709\u6548')),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType')),
                ('party', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='comment_favorites', to='saas.Party', verbose_name='\u56e2\u4f53')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_favorites', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-create_time',),
                'verbose_name': '\u6536\u85cf',
                'verbose_name_plural': '\u6536\u85cf',
            },
        ),
    ]
