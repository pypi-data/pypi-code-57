from django.db import models


class Download(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=1000, null=True)
    client_ip = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'downloads'


class UserVersion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    version = models.CharField(max_length=20, null=True)
    client_ip = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'user_versions'
