# Generated by Django 3.0.6 on 2020-05-12 18:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comment', '0003_auto_20200419_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.PositiveIntegerField(default=0)),
                ('dislikes', models.PositiveIntegerField(default=0)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='comment.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='ReactionInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction_type', models.SmallIntegerField(choices=[(1, 'LIKE'), (2, 'DISLIKE')])),
                ('date_reacted', models.DateTimeField(auto_now=True)),
                ('reaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='comment.Reaction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'reaction')},
            },
        ),
    ]
