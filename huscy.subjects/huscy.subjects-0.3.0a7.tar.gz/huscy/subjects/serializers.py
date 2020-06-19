import logging

from datetime import date

from dateutil import relativedelta
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import exceptions, serializers

from huscy.subjects import helpers, models, services

logger = logging.getLogger('huscy.subjects')


class AddressSerializer(serializers.ModelSerializer):
    country = CountryField(initial='DE')

    class Meta:
        model = models.Address
        fields = (
            'city',
            'contact',
            'country',
            'id',
            'street',
            'zip_code',
        )


class PhoneSerializer(serializers.ModelSerializer):
    label_display = serializers.CharField(source='get_label_display', read_only=True)
    number = PhoneNumberField()

    class Meta:
        model = models.Phone
        fields = (
            'contact',
            'label',
            'label_display',
            'number',
        )


class ContactSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    age_in_months = serializers.SerializerMethodField()
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    phones = PhoneSerializer(many=True, read_only=True)

    class Meta:
        model = models.Contact
        fields = (
            'addresses',
            'age_in_months',
            'date_of_birth',
            'display_name',
            'email',
            'first_name',
            'gender',
            'gender_display',
            'id',
            'last_name',
            'phones',
        )

    def get_age_in_months(self, contact):
        delta = relativedelta.relativedelta(date.today(), contact.date_of_birth)
        return delta.years * 12 + delta.months


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = (
            'contact',
            'guardians',
            'id',
            'is_active',
        )

    def create(self, validated_data):
        request = self.context.get('request')
        logger.info('User %s tried to create new subject from ip %s',
                    request.user.username, helpers.get_client_ip(request))
        return services.create_subject(**validated_data)

    # to have POST and GET behave diffrent contact and guardians are not nested Serializers
    def to_representation(self, subject):
        representation = super(SubjectSerializer, self).to_representation(subject)
        representation.update({
            'contact': ContactSerializer(subject.contact, source='subject_contact').data,
            'guardians': ContactSerializer(subject.guardians, many=True, read_only=True,
                                           source='guardian_contacts').data,
            'is_child': subject.is_child,
            'is_patient': subject.is_patient,
        })
        return representation


class InactivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inactivity
        fields = (
            'subject',
            'until',
        )

    def create(self, validated_data):
        try:
            return services.set_inactivity(**validated_data)
        except ValueError:
            raise exceptions.ValidationError
