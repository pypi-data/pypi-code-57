from rest_framework import serializers

from lionclaw.shipping.models.locations import Address, Country
from django.utils.translation import ugettext_lazy as _

class AddressSerializer(serializers.ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    class Meta:
        model = Address
        fields = "__all__"

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"
