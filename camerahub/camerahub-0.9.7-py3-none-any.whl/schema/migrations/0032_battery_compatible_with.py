# Generated by Django 2.2.9 on 2020-03-17 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0031_auto_20200317_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='battery',
            name='compatible_with',
            field=models.ManyToManyField(blank=True, to='schema.Battery'),
        ),
    ]
