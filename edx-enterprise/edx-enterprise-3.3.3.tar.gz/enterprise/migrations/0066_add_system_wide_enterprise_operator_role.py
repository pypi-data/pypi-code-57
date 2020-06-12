# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-27 13:59
from __future__ import unicode_literals

from django.db import migrations

from enterprise.constants import ENTERPRISE_OPERATOR_ROLE


def create_roles(apps, schema_editor):
    """Create the enterprise roles if they do not already exist."""
    SystemWideEnterpriseRole = apps.get_model('enterprise', 'SystemWideEnterpriseRole')
    SystemWideEnterpriseRole.objects.update_or_create(name=ENTERPRISE_OPERATOR_ROLE)


def delete_roles(apps, schema_editor):
    """Delete the enterprise roles."""
    SystemWideEnterpriseRole = apps.get_model('enterprise', 'SystemWideEnterpriseRole')
    SystemWideEnterpriseRole.objects.filter(
        name__in=[ENTERPRISE_OPERATOR_ROLE]
    ).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0065_add_enterprise_feature_roles'),
    ]

    operations = [
        migrations.RunPython(create_roles, delete_roles)
    ]
