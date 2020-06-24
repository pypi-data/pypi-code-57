"""Migration to add the permissions table.
"""

# pylint:disable=invalid-name

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration for adding the initial table for providing permissions.
    """
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GCPIotDevicePermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
                                        verbose_name='ID')),
            ],
            options={
                'managed': False,
            },
        ),
    ]
