from django import forms

# generic form {{{1
def get_generic_form(model_cls, field_list):
    class GenericForm(forms.ModelForm):
        class Meta:
            model = model_cls
            fields = field_list

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                current_cls = f"{field.widget.attrs['class']} " if 'class' in field.widget.attrs else ''
                field.widget.attrs['class'] = f"{current_cls}{model_cls.__name__.lower()}-{field_name}"
    return GenericForm

# import xls form {{{1
class ImportXlsForm(forms.Form):
   xls_file = forms.FileField()
