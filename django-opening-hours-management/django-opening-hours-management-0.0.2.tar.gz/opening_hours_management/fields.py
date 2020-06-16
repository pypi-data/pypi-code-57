import datetime

from django import forms

from .widgets import SelectTimeWidget


class FormTimeField(forms.TimeField):
    widget = SelectTimeWidget

    def to_python(self, value):
        """
        Validate that the input can be converted to a time. Return a Python
        datetime.time object.
        """
        hour, minute = map(lambda x: int(x), value)
        return datetime.time(hour, minute, 0)
