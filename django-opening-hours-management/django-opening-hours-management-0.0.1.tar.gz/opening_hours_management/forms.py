from datetime import datetime, time

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from intervaltree import Interval, IntervalTree

from .constants import MIDNIGHT_TIME
from .fields import FormTimeField
from .models import (
    ISO_WEEKDAY_CHOICES,
    GeneralHolidaysTimeRange,
    SpecificPeriodTimeRange,
    WeekDayTimeRange,
)
from .shortcuts import format_time_range, time_total_seconds


class TimeRangeModelForm(forms.ModelForm):
    opening_time = FormTimeField()
    closing_time = FormTimeField()


class TimeRangeInlineFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        super().clean()

        forms_to_delete = self.deleted_forms
        valid_forms = [
            form
            for form in self.forms
            if form.is_valid() and form not in forms_to_delete
        ]

        interval_tree = IntervalTree()

        has_concurrent_periods = False
        for form in valid_forms:
            opening_time = time_total_seconds(form.cleaned_data["opening_time"])

            closing_time = form.cleaned_data["closing_time"]

            if closing_time == MIDNIGHT_TIME:
                closing_time = time_total_seconds(time(23, 59)) + 1
            else:
                closing_time = time_total_seconds(closing_time)

            overlap_set = interval_tree.overlap(opening_time, closing_time)

            if len(overlap_set) > 0:
                overlap = list(overlap_set)[0]
                overlap_form_data = overlap.data.cleaned_data
                overlap_opening_time = overlap_form_data["opening_time"]
                overlap_closing_time = overlap_form_data["closing_time"]
                overlap_display = format_time_range(
                    overlap_opening_time, overlap_closing_time
                )

                form.add_error(
                    "opening_time",
                    _(
                        "This period is in conflict with the period {overlap_display}"
                    ).format(overlap_display=overlap_display),
                )
                has_concurrent_periods = True

            interval = Interval(opening_time, closing_time, form)
            interval_tree.add(interval)

        if has_concurrent_periods:
            raise ValidationError(
                _("The form cannot be validated because some periods are in conflict")
            )


class WeekDayTimeRangeModelForm(TimeRangeModelForm):
    class Meta:
        model = WeekDayTimeRange
        exclude = []


class WeekDayTimeRangeInlineFormSet(TimeRangeInlineFormSet):
    pass


class WeekDayHoursInlineFormSet(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        # Initialize week days only if no data is provided, otherwise no changes are detected on sub-forms save
        initial = (
            [{"week_day": weekday[0]} for weekday in ISO_WEEKDAY_CHOICES]
            if "data" not in kwargs
            else None
        )
        super().__init__(initial=initial, *args, **kwargs)


class GeneralHolidaysTimeRangeModelForm(TimeRangeModelForm):
    class Meta:
        model = GeneralHolidaysTimeRange
        exclude = []


class GeneralHolidaysTimeRangeInlineFormSet(TimeRangeInlineFormSet):
    pass


class GeneralHolidaysHoursInlineFormSet(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        initial = [{"closed": True}] if "data" not in kwargs else None
        super().__init__(initial=initial, *args, **kwargs)


class SpecificPeriodTimeRangeModelForm(TimeRangeModelForm):
    class Meta:
        model = SpecificPeriodTimeRange
        exclude = []


class SpecificPeriodTimeRangeInlineFormSet(TimeRangeInlineFormSet):
    pass


class SpecificPeriodHoursInlineFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        super().clean()

        forms_to_delete = self.deleted_forms
        valid_forms = [
            form
            for form in self.forms
            if form.is_valid() and form not in forms_to_delete
        ]

        interval_tree = IntervalTree()

        has_concurrent_periods = False
        for form in valid_forms:
            if "from_date" in form.cleaned_data and "to_date" in form.cleaned_data:
                from_timestamp = datetime.combine(
                    form.cleaned_data["from_date"], datetime.min.time()
                ).timestamp()
                to_timestamp = datetime.combine(
                    form.cleaned_data["to_date"], datetime.max.time()
                ).timestamp()

                overlap_set = interval_tree.overlap(from_timestamp, to_timestamp)

                if len(overlap_set) > 0:
                    overlap = list(overlap_set)[0]
                    overlap_form_data = overlap.data.cleaned_data
                    overlap_from = overlap_form_data["from_date"]
                    overlap_to = overlap_form_data["to_date"]
                    overlap_display = f"{overlap_from} - {overlap_to}"

                    form.add_error(
                        "from_date",
                        _(
                            "This period is in conflict with the period {overlap_display}"
                        ).format(overlap_display=overlap_display),
                    )
                    has_concurrent_periods = True

                interval = Interval(from_timestamp, to_timestamp, form)
                interval_tree.add(interval)

        if has_concurrent_periods:
            raise ValidationError(
                _("The form cannot be validated because some periods are in conflict")
            )
