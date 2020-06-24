from material.frontend.views import ModelViewSet

from . import models

from rest_framework import viewsets, permissions
from . import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers

class BusinessFormApiViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API végpont a cégformák törzs lekérdezésére.
    """
    queryset = models.BusinessForm.objects.all().order_by('-code')
    serializer_class = serializers.BusinessFormSerializer
    permission_classes = []

class BusinessFormModelViewSet(ModelViewSet):
    model = models.BusinessForm
    list_display = [
        'code',
        'name'
    ]

class ContributionApiViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API végpont a járulék törzs lekérdezésére.
    """
    queryset = models.Contribution.objects.all().order_by('-code')
    serializer_class = serializers.ContributionSerializer
    permission_classes = []

class ContributionModelViewSet(ModelViewSet):
    model = models.Contribution

class DiscountApiViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API végpont a kedvezmény törzs lekérdezésére.
    """
    queryset = models.Discount.objects.all().order_by('-code')
    serializer_class = serializers.DiscountSerializer
    permission_classes = [permissions.IsAuthenticated]

class DiscountModelViewSet(ModelViewSet):
    model = models.Discount

class LegalApiViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API végpont a jogviszony törzs lekérdezésére.
    """
    queryset = models.Legal.objects.all().order_by('-code')
    serializer_class = serializers.LegalSerializer
    permission_classes = [permissions.IsAuthenticated]

class LegalModelViewSet(ModelViewSet):
    model = models.Legal

class PretenceApiViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API végpont a jogcím törzs lekérdezésére.
    """
    queryset = models.Pretence.objects.all().order_by('-code')
    serializer_class = serializers.PretenceSerializer
    permission_classes = [permissions.IsAuthenticated]


class PretenceModelViewSet(ModelViewSet):
    model = models.Pretence


class TaxApiViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API végpont a adónemek törzs lekérdezésére.
    """
    queryset = models.Tax.objects.all().order_by('-code')
    serializer_class = serializers.TaxSerializer
    permission_classes = []


class TaxModelViewSet(ModelViewSet):
    model = models.Tax


class PauseCategoryApiViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API végpont a társadalom biztosítás szüneteltetése törzs lekérdezésére.
    """
    queryset = models.PauseCategory.objects.all().order_by('-code')
    serializer_class = serializers.PauseCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class PauseCategoryModelViewSet(ModelViewSet):
    model = models.PauseCategory

class TimesheetCategoryApiViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API végpont a jelenlét törzs lekérdezésére.
    """
    queryset = models.TimeSheetCategory.objects.all().order_by('-code')
    serializer_class = serializers.TimeSheetCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class TimeSheetCategoryModelViewSet(ModelViewSet):
    model = models.TimeSheetCategory

