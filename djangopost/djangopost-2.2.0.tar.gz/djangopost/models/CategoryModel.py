from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from djangopost.managers import CategoryModelManager


class CategoryModel(models.Model):

    STATUS_CHOICES = (
            ('draft', 'Draft'),
            ('publish', 'Publish'),
            ('withdraw', 'Withdraw'),
            ('private', 'Private')
    )

    serial        = models.IntegerField(blank=True, null=True)
    title         = models.CharField(max_length=35, unique=True, blank=False, null=False)
    slug          = models.SlugField(max_length=35, unique=True, blank=False, null=False)
    description   = models.TextField(blank=True, null=True)
    author        = models.ForeignKey(User, on_delete=models.CASCADE)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    verification  = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    # register model managers.
    objects = CategoryModelManager()

    # overright the save method.
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(CategoryModel, self).save(*args, **kwargs)

    # str method.
    def __str__(self):
        return self.title

    # create absolute urls.
    def get_absolute_url_for_detail_view(self):
        return reverse("djangopost:category_detail_view", kwargs={'category_slug': self.slug})

    def get_absolute_url_for_update_view(self):
        return reverse("djangopost:category_update_view", kwargs={'category_slug': self.slug})

    def get_absolute_url_for_delete_view(self):
        return reverse("djangopost:category_delete_view", kwargs={'category_slug': self.slug})

    # meta class.
    class Meta:
        ordering = ['-pk']
        verbose_name = "Djangopost category"
        verbose_name_plural = "Djangopost categories"