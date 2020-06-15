import mimetypes
import os
import uuid
import math

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .managers import FileManager


def generate_unique_file_name(instance, filename):
    """
    Method for generating a unique filename using uuid
    :param instance: File instance
    :param filename: Filename of the file instance
    :return: unique filename with file extension
    """
    return os.path.join(str(uuid.uuid4()), filename)


class AbstractFile(models.Model):
    """
    Default File Model
    """

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    name = models.CharField(
        max_length=255,
        blank=True,
        help_text="if no name is given the filename will be taken",
    )
    size = models.IntegerField()
    format = models.CharField(max_length=50, null=True, blank=True)
    creator = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="files",
        null=True,
        blank=True,
    )
    upload_date = models.DateField(default=timezone.now)
    file = models.FileField(upload_to=generate_unique_file_name)
    objects = FileManager()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.name:
            self.name = self.file.name
        self.size = self.file.size

        self.full_clean()  # call full_clean() to ensure that clean method gets called and all fields are valid
        super().save(force_insert, force_update, using, update_fields)

    def clean(self):
        from .settings import api_settings  # import locally to prevent import loop

        # get the files mime type from the file itself or if not given guess it from the filename
        mime_type = (
            self.file.file.content_type
            if hasattr(self.file.file, "content_type")
            else mimetypes.guess_type(self.file.name)[0]
        )

        # check if the files mime type is allowed
        if mime_type in api_settings.ALLOWED_FORMATS:
            self.format = mime_type
        else:
            raise ValidationError("mime_type_not_allowed")

        # size check
        if math.ceil(len(self.file.file)) >= api_settings.MAX_FILE_SIZE_KB * 1024:
            raise ValidationError("filesize_too_large")


class File(AbstractFile):
    pass
