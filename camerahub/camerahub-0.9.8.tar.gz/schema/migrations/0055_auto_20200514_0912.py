# Generated by Django 2.2.12 on 2020-05-14 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0054_auto_20200504_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='recipient',
            field=models.ForeignKey(blank=True, help_text='Person who placed this order', null=True, on_delete=django.db.models.deletion.CASCADE, to='schema.Person'),
        ),
    ]
