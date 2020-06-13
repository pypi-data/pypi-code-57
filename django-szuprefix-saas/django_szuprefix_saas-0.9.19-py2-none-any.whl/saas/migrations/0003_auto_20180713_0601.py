# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-12 22:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('saas', '0002_auto_20180415_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='as_saas_worker', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
