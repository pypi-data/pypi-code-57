# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-02-25 12:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0005_auto_20200222_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='lecturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='media.Lecturer', verbose_name='\u8bb2\u5e08'),
        ),
    ]
