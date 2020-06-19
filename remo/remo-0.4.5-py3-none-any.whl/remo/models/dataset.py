import hashlib
import io
import logging
import os
import math
import requests

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Max
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from jsonfield import JSONField

from remo_app.remo.utils.utils import is_windows
from .license import License
from ..services.vips_image import VipsImage

logger = logging.getLogger('remo_app')


def get_original_file_path(instance, filename):
    return 'dataset_originals/{}'.format(filename)


def get_image_file_path(instance, filename):
    return 'dataset_images/{}'.format(filename)


def get_thumbnail_file_path(instance, filename):
    return 'dataset_thumbnails/{}'.format(filename)


def get_view_file_path(instance, filename):
    return 'dataset_views/{}'.format(filename)


def get_preview_file_path(instance, filename):
    return 'dataset_previews/{}'.format(filename)


def get_image_dimensions(image):
    if not image:
        return None, None

    img = None
    if settings.STORAGE == 'local':
        path = str(image.file)
        img = VipsImage.from_file(path)
    elif settings.STORAGE == 'aws':
        url = image.url
        response = requests.get(url)
        if response.status_code == 200:
            img = VipsImage.from_buffer(response.content)
    if img:
        return img.width, img.height

    return None, None


class Image(models.Model):
    """
    One image entity. Corresponds to one image file. Can belong to
    several datasets.
    Each image file must be unique by contents.
    For this purpose the name of file is actually has a hash from
    contents. `thumbnail` have name equal
    to `image`, but stored to different path.
    """
    original = models.FileField(upload_to=get_original_file_path, null=True, max_length=1000)
    image = models.FileField(upload_to=get_image_file_path, null=True, max_length=1000)
    local_image = models.CharField(max_length=1000, null=True)
    thumbnail = models.FileField(upload_to=get_thumbnail_file_path, null=True, max_length=1000)
    view = models.FileField(upload_to=get_view_file_path, null=True, max_length=1000)
    preview = models.FileField(upload_to=get_preview_file_path, null=True, max_length=1000)
    size = models.PositiveIntegerField(default=0)  # File size in bytes
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'images'

    @staticmethod
    def generate_filename(contents):
        """
        Generate filename based on image contents
        :param contents: file-like object with image data
        :return: filename string without extension
        """
        pos = contents.tell()
        contents.seek(0)
        filename = hashlib.md5(contents.read()).hexdigest()
        contents.seek(pos)

        return filename

    def __str__(self):
        return 'Image #{}'.format(self.id)

    def thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url

    def preview_url(self):
        if self.preview:
            return self.preview.url

    def local_image_url(self):
        if self.local_image:
            if is_windows():
                return "{}/{}".format(settings.LOCAL_FILES, self.local_image)
            return settings.LOCAL_FILES + self.local_image

    def original_url(self):
        if self.original:
            if self.local_image:
                return self.local_image_url()
            return self.original.url

    def image_url(self):
        if self.image:
            return self.image.url

        return self.local_image_url()

    def view_url(self):
        if self.view:
            return self.view.url

        return self.image_url()

    def dimensions(self):
        return [self.width, self.height]

    def thumbnail_dimensions(self):
        return get_image_dimensions(self.thumbnail)

    def preview_dimensions(self):
        return get_image_dimensions(self.preview)

    def image_dimensions(self):
        if self.image:
            return get_image_dimensions(self.image)

        return self.dimensions()

    def view_dimensions(self):
        if self.view:
            return get_image_dimensions(self.view)

        return self.image_dimensions()

    def delete(self, using=None, keep_parents=False):
        if self.original and not self.local_image:
            self.original.storage.delete(self.original.name)
        if self.image:
            self.image.storage.delete(self.image.name)
        if self.thumbnail:
            self.thumbnail.storage.delete(self.thumbnail.name)
        if self.preview:
            self.preview.storage.delete(self.preview.name)
        if self.view:
            self.view.storage.delete(self.view.name)
        super().delete(using=using, keep_parents=keep_parents)


