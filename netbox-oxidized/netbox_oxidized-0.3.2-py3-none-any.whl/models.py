from django.db import models
from django.urls import reverse
from extras.models import CustomFieldModel
from extras.utils import extras_features
from utilities.models import ChangeLoggedModel
from ipam.validators import DNSValidator

@extras_features('custom_fields')
class OxidizedNode(ChangeLoggedModel):
    name = models.CharField(
        max_length=255,
        blank=True,
        validators=[DNSValidator],
        verbose_name='Node Name',
        help_text='Hostname or FQDN (not case-sensitive)'
    )
    ipaddress = models.CharField(
        max_length=255,
        verbose_name='IP Address',
        help_text='IP Address of the node'

    )
    node_model = models.CharField(
        max_length=255,
        verbose_name='Node Model',
        help_text='An Oxidized Supported OS'
    )

    group = models.CharField(
        max_length=255,
        verbose_name='Node Group',
        help_text='The group the node belongs to'
    )

    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.CASCADE,
        related_name='oxidizednodes',
        blank=True,
        null=True
    )
    csv_headers = ['site', 'name', 'ipaddress', 'node_model','group', 'device', ]
    clone_fields = ['group','node_model']

    class Meta:
        ordering =['device', 'name']

    def get_absolute_url(self):
        return reverse('plugins:netbox_oxidized:oxidizednode', args=[self.pk])

    def site(self):
        return self.device.site_id
