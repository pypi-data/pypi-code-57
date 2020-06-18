import os
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify


def post_image_file_path(instance, filename):
    """Generate file path for new post image """
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("uploads/post/", filename)


def author_avatar_file_path(instance, filename):
    """Generate file path for new author avatar """
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("uploads/author/", filename)


class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True)
    avatar = models.ImageField(null=True, upload_to=author_avatar_file_path, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        new_object = False if self.pk else True
        now = timezone.now()
        if new_object:
            self.created_at = now
            self.slug = self._get_unique_slug()
        self.modified_at = now
        if not self.first_name:
            raise ValidationError("First name is required")
        if not self.last_name:
            raise ValidationError("Last name is required")
        if not self.user:
            raise ValidationError("User is required")
        try:
            int(self.name.replace(" ", ""))
            raise ValidationError("Only enter valid names")
        except ValueError:
            pass

        super().save()

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Author.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(slug, num)
            num += 1
        return unique_slug

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.name


class SocialAccount(models.Model):
    author = models.ManyToManyField("blog.Author", related_name="social_accounts")
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    url = models.CharField(max_length=510)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        new_object = False if self.pk else True
        now = timezone.now()
        if new_object:
            self.created_at = now
            self.slug = self._get_unique_slug()
        self.modified_at = now
        super().save()

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while SocialAccount.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(slug, num)
            num += 1
        return unique_slug


class Post(models.Model):
    author = models.ForeignKey(
        "blog.Author", null=True, on_delete=models.SET_NULL, blank=True
    )
    cover_image = models.ImageField(
        null=True, upload_to=post_image_file_path, blank=True
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.TextField()
    summary = models.TextField(max_length=500, blank=True)
    category = models.ForeignKey(
        "blog.Category", null=True, on_delete=models.SET_NULL, blank=True
    )
    tags = models.ManyToManyField("blog.Tag", related_name="tags", blank=True)
    DRAFT = "Draft"
    PUBLISHED = "Published"
    POST_STATUS_CHOICES = (
        (DRAFT, "Draft"),
        (PUBLISHED, "Published"),
    )
    status = models.CharField(max_length=25, choices=POST_STATUS_CHOICES, default=DRAFT)
    HTML = "HTML"
    MARKDOWN = "MARKDOWN"
    FILE_TYPE_CHOICES = ((HTML, "HTML"), (MARKDOWN, "MARKDOWN"))
    file_type = models.CharField(max_length=25, choices=FILE_TYPE_CHOICES, default=HTML)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        new_object = False if self.pk else True
        now = timezone.now()
        if new_object:
            self.created_at = now
            self.slug = self.slug or self._get_unique_slug()
        self.modified_at = now
        if not self.title:
            raise ValidationError("Title is required")
        if not self.content:
            raise ValidationError("Content is required")
        super().save()

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(slug, num)
            num += 1
        return unique_slug

    def mark_as_published(self):
        self.status = self.PUBLISHED
        self.save()

    def mark_as_draft(self):
        self.status = self.DRAFT
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        new_object = False if self.pk else True
        now = timezone.now()
        if new_object:
            self.created_at = now
            self.slug = self._get_unique_slug()
        self.modified_at = now
        super().save()

    class Meta:
        verbose_name_plural = "categories"

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(slug, num)
            num += 1
        return unique_slug


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        new_object = False if self.pk else True
        now = timezone.now()
        if new_object:
            self.created_at = now
            self.slug = self._get_unique_slug()
        self.modified_at = now
        super().save()

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Tag.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(slug, num)
            num += 1
        return unique_slug
