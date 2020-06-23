from django.db import models
from django.utils.safestring import mark_safe
from edc_lab.choices import RESULT_QUANTIFIER
from edc_lab.constants import EQ

from ..choices import GLUCOSE_UNITS


class FastingGlucoseModelMixin(models.Model):
    # IFG
    fasting_glucose = models.DecimalField(
        verbose_name=mark_safe("Fasting glucose <u>level</u>"),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    fasting_glucose_quantifier = models.CharField(
        max_length=10, choices=RESULT_QUANTIFIER, default=EQ,
    )

    fasting_glucose_units = models.CharField(
        verbose_name="Units (fasting glucose)",
        max_length=15,
        choices=GLUCOSE_UNITS,
        blank=True,
        null=True,
    )

    fasting_glucose_datetime = models.DateTimeField(
        verbose_name=mark_safe("<u>Time</u> fasting glucose <u>level</u> measured"),
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
