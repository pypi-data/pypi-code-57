from rest_framework import serializers

from whisperer.models import Webhook, WebhookEvent


class WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webhook
        exclude = ('user',)


class WebhookEventSerializer(serializers.ModelSerializer):
    webhook = WebhookSerializer()

    class Meta:
        model = WebhookEvent
        fields = '__all__'
