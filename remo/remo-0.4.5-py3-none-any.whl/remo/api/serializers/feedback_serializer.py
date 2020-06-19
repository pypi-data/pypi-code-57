from rest_framework import serializers

from remo_app.remo.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        exclude = ('user',)
