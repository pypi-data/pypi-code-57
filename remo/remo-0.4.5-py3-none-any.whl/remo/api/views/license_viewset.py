from rest_framework import mixins, viewsets
from remo_app.remo.models import License


class LicenseViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = License.objects.all()
