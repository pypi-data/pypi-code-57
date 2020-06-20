import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """ 
    Best practice for lookup field url instead pk or slug.
    for security
    """
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class ActivatorModel(models.Model):
    """
    ActivatorModel
    An abstract base class model that provides activate and deactivate fields.
    """

    INACTIVE_STATUS = 'i'
    ACTIVE_STATUS = 'a'

    STATUS_CHOICES = (
        (INACTIVE_STATUS, _('Inactive')),
        (ACTIVE_STATUS, _('Active')),
    )

    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=ACTIVE_STATUS)
    activate_date = models.DateTimeField(
        blank=True, null=True, help_text=_('keep empty for an immediate activation'))
    deactivate_date = models.DateTimeField(
        blank=True, null=True, help_text=_('keep empty for indefinite activation'))

    class Meta:
        abstract = True
