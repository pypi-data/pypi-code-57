# Generated by Django 2.2.9 on 2020-01-22 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drfpasswordless', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callbacktoken',
            name='to_alias',
            field=models.CharField(blank=True, max_length=254),
        ),
    ]