class Dataset(models.Model):
    # XXX: take a look on clone_relations_from hierarchy on relations change
    name = models.CharField(max_length=1000)
    is_archived = models.BooleanField(default=False, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #
    # add / delete image to dataset
    # reorganize / move images inside dataset (not implemented yet)
    # add / edit / delete annotation
    # rename dataset
    #
    # on this actions need to update field `updated_at`
    #
    updated_at = models.DateTimeField(auto_now=True)
    license = models.ForeignKey(License, models.DO_NOTHING, blank=True, null=True)
    is_public = models.BooleanField(default=False)
    users_shared = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='users_shared'
    )
    # TODO: add teams_shared when teams will be implemented
    images = models.ManyToManyField(Image, through='DatasetImage', related_name='datasets')
    size_in_bytes = models.BigIntegerField(default=0)
    quantity = models.BigIntegerField(default=0)

    class Meta:
        ordering = ['id']
        db_table = 'datasets'

    def __str__(self):
        return self.name

    def update(self):
        self.updated_at = timezone.now()
        self.save()

    def clone_relations_from(self, instance):
        """
        Clone relations from given Dataset through to Image
        :param instance: object to be cloned (already saved)
        :return:
        """
        # Mapping old AnnotationSet ids to new ones
        annotation_sets = {}

        for annotation_set in instance.annotation_sets.all():
            old_set = annotation_set.__class__.objects.get(pk=annotation_set.pk)
            new_set = annotation_set
            new_set.pk = None
            new_set.dataset = self

            # Clear release date for new private dataset cause this
            # field has sense only for public ones, DEV-246
            new_set.released_at = None

            new_set.save()
            new_set.clone_relations_from(old_set)
            new_set.save()

            annotation_sets[old_set.pk] = new_set.pk

        for dataset_img in instance.dataset_images.all():
            old_img = dataset_img.__class__.objects.get(pk=dataset_img.pk)
            new_img = dataset_img
            new_img.pk = None
            new_img.dataset = self
            new_img.save()
            new_img.clone_relations_from(old_img, annotation_sets)
            new_img.save()

        # self.users_shared.set(instance.users_shared.all())

        return instance

    def delete(self, using=None, keep_parents=False):
        ids = [img.id for img in self.images.all()]
        super().delete(using=using, keep_parents=keep_parents)
        for id in ids:
            img = Image.objects.get(id=id)
            if not DatasetImage.objects.filter(image_object=img).exists():
                img.delete()


class DatasetStatistics(models.Model):
    dataset = models.ForeignKey(Dataset, models.CASCADE, related_name='dataset_statistics')
    statistics = JSONField(null=True)

    class Meta:
        db_table = 'dataset_statistics'


