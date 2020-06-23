from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Dependence
from .models import Employment
from customers.models import Customer
from commons.models import Person

# class ChangeDependentForm(forms.Form):
#     dependence = forms.ModelChoiceField(queryset=Person.objects.all()[:100], label=_('Eltartott'))
#
#     def __init__(self, *args, **kwargs):
#         self.employment = kwargs.pop('employment')
#         super(ChangeDependentForm, self).__init__(*args, **kwargs)
#
#     def save(self):
#         new_manager = self.cleaned_data['manager']
#
#         DeptManager.objects.filter(
#             department=self.department
#         ).set(
#             department=self.department,
#             employee=new_manager
#         )