from django.conf import settings
from django.contrib import admin
from jauth.models import AccountKitUser, AccountKitAccessToken, FacebookAccessToken, FacebookUser, GoogleUser, \
    GoogleAccessToken


class JauthAdminBase(admin.ModelAdmin):
    pass


class AccountKitAdmin(JauthAdminBase):
    exclude = ()


class FacebookAdmin(JauthAdminBase):
    exclude = ()


class GoogleAdmin(JauthAdminBase):
    exclude = ()


if hasattr(settings, 'ACCOUNT_KIT_APP_ID') and settings.ACCOUNT_KIT_APP_ID:
    admin.site.register(AccountKitUser, AccountKitAdmin)
    admin.site.register(AccountKitAccessToken, AccountKitAdmin)
if hasattr(settings, 'FACEBOOK_APP_ID') and settings.FACEBOOK_APP_ID:
    admin.site.register(FacebookUser, FacebookAdmin)
    admin.site.register(FacebookAccessToken, FacebookAdmin)
if hasattr(settings, 'GOOGLE_APP_ID') and settings.GOOGLE_APP_ID:
    admin.site.register(GoogleUser, GoogleAdmin)
    admin.site.register(GoogleAccessToken, GoogleAdmin)

required_params = ['JAUTH_AUTHENTICATION_ERROR_REDIRECT', 'JAUTH_AUTHENTICATION_SUCCESS_REDIRECT']
for p in required_params:
    if not hasattr(settings, p):
        raise Exception('{} configuration missing'.format(p))
