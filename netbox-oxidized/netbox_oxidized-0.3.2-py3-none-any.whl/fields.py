from django import forms

class SelectTextWidget(forms.TextInput):

    def __init__(self, data_list, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name
        self.datalist = data_list
        self.attrs.update({'list':'list__%s' % self.name, 'class': 'form-control', 'placeholder': self.name})

        

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super().render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self.name

        for k, v in self.datalist.items():
            data_list += '<option value="%s">%s</option>' % (k, v)

        data_list += '</datalist>'

        return (text_html + data_list)