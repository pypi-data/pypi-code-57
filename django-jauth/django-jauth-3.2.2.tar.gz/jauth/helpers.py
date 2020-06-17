# pylint: disable=logging-format-interpolation
import base64
import hashlib
import hmac
import json
import logging
from urllib.parse import urlencode

import requests
from django.conf import settings
from requests import Response
from rest_framework.exceptions import ValidationError


logger = logging.getLogger(__name__)


def http_request(method: str, url: str, **kwargs) -> Response:
    res = requests.request(method, url, **kwargs)
    logger.info('{} {} -------------------------------------------------------------------- '.format(method.upper(), url))
    logger.info('{}'.format(res.request.body))  # type: ignore
    logger.info('HTTP {} -------------------------------------------------------------------- '.format(res.status_code))
    logger.info('{}'.format(res.text))
    return res


def account_kit_get_access_token(code: str) -> Response:
    """
    GET https://graph.accountkit.com/v1.3/access_token?grant_type=authorization_code&code=<authorization_code>&access_token=AA|<facebook_app_id>|<app_secret>
    :param code:
    :return: dict
    """
    app_id = settings.ACCOUNT_KIT_APP_ID
    app_secret = settings.ACCOUNT_KIT_APP_SECRET
    url = settings.ACCOUNT_KIT_API_URL + '/access_token?grant_type=authorization_code&code={}&access_token=AA|{}|{}'.format(code, app_id, app_secret)
    res = http_request('get', url)
    return res


def account_kit_me(access_token: str) -> Response:
    """
    GET https://graph.accountkit.com/v1.3/me/?access_token=<access_token>
    :param access_token:
    :return: str
    """
    url = settings.ACCOUNT_KIT_API_URL + '/me?access_token={}'.format(access_token)
    res = http_request('get', url)
    return res


def facebook_get_access_token(code: str) -> Response:
    """
    :param code:
    :return: dict
    """
    app_id = settings.FACEBOOK_APP_ID
    app_secret = settings.FACEBOOK_APP_SECRET
    redirect_url = settings.FACEBOOK_REDIRECT_URL
    url = settings.FACEBOOK_API_URL + '/oauth/access_token?client_id={}&redirect_uri={}&client_secret={}&code={}'.format(
        app_id, redirect_url, app_secret, code)
    res = http_request('get', url)
    return res


def facebook_me(access_token: str) -> Response:
    """
    :param access_token:
    :return: str
    """
    url = settings.FACEBOOK_API_URL + '/me?access_token={}'.format(access_token)
    res = http_request('get', url)
    return res


def facebook_parse_signed_request(signed_request: str) -> dict:
    encoded_sig, payload = signed_request.split('.', 2)
    app_secret = settings.FACEBOOK_APP_SECRET
    data = json.loads(base64.b64decode(payload.replace('-_', '+/')))
    expected_sig = hmac.new(app_secret.encode(), msg=payload.encode(), digestmod=hashlib.sha256).digest()
    if expected_sig != encoded_sig:
        raise ValidationError("Expected signature does not match encoded signature in Facebook request")
    return data


def google_get_access_token(code: str) -> Response:
    """
    :param code:
    :return: dict
    """
    app_id = settings.GOOGLE_APP_ID
    app_secret = settings.GOOGLE_APP_SECRET
    redirect_url = settings.GOOGLE_REDIRECT_URL
    url = settings.GOOGLE_API_URL + '/oauth2/v4/token'
    data = {
        'code': code,
        'client_id': app_id,
        'client_secret': app_secret,
        'redirect_uri': redirect_url,
        'grant_type': 'authorization_code',
    }
    res = http_request('post', url, data=data)
    return res


def google_me(access_token: str) -> Response:
    """
    {
      "id": "107873301371187782400",
      "email": "kajala@gmail.com",
      "verified_email": true,
      "name": "Jani Kajala",
      "given_name": "Jani",
      "family_name": "Kajala",
      "picture": "https://lh4.googleusercontent.com/-g1HKAdB0pi0/AAAAAAAAAAI/AAAAAAACcbQ/pCyIjkFBHv8/photo.jpg",
      "locale": "en"
    }
    :param access_token:
    :return: str
    """
    url = settings.GOOGLE_API_URL + '/oauth2/v1/userinfo?alt=json&access_token={}'.format(access_token)
    res = http_request('get', url)
    return res


def google_login_url(state: str, scope: str = 'email profile', api_url: str = 'https://accounts.google.com/o/oauth2/v2/auth', **kw) -> str:
    return api_url + '?' + urlencode({
        'client_id': settings.GOOGLE_APP_ID,
        'redirect_uri': settings.GOOGLE_REDIRECT_URL,
        'state': state,
        'scope': scope,
        'response_type': 'code',
        **kw,
    })


def facebook_login_url(state: str, api_url: str = 'https://www.facebook.com/v3.3/dialog/oauth', **kw) -> str:
    return api_url + '?' + urlencode({
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': settings.FACEBOOK_REDIRECT_URL,
        'state': state,
        **kw,
    })


def account_kit_sms_login_url(state: str, api_url: str = 'https://www.accountkit.com/v1.0/basic/dialog/sms_login/', **kw) -> str:
    return api_url + '?' + urlencode({
        'app_id': settings.ACCOUNT_KIT_APP_ID,
        'redirect': settings.ACCOUNT_KIT_REDIRECT_URL,
        'state': state,
        'fbAppEventsEnabled': 'true',
        **kw,
    })


def oauth2_login_urls(state: str, **kw) -> dict:
    data = {}
    if hasattr(settings, 'ACCOUNT_KIT_APP_ID') and settings.ACCOUNT_KIT_APP_ID:
        data['account_kit_sms_login_url'] = account_kit_sms_login_url(state, **kw)
    if hasattr(settings, 'FACEBOOK_APP_ID') and settings.FACEBOOK_APP_ID:
        data['facebook_login_url'] = facebook_login_url(state, **kw)
    if hasattr(settings, 'GOOGLE_APP_ID') and settings.GOOGLE_APP_ID:
        data['google_login_url'] = google_login_url(state, **kw)
    return data
