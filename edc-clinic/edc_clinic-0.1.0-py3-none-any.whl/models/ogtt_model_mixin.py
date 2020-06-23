from django.db import models
from django.utils.safestring import mark_safe
from edc_lab.choices import RESULT_QUANTIFIER
from edc_lab.constants import EQ

from ..choices import GLUCOSE_UNITS


class OgttModelMixin(models.Model):
    ogtt_base_datetime = models.DateTimeField(
        verbose_name=mark_safe("<u>Time</u> oral glucose solution was given"),
        null=True,
        blank=True,
        help_text="(glucose solution given)",
    )

    ogtt_two_hr = models.DecimalField(
        verbose_name=mark_safe(
            "Blood glucose <u>level</u> 2-hours " "after oral glucose solution given"
        ),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    ogtt_two_hr_quantifier = models.CharField(
        max_length=10, choices=RESULT_QUANTIFIER, default=EQ,
    )

    ogtt_two_hr_units = models.CharField(
        verbose_name="Units (Blood glucose 2hrs after...)",
        max_length=15,
        choices=GLUCOSE_UNITS,
        blank=True,
        null=True,
    )

    ogtt_two_hr_datetime = models.DateTimeField(
        verbose_name=mark_safe(
            "<u>Time</u> blood glucose measured 2-hours "
            "after oral glucose solution given"
        ),
        blank=True,
        null=True,
        help_text="(2 hours after glucose solution given)",
    )

    class Meta:
        abstract = True
