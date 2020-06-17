from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class OAuthUser(models.Model):
    created = models.DateTimeField(_('created'), default=now, blank=True, db_index=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True)
    ext_user_id = models.CharField(db_index=True, max_length=32)
    me = JSONField(blank=True, default=dict)

    class Meta:
        abstract = True


class OAuthAccessToken(models.Model):
    access_token = models.CharField(max_length=255)
    expire_time = models.DateTimeField(db_index=True)

    class Meta:
        abstract = True


class AccountKitUser(OAuthUser):
    @property
    def phone(self) -> str:
        return self.me.get('phone', {}).get('number', '') if self.me else ''


class AccountKitAccessToken(OAuthAccessToken):
    ext_user = models.ForeignKey(AccountKitUser, on_delete=models.CASCADE, related_name='+')


class FacebookUser(OAuthUser):
    @property
    def picture_url(self) -> str:
        return settings.FACEBOOK_API_URL + '/{}/picture?type=square'.format(self.ext_user_id)

    @property
    def name(self) -> str:
        return self.me.get('name') if self.me else ''

    @property
    def first_name(self) -> str:
        name = self.name
        if name:
            parts = name.split(' ')
            return ' '.join(parts[:-1])
        return ''

    @property
    def last_name(self) -> str:
        name = self.name
        if name:
            parts = name.split(' ')
            return ' '.join(parts[-1:])
        return ''

    @property
    def phone(self) -> str:
        return self.me.get('phone', {}).get('number', '') if self.me else ''

    @property
    def email(self) -> str:
        return self.me.get('email', '') if self.me else ''


class FacebookAccessToken(OAuthAccessToken):
    ext_user = models.ForeignKey(FacebookUser, on_delete=models.CASCADE, related_name='+')


class GoogleUser(OAuthUser):
    @property
    def email(self) -> str:
        return self.me.get('email', '') if self.me else ''

    @property
    def verified_email(self) -> bool:
        return self.me.get('verified_email', False) if self.me else False

    @property
    def locale(self) -> str:
        return self.me.get('locale', '') if self.me else ''

    @property
    def picture_url(self) -> str:
        return self.me.get('picture', '') if self.me else ''

    @property
    def name(self) -> str:
        return self.me.get('name', '') if self.me else ''

    @property
    def first_name(self) -> str:
        return self.me.get('given_name', '') if self.me else ''

    @property
    def last_name(self) -> str:
        return self.me.get('family_name', '') if self.me else ''


class GoogleAccessToken(OAuthAccessToken):
    ext_user = models.ForeignKey(GoogleUser, on_delete=models.CASCADE, related_name='+')