class DatasetImage(models.Model):
    # XXX: take a look on clone_relations_from hierarchy on relations change
    dataset = models.ForeignKey(Dataset, models.CASCADE, related_name='dataset_images')
    image_object = models.ForeignKey(Image, models.CASCADE)
    # deprecated
    # TODO: drop this field
    number_in_dataset = models.IntegerField(default=0)
    original_name = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    folder = models.ForeignKey(
        'ImageFolder',
        models.CASCADE,
        related_name='contents',
        null=True
    )

    class Meta:
        ordering = ('number_in_dataset',)
        db_table = 'dataset_images'
        unique_together = (
            # Dataset may have only unique image names
            # ('dataset', 'original_name'),
        )

    def thumbnail_url(self):
        return self.image_object.thumbnail_url()

    def preview_url(self):
        return self.image_object.preview_url()

    def local_image_url(self):
        return self.image_object.local_image_url()

    def original_url(self):
        return self.image_object.original_url()

    def image_url(self):
        return self.image_object.image_url()

    def view_url(self):
        return self.image_object.view_url()

    def dimensions(self):
        return self.image_object.dimensions()

    def thumbnail_dimensions(self):
        return self.image_object.thumbnail_dimensions()

    def preview_dimensions(self):
        return self.image_object.preview_dimensions()

    def image_dimensions(self):
        return self.image_object.image_dimensions()

    def view_dimensions(self):
        return self.image_object.view_dimensions()

    def save(self, *args, **kwargs):
        if not self.number_in_dataset:
            dataset_images = DatasetImage.objects.filter(dataset=self.dataset)
            is_first_image = not dataset_images.exists()
            self.number_in_dataset = 1 if is_first_image else dataset_images.aggregate(
                Max('number_in_dataset'))['number_in_dataset__max'] + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return 'DatasetImage: #{}'.format(self.id)

    def is_new(self):
        return self.id is None

    @staticmethod
    def is_duplicate(dataset, path):
        name = path
        if os.path.exists(path):
            name = os.path.basename(path)

        img = DatasetImage.objects.filter(dataset=dataset, original_name=name).first()
        return img is not None

    def link_local_file(self, path):
        filename = self._gen_filename(path)
        if self._is_new_image(filename, local_path=path):
            img = self._open_image_from_file(path)
            self._save_image_size_and_dimensions_from_file(path, img)

            img = self._link_local_file(filename, path, img)
            img = self._save_preview_image_from_file(filename, path, img)
            self._save_thumbnail_image(filename, img)

        return self

    def upload_image_from_file(self, path):
        filename = self._gen_filename(path)
        if self._is_new_image(filename, original_name=os.path.basename(path)):
            img = self._open_image_from_file(path)
            self._save_image_size_and_dimensions_from_file(path, img)

            img = self._save_original_image_from_file(filename, path, img)
            img = self._save_view_image_from_file(filename, path, img)
            img = self._save_preview_image_from_file(filename, path, img)
            self._save_thumbnail_image(filename, img)

        return self

    def upload_image_from_buffer(self, buffer, original_name):
        filename = Image.generate_filename(buffer)
        if self._is_new_image(filename, original_name):
            img = self._open_image_from_buffer(buffer)
            self._save_image_size_and_dimensions_from_buffer(buffer, img)

            img = self._save_original_image_from_buffer(filename, buffer, img)
            img = self._save_view_image_from_buffer(filename, buffer, img)
            img = self._save_preview_image_from_buffer(filename, buffer, img)
            self._save_thumbnail_image(filename, img)

        return self

    def _gen_filename(self, path):
        """
        Generate filename based on file contents
        """
        with open(path, 'rb') as f:
            filename = hashlib.md5(f.read()).hexdigest()

        return filename

    def _is_new_image(self, filename, original_name=None, local_path=None):
        """
        Returns boolean status is_new
        """
        is_new = False
        pathname = get_thumbnail_file_path(None, filename)
        image_object = Image.objects.filter(thumbnail=pathname).first()
        if image_object:
            dataset_image = DatasetImage.objects.filter(dataset=self.dataset, image_object=image_object).first()
            if dataset_image:
                self.id = dataset_image.id
                self.dataset = dataset_image.dataset
                self.image_object = dataset_image.image_object
                self.number_in_dataset = dataset_image.number_in_dataset
                self.original_name = dataset_image.original_name
                self.folder = dataset_image.folder
                return is_new

        if not image_object:
            image_object = Image.objects.create()
            is_new = True

        self.image_object = image_object
        if local_path:
            self.image_object.local_image = local_path
            original_name = os.path.basename(local_path)

        self.original_name = original_name
        self.image_object.save()
        return is_new

    def _save_image_size_and_dimensions_from_file(self, path, img):
        file_size = os.path.getsize(path)
        self._save_image_size_and_dimensions(file_size, img.width, img.height)

    def _save_image_size_and_dimensions_from_buffer(self, buffer, img):
        buffer.seek(0, io.SEEK_END)
        file_size = buffer.tell()
        buffer.seek(0)
        self._save_image_size_and_dimensions(file_size, img.width, img.height)

    def _save_image_size_and_dimensions(self, file_size, width, height):
        self.image_object.size = file_size
        self.image_object.width, self.image_object.height = width, height
        self.image_object.save()

    def _link_local_file(self, filename, path, img):
        if self._is_image_exists_and_update_pathname(filename, 'image'):
            return img

        self.image_object.original.name = path
        self.image_object.save()

        if self._is_high_resolution_image():
            return self._save_lower_resolution_image(filename, img)
        return img

    def _save_preview_image_from_file(self, filename, path, img):
        if self._is_image_exists_and_update_pathname(filename, 'preview'):
            return img

        return self._save_optimized_image_from_file(filename, path, img, 'preview')

    def _save_original_image_from_file(self, filename, path, img):
        if self._is_image_exists_and_update_pathname(filename, 'image'):
            return img

        if self._is_high_resolution_image():
            self._save_image_from_file(filename, path, 'original')
            return self._save_lower_resolution_image(filename, img)

        self._save_image_from_file(filename, path, 'image')
        return img

    def _save_view_image_from_file(self, filename, path, img):
        if self._is_image_exists_and_update_pathname(filename, 'view'):
            return img

        return self._save_optimized_image_from_file(filename, path, img, 'view')

    def _save_original_image_from_buffer(self, filename, buffer, img):
        if self._is_image_exists_and_update_pathname(filename, 'image'):
            return img

        if self._is_high_resolution_image():
            self._save_image_from_buffer(filename, buffer, 'original')
            return self._save_lower_resolution_image(filename, img)

        self._save_image_from_buffer(filename, buffer, 'image')
        return img

    def _save_view_image_from_buffer(self, filename, buffer, img):
        if self._is_image_exists_and_update_pathname(filename, 'view'):
            return img

        return self._save_optimized_image_from_buffer(filename, buffer, img, 'view')

    def _save_preview_image_from_buffer(self, filename, buffer, img):
        if self._is_image_exists_and_update_pathname(filename, 'preview'):
            return img

        return self._save_optimized_image_from_buffer(filename, buffer, img, 'preview')

    def _is_image_exists_and_update_pathname(self, filename, property):
        """
        property: image, view, preview, thumbnail
        """
        get_file_path = {
            'image': get_image_file_path,
            'view': get_view_file_path,
            'preview': get_preview_file_path,
            'thumbnail': get_thumbnail_file_path,
        }.get(property)

        img = getattr(self.image_object, property)
        storage_backend = img.storage
        pathname = get_file_path(None, filename)
        if storage_backend.exists(pathname):
            img.name = pathname
            self.image_object.save()
            return True

    def _is_image_exists(self, filename, path):
        storage = self.image_object.image.storage
        pathname = get_image_file_path(None, filename)
        if storage.exists(pathname):
            self.image_object.image.name = pathname
            self.image_object.original.name = path
            self.image_object.save()
            return True
        return False

    def _open_image_from_file(self, path):
        return VipsImage.from_file(path)

    def _open_image_from_buffer(self, buffer):
        buffer.seek(0)
        return VipsImage.from_buffer(buffer.read())

    def _is_high_resolution_image(self):
        width, height = self.image_object.width, self.image_object.height
        file_size = self.image_object.size
        return (width * height > settings.HIGH_RESOLUTION_THRESHOLD
                or file_size > settings.HIGH_RESOLUTION_FILE_SIZE_THRESHOLD)

    def _save_lower_resolution_image_from_file(self, filename, path):
        img = self._open_image_from_file(path)
        return self._save_lower_resolution_image(filename, img)

    def _save_lower_resolution_image_from_buffer(self, filename, buffer):
        img = self._open_image_from_buffer(buffer)
        return self._save_lower_resolution_image(filename, img)

    def _save_lower_resolution_image(self, filename, img):
        optimized_size = DatasetImage._calculate_image_size((img.width, img.height), settings.HIGH_RESOLUTION)
        if optimized_size:
            img = img.resize(optimized_size[0] / img.width)
        img = img.copy_memory()
        self._save_result_image(filename, img, settings.HIGH_RESOLUTION_QUALITY, 'image')

        return img

    def _save_image_from_file(self, filename, path, property):
        img_obj = getattr(self.image_object, property)
        with open(path, 'rb') as img_file:
            img_obj.save(filename, img_file, save=True)

    def _save_image_from_buffer(self, filename, buffer, property):
        img_obj = getattr(self.image_object, property)
        img_obj.save(filename, buffer, save=True)

    def _save_optimized_image_from_file(self, filename, path, img, property):
        optimized_image = self._save_optimized_image(filename, img, property)
        if optimized_image is not None:
            return optimized_image

        self._save_image_from_file(filename, path, property)
        return img

    def _save_optimized_image_from_buffer(self, filename, buffer, img, property):
        optimized_image = self._save_optimized_image(filename, img, property)
        if optimized_image is not None:
            return optimized_image

        self._save_image_from_buffer(filename, buffer, property)
        return img

    def _save_optimized_image(self, filename, img, property):
        dimensions = {
            'view': settings.VIEW_SIZE,
            'preview': settings.PREVIEW_SIZE,

        }.get(property)

        quality = {
            'view': settings.VIEW_QUALITY,
            'preview': settings.PREVIEW_QUALITY,

        }.get(property)

        optimized_size = DatasetImage._calculate_image_size((img.width, img.height), dimensions)
        if optimized_size:
            img = img.resize(optimized_size[0] / img.width)
            img = img.copy_memory()
            self._save_result_image(filename, img, quality, property)
            return img

    def _save_result_image(self, filename, img, quality, property, extension='.jpg'):
        """
        property: view, preview, thumbnail
        """
        img_obj = getattr(self.image_object, property)
        data = img.write_to_buffer(extension, Q=quality)
        img_obj.save(filename, ContentFile(data), save=True)

    def _save_thumbnail_image(self, filename, img):
        if self._is_image_exists_and_update_pathname(filename, 'thumbnail'):
            return

        w, h = settings.THUMBNAIL_SIZE
        downscale = w / min(img.width, img.height)
        img = img.resize(downscale)

        width, height = img.width, img.height
        x = int((width - w) / 2) if width > w else 0
        y = int((height - h) / 2) if height > h else 0
        img = img.crop(x, y, w, h)

        self._save_result_image(filename, img, settings.THUMBNAIL_QUALITY, 'thumbnail')

    @staticmethod
    def _calculate_image_size(img_size, new_size, min_size=50):
        """
        Calculates appropriate size for smaller image
        :param img_size: (x, y)
        :param new_size: (x, y)
        :param min_size:
        :return: (x, y)
        """
        x, y = img_size
        if x < min_size or y < min_size:
            return

        actual_area = x * y
        expected_area = new_size[0] * new_size[1]
        if actual_area <= expected_area:
            return

        factor = math.sqrt(actual_area / expected_area)
        x /= factor
        y /= factor

        if x < min_size:
            factor = x / min_size
            x /= factor
            y /= factor

        if y < min_size:
            factor = y / min_size
            x /= factor
            y /= factor

        x = int(x + 0.5)
        y = int(y + 0.5)
        return x, y

    def clone_relations_from(self, instance, annotation_set_ids={}):
        """
        Clone relations from given DatasetImage
        Also clone Annotation(s)
        :param instance: object to be cloned (already saved)
        :param annotation_set_ids: Optional. Mapping AnnotationSets ids
        :return:
        """
        for annotation in instance.annotations.all():
            old_obj = annotation.__class__.objects.get(pk=annotation.pk)
            annotation.pk = None
            annotation.image = self
            annotation.annotation_set_id = annotation_set_ids.get(
                old_obj.annotation_set.pk,
                old_obj.annotation_set.pk
            )
            annotation.save()
            annotation.clone_relations_from(old_obj)
            annotation.save()

        for tag in instance.annotation_tags.all():
            tag.pk = None
            tag.image = self
            tag.annotation_set_id = annotation_set_ids.get(
                tag.annotation_set.pk,
                tag.annotation_set.pk
            )
            tag.save()

        return instance

    def delete(self, using=None, keep_parents=False):
        img_obj = self.image_object
        dataset = self.dataset

        super().delete(using=using, keep_parents=keep_parents)

        if img_obj and dataset:
            dataset.size_in_bytes -= img_obj.size
            dataset.quantity -= 1
            dataset.updated_at = timezone.now()
            dataset.save()

        if not DatasetImage.objects.filter(image_object=img_obj).exists():
            img_obj.delete()


@receiver(post_save, sender=DatasetImage)
def increase_dataset_size(sender, instance, created, **kwargs):
    if instance.image_object:
        dataset = instance.dataset
        if dataset:
            if created:
                dataset.size_in_bytes += instance.image_object.size
                dataset.quantity += 1
                dataset.updated_at = timezone.now()
            dataset.save()
