from django.db import models
from jsonfield import JSONField

from .dataset import Dataset


class ImageFolder(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    dataset = models.ForeignKey(Dataset, models.CASCADE, related_name='image_folders')
    parent = models.ForeignKey('ImageFolder', models.CASCADE, related_name='children', null=True)

    class Meta:
        db_table = 'folders'


class ImageFolderStatistics(models.Model):
    image_folder = models.ForeignKey(ImageFolder, models.CASCADE, related_name='statistics')
    statistics = JSONField(null=True)

    class Meta:
        db_table = 'folder_statistics'
