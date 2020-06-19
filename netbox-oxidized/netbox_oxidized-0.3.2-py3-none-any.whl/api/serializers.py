from rest_framework.serializers import ModelSerializer
from netbox_oxidized.models import OxidizedNode

class NodeSerializer(ModelSerializer):

    class Meta:
        model = OxidizedNode
        fields = ['name', 'ipaddress', 'node_model', 'group']