from django import forms
from taggit.forms import TagField
from django.contrib.contenttypes.models import ContentType

from extras.forms import (
    AddRemoveTagsForm, CustomFieldBulkEditForm, CustomFieldModelCSVForm, CustomFieldFilterForm, CustomFieldModelForm,
    LocalConfigContextFilterForm,
)

from utilities.forms import (
    APISelect, APISelectMultiple, BootstrapMixin,DynamicModelChoiceField, DynamicModelMultipleChoiceField,TagFilterField,
)
from tenancy.forms import TenancyFilterForm, TenancyForm

from dcim.models import (Device, Region, Site, DeviceRole, Manufacturer,DeviceType, Platform,)
from .models import OxidizedNode
from .fields import SelectTextWidget
from .constants import NODE_MODELS

class OxidizedNodeFilterForm(BootstrapMixin, forms.Form):
    model = OxidizedNode
    field_order = ['q']

    q = forms.CharField(
        required=False,
        label='Search'
    )

class OxidizedNodeForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = OxidizedNode
        fields = ['name', 'ipaddress','node_model','group','device', ]

        help_texts = {
            'node_model': "Node Model"
        }

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['node_model'].widget = SelectTextWidget(data_list=NODE_MODELS, name='model')