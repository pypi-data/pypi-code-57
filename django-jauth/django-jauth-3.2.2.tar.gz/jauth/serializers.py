from datetime import timedelta
from django.contrib.auth.models import User
from django.db import transaction
from django.utils.timezone import now
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .helpers import account_kit_me, account_kit_get_access_token
from .helpers import facebook_get_access_token, facebook_me
from .models import AccountKitUser, AccountKitAccessToken
from .models import FacebookUser, FacebookAccessToken
from .helpers import google_me, google_get_access_token
from .models import GoogleUser, GoogleAccessToken


class AuthResultSerializer(serializers.Serializer):
    def to_representation(self, instance: User):
        assert isinstance(instance, User)
        token = Token.objects.get_or_create(user=instance)[0]
        return {
            'token': token.key,
            'user': {'id': instance.id, 'username': instance.username, 'email': instance.email},
        }


class AccountKitAuthTokenSerializer(serializers.Serializer):
    code = serializers.CharField(label=_("Code"), required=False)
    access_token = serializers.CharField(label=_("Access Token"), required=False)

    def validate(self, attrs):
        code = attrs.get('code', '')
        access_token = attrs.get('access_token', '')
        expire_time = None

        if not access_token:
            if not code:
                raise serializers.ValidationError(_('Unable to log in with provided credentials.') + ' (NO_CODE)', code='authorization')
            request_time = now()
            res = account_kit_get_access_token(code)
            if res.status_code != 200:
                raise serializers.ValidationError(_('Unable to log in with provided credentials.') + ' (INVALID_OR_USED_CODE)', code='authorization')
            data = res.json()
            access_token = data['access_token']
            expire_time = request_time + timedelta(seconds=data['token_refresh_interval_sec'])

        res = account_kit_me(access_token)
        if res.status_code != 200:
            raise serializers.ValidationError(_('Unable to log in with provided credentials.') + ' (ME)', code='authorization')
        me = res.json()
        ak_user_id = me['id']

        with transaction.atomic():
            fields = ['me']
            ak_user, created = AccountKitUser.objects.get_or_create(ext_user_id=ak_user_id)
            if created:
                user = User(username='ak-{}'.format(ak_user_id))
                user.save()
                ak_user.user = user
                fields.append('user')
            ak_user.me = me
            ak_user.save(update_fields=fields)
            ak_token, created = AccountKitAccessToken.objects.get_or_create(ext_user=ak_user, access_token=access_token, defaults={'expire_time': expire_time})
            if ak_token.expire_time != expire_time:
                ak_token.expire_time = expire_time
                ak_token.save(update_fields=['expire_time'])

        attrs['user'] = ak_user.user
        return attrs


class FacebookAuthTokenSerializer(serializers.Serializer):
    code = serializers.CharField(label=_("Code"), required=False)
    access_token = serializers.CharField(label=_("Access Token"), required=False)

    def validate(self, attrs):
        code = attrs.get('code', '')
        access_token = attrs.get('access_token', '')
        expire_time = None

        if not access_token:
            if not code:
                raise serializers.ValidationError(_('Unable to log in with provided credentials.') + ' (NO_CODE)', code='authorization')
            request_time = now()
            res = facebook_get_access_token(code)
            if res.status_code != 200:
                raise serializers.ValidationError(_('Unable to log in with provided credentials.') + ' (INVALID_OR_USED_CODE)', code='authorization')
            data = res.json()
            access_token = data['access_token']
            expire_time = request_time + timedelta(seconds=data["expires_in"])

        res = facebook_me(access_token)
        if res.status_code != 200:
            raise serializers.ValidationError(_('Unable to log in with provided credentials.') + ' (ME)', code='authorization')
        me = res.json()
        fb_user_id = me['id']

        with transaction.atomic():
            fields = ['me']
            fb_user, created = FacebookUser.objects.get_or_create(ext_user_id=fb_user_id)
            if created:
                user = User(username='fb-{}'.format(fb_user_id))
                user.save()
                fb_user.user = user
                fields.append('user')
            fb_user.me = me
            fb_user.save(update_fields=fields)
            fb_token, created = FacebookAccessToken.objects.get_or_create(ext_user=fb_user, access_token=access_token, defaults={'expire_time': expire_time})
            if fb_token.expire_time != expire_time:
                fb_token.expire_time = expire_time
                fb_token.save(update_fields=['expire_time'])

        attrs['user'] = fb_user.user
        return attrs


class GoogleAuthTokenSerializer(serializers.Serializer):
    code = serializers.CharField(label=_("Code"), required=False)
    access_token = serializers.CharField(label=_("Access Token"), required=False)

    def validate(self, attrs):
        code = attrs.get('code', '')
        access_token = attrs.get('access_token', '')
        expire_time = None

        if not access_token:
            if not code:
                raise serializers.ValidationError(_('Unable to log in with provided credentials.') + ' (NO_CODE)', code='authorization')
            request_time = now()
            res = google_get_access_token(code)
            if res.status_code != 200:
                raise serializers.ValidationError(_('Unable to log in with provided credentials.') + ' (INVALID_OR_USED_CODE)', code='authorization')
            data = res.json()
            access_token = data['access_token']
            expire_time = request_time + timedelta(seconds=data['expires_in'])

        res = google_me(access_token)
        if res.status_code != 200:
            raise serializers.ValidationError(_('Unable to log in with provided credentials.') + ' (ME)', code='authorization')
        me = res.json()
        gg_user_id = me['id']

        with transaction.atomic():
            fields = ['me']
            gg_user, created = GoogleUser.objects.get_or_create(ext_user_id=gg_user_id)
            if created:
                user = User(username='gg-{}'.format(gg_user_id))
                user.save()
                gg_user.user = user
                fields.append('user')
            gg_user.me = me
            gg_user.save(update_fields=fields)
            gg_token, created = GoogleAccessToken.objects.get_or_create(ext_user=gg_user, access_token=access_token, defaults={'expire_time': expire_time})
            if gg_token.expire_time != expire_time:
                gg_token.expire_time = expire_time
                gg_token.save(update_fields=['expire_time'])

        attrs['user'] = gg_user.user
        return attrs
