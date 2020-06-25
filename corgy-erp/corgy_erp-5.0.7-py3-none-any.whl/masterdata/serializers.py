from .models import BusinessForm
from .models import Contribution
from .models import Discount
from .models import Legal
from .models import PauseCategory
from .models import Pretence
from .models import Tax
from .models import TimeSheetCategory
from . import models
from rest_framework import serializers


class BusinessFormSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.BusinessForm
        fields = ['pk', 'code', 'name']


class ContributionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Contribution
        fields = ['pk', 'code', 'name']

class DiscountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Discount
        fields = ['pk', 'code', 'name']


class LegalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Legal
        fields = ['pk', 'code', 'name']


class PretenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Pretence
        fields = ['pk', 'code', 'name']

class TaxSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Tax
        fields = ['pk', 'code', 'name']

class PauseCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.PauseCategory
        fields = ['pk', 'code', 'name']


class TimeSheetCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.TimeSheetCategory
        fields = ['pk', 'code', 'name']
