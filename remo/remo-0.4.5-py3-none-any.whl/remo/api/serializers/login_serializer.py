from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, exceptions

# Get the UserModel
UserModel = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        if email and password:
            return self.authenticate(email=email, password=password)

        msg = 'Must include "email" and "password".'
        raise exceptions.ValidationError(msg)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = None
        username = None

        if email:
            try:
                username = UserModel.objects.get(email__iexact=email).get_username()
            except UserModel.DoesNotExist:
                pass

        if username:
            user = self._validate_email(email, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = 'User account is disabled.'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Unable to log in with provided credentials.'
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs
