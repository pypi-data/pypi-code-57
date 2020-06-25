
from datetime import date
from django.db import models
from django.utils import timezone


class TemporalQuerySet(models.QuerySet):
    """
    Temporal manager for models with `from_date`/`to_date` fields.
    """

    def set(self, **kwargs):
        today = timezone.now().date()

        self.filter(
            begin__lte=today,
            end__gt=today,
        ).update(to_date=today)

        self.filter(
            begin=today,
            end=today,
        ).delete()

        return self.create(
            begin=today,
            end=date(9999, 1, 1),
            **kwargs
        )

    def current(self):
        today = timezone.now().date()

        return self.filter(
            begin__lte=today,
            end__gt=today,
        ).first()