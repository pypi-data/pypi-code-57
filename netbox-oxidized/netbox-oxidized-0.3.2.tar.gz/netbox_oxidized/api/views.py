from rest_framework.viewsets import ModelViewSet

from netbox_oxidized.models import OxidizedNode
from .serializers import NodeSerializer
#from .pagination import DataOnlyPagination


class NodeViewSet(ModelViewSet):
    queryset = OxidizedNode.objects.all()
    serializer_class = NodeSerializer
    paginator = None

