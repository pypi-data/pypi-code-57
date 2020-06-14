from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import formats


class DateTimeFormatsIterator:
	def __iter__(self):
		yield from formats.get_format('DATETIME_INPUT_FORMATS')
		yield from formats.get_format('DATE_INPUT_FORMATS')


class FixedTimezoneDateTimeField(forms.Field):
	widget = forms.widgets.DateTimeInput
	input_formats = DateTimeFormatsIterator()
	default_error_messages = {
		'invalid': _('Enter a valid date/time.')
	}

	def __init__(self, *, input_formats=None, **kwargs):
		super().__init__(**kwargs)
		if input_formats is not None:
			self.input_formats = input_formats
	
	def strptime(self, value, format):
		return datetime.datetime.strptime(value, format)
	
	def prepare_value(self, value):
		output = value.astimezone(self.timezone).replace(tzinfo=None)
		return output
	
	def to_python(self, value):
		value = value.strip()
		tz_unaware = None
		for format in self.input_formats:
			try:
				tz_unaware = self.strptime(value, format)
				break
			except (ValueError, TypeError):
				continue
		if tz_unaware is None:
			raise ValidationError(self.error_messages['invalid'], code='invalid')
		return self.timezone.localize(tz_unaware)
