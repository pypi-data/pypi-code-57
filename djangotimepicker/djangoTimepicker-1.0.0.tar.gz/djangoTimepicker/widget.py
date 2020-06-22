from django.forms import DateTimeInput


class DjangoTimePickerInput(DateTimeInput):
    template_name = 'datetimepicker.html'

    def __init__(self, attrs=None, timeFormat='Y:m:d H:i:s', language='zh'):
        
        super(DjangoTimePickerInput, self).__init__(attrs)
        self.timeFormat = timeFormat
        self.language = language

    def get_context(self, name, value, attrs):
        context = super(DjangoTimePickerInput, self).get_context(name, value, attrs)
        context['widget']['timeFormat'] = self.timeFormat
        context['widget']['language'] = self.language
        return context