# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-02-24 19:41
from __future__ import unicode_literals

import collections

import jsonfield.encoder
import jsonfield.fields

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0087_auto_20200206_1151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enterprisecustomer',
            name='learner_portal_hostname',
        ),
        migrations.RemoveField(
            model_name='historicalenterprisecustomer',
            name='learner_portal_hostname',
        ),
        migrations.AlterField(
            model_name='enterprisecatalogquery',
            name='content_filter',
            field=jsonfield.fields.JSONField(blank=True, default={}, dump_kwargs={'cls': jsonfield.encoder.JSONEncoder, 'separators': (',', ':')}, help_text="Query parameters which will be used to filter the discovery service's search/all endpoint results, specified as a JSON object. An empty JSON object means that all available content items will be included in the catalog.", load_kwargs={'object_pairs_hook': collections.OrderedDict}, null=True),
        ),
        migrations.AlterField(
            model_name='enterprisecustomercatalog',
            name='content_filter',
            field=jsonfield.fields.JSONField(blank=True, default={}, dump_kwargs={'cls': jsonfield.encoder.JSONEncoder, 'separators': (',', ':')}, help_text="Query parameters which will be used to filter the discovery service's search/all endpoint results, specified as a Json object. An empty Json object means that all available content items will be included in the catalog.", load_kwargs={'object_pairs_hook': collections.OrderedDict}, null=True),
        ),
        migrations.AlterField(
            model_name='historicalenterprisecustomercatalog',
            name='content_filter',
            field=jsonfield.fields.JSONField(blank=True, default={}, dump_kwargs={'cls': jsonfield.encoder.JSONEncoder, 'separators': (',', ':')}, help_text="Query parameters which will be used to filter the discovery service's search/all endpoint results, specified as a Json object. An empty Json object means that all available content items will be included in the catalog.", load_kwargs={'object_pairs_hook': collections.OrderedDict}, null=True),
        ),
    ]
