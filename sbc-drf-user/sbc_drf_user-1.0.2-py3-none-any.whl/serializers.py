import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from sbc_drf import errors

from .errors import ErrMsg
from .models import User

L = logging.getLogger('app.' + __name__)


class UserSerializer(ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = get_user_model()
        write_only_fields = ('password',)
        read_only_fields = (
            'password_reset_requested_at',
            'password_reset_at',
            'is_password_reset'
        )
        exclude = ('password_reset_key', 'user_permissions', 'email_verification_key')
        exclude_on_update = ('password', 'email')
        extra_kwargs = {
            'password': {'validators': [validate_password]},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context.get('request').user

        # Exclude fields if current user is not superuser
        if user and user.is_superuser is False:
            for field in ('is_staff', 'is_superuser'):
                attrs.pop(field, None)

        return attrs

    def update(self, instance, validated_data):
        # Exclude these fields when user update itself
        if instance == self.context.get('request').user:
            for field in ('groups', 'user_permissions', 'is_active'):
                validated_data.pop(field, None)

        return super().update(instance, validated_data)


class ChangePasswordSerializer(Serializer):
    old_password = serializers.CharField(max_length=128, min_length=3, allow_blank=True, default='')
    new_password = serializers.CharField(
        max_length=128,
        min_length=3,
        required=True,
        validators=[validate_password]
    )

    def validate_old_password(self, value):
        user = self.context.get('user')
        request = self.context.get('request')
        is_valid_pwd = user.check_password(value)

        if user.id == request.user.id and is_valid_pwd is False:
            L.info('Old password does not match: %s', user)
            raise errors.ValidationError(*ErrMsg.MISMATCH_OLD_PWD_1002)

        if request.user.is_superuser is False and is_valid_pwd is False:
            L.info('Old password does not match: %s', user)
            raise errors.ValidationError(*ErrMsg.MISMATCH_OLD_PWD_1002)

        return value

    def create(self, validated_data):
        """
        Perform change password
        :return dict: validated_data
        """
        user = self.context.get('user')
        user.change_password(**validated_data)
        return validated_data


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    reset_key = serializers.CharField(required=True)
    new_password = serializers.CharField(max_length=128, min_length=3, required=True)

    def validate_email(self, value):
        try:
            return User.objects.get(email=value)
        except User.DoesNotExist:
            raise errors.ValidationError(*ErrMsg.EMAIL_NOT_EXISTS_1003)

    def validate(self, attrs):
        user = attrs.pop('email')

        attrs['email'] = user.email
        attrs['user'] = user

        if str(user.password_reset_key) != attrs['reset_key']:
            raise errors.ValidationError(*ErrMsg.EMAIL_PW_KEY_MISMATCH_1004)

        if user.is_password_reset is True:
            raise errors.ValidationError(*ErrMsg.PW_RESET_KEY_USED_1005)

        return attrs

    def create(self, validated_data):
        user = validated_data.pop('user')

        User.objects.reset_password(**validated_data)

        return user
