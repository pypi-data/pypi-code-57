import logging
import random
import time
import urllib.parse

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers, exceptions

from remo_app.remo.models import UserDetails

User = get_user_model()
logger = logging.getLogger('remo_app')


class UserInfoSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(source='is_superuser')

    class Meta:
        model = User
        fields = ('email', 'username', 'last_name', 'first_name', 'is_admin')


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    comment = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        # Create inactive user
        # Just collect user emails during singin up
        if get_user_model().objects.filter(email=validated_data['email']).exists():
            raise exceptions.ValidationError('User with such email already exists')

        with transaction.atomic():
            new_user = get_user_model().objects.create_user(
                username=validated_data['email'],
                email=validated_data['email'],
                password=None,
                is_staff=False,
                is_superuser=False,
                is_active=False
            )
            if 'comment' in validated_data:
                UserDetails.objects.create(
                    user=new_user,
                    comment=validated_data['comment']
                )
            if settings.HUBSPOT_API_KEY is not None and not self.create_hubspot_user(validated_data):
                raise exceptions.APIException('Error occurred during interacting HubSpot')

        return new_user

    def create_hubspot_user(self, validated_data):
        api_key = urllib.parse.quote(settings.HUBSPOT_API_KEY)
        data = {
            'email': validated_data['email'],
            'firstname': None,
            'lastname': None,
            'website': None,
            'company': None,
            'phone': None,
            'address': None,
            'city': None,
            'state': None,
            'zip': None,
            'jobtitle': validated_data.get('comment')
        }
        api_properties = [{'property': k, 'value': v} for k, v in data.items()]

        counter = 0
        while counter < settings.HUBSPOT_API_THROTTLING_RETRIES:
            response = requests.post(
                'https://api.hubapi.com/contacts/v1/contact/?hapikey={}'.format(api_key),
                json={'properties': api_properties}
            )

            if response.status_code == 200:
                break

            # Request limit exceeded
            if response.status_code == 429:
                try:
                    err = response.json()

                    # Daily limit exceeded, nothing we can do
                    if err['policyName'].lower() == 'daily':
                        logger.error(
                            'Daily requests limit exceeded, email: %s',
                            validated_data['email']
                        )
                        return False

                    # Secondly limit exceeded, wait increasing random time
                    logger.warning(
                        'Secondly requests limit exceeded, slowing down, email: %s',
                        validated_data['email']
                    )
                    time.sleep(random.randrange(counter, (counter + 1) * 2))
                except (ValueError, KeyError):
                    logger.error(
                        'Hubspot returned wrong data for 429 status code'
                    )

            counter += 1

        return True
