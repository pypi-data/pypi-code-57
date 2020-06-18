import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from helpers.validators import locale_regex

class Base(models.Model):
    INVISIBLE = 0
    VISIBLE = 1
    INACTIVE = 2
    DELETED = 3

    STATUS_CHOICES = [
        (INVISIBLE, 'Invisible'),
        (VISIBLE, 'Visible'),
        (INACTIVE, 'Inactive'),
        (DELETED, 'Deleted'),
    ]

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    hero = models.BooleanField(blank=True, null=True)

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=VISIBLE,
        verbose_name='Status',
        validators=[MinValueValidator(0), MaxValueValidator(3)],
    )

    class Meta:
        abstract = True


class Locale(Base):

    locale = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        validators=[locale_regex,]
    )

    class Meta:
        abstract = True
