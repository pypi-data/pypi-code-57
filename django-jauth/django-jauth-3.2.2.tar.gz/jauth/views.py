import json
import logging
from urllib.parse import urlencode
from django.conf import settings
from django.contrib import auth
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework.request import Request
from rest_framework.views import APIView
from .helpers import facebook_parse_signed_request
from .models import FacebookAccessToken, FacebookUser
from .serializers import AccountKitAuthTokenSerializer, FacebookAuthTokenSerializer, GoogleAuthTokenSerializer, \
    AuthResultSerializer


logger = logging.getLogger(__name__)


class OAuthRedirectViewBase(TemplateView):
    template_name = 'jauth/oauth-redirect.html'
    serializer_class = None
    result_serializer_class = AuthResultSerializer

    def get_context_data(self, **kw):
        request = self.request
        assert isinstance(request, HttpRequest)

        cx = {
            'auth_result_json': 'null',
            'status': 'not_authenticated',
        }
        for k, v in kw.items():
            if v:
                cx[k] = v

        data = request.GET.dict()
        if 'code' in data:
            serializer = self.serializer_class()  # pylint: disable=not-callable
            data = serializer.validate(data)
            user = data['user']
            cx['user'] = user
            if settings.JAUTH_AUTHENTICATION_SUCCESS_REDIRECT:
                auth.login(request, user)
                return cx
            result = self.result_serializer_class(user).data
            cx['auth_result_json'] = json.dumps(result)
            cx['status'] = 'ok'

        return cx

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            context = self.get_context_data(**kwargs)
            if settings.JAUTH_AUTHENTICATION_SUCCESS_REDIRECT:
                return redirect(settings.JAUTH_AUTHENTICATION_SUCCESS_REDIRECT)
            return self.render_to_response(context)
        except Exception as e:
            if settings.JAUTH_AUTHENTICATION_ERROR_REDIRECT:
                return redirect(settings.JAUTH_AUTHENTICATION_ERROR_REDIRECT + '?' + urlencode({'msg': str(e)}))
            return HttpResponse(content=str(e).encode(), status=401)  # HTTP 401 Unauthorized


class FacebookDeauthorizeView(APIView):
    def post(self, request: Request, *args, **kwargs):  # pylint: disable=unused-argument
        logger.info('FacebookDeauthorizeView BEGIN -----------------------')
        logger.info(request.POST.dict())
        signed_request = request.POST.get('signed_request')
        if not signed_request:
            return {}
        data = facebook_parse_signed_request(signed_request)
        logger.info('Parsed data:')
        logger.info(data)
        user_id = data['user_id']
        FacebookAccessToken.objects.filter(ext_user__ext_user_id=user_id).delete()
        logger.info('FacebookDeauthorizeView END -------------------------')
        return data


class FacebookDeleteView(APIView):
    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        logger.info('FacebookDeleteView BEGIN ----------------------------')
        logger.info(request.POST.dict())
        signed_request = request.POST.get('signed_request')
        data = facebook_parse_signed_request(signed_request)
        logger.info('Parsed data:')
        logger.info(data)
        user_id = data['user_id']
        FacebookUser.objects.filter(ext_user_id=user_id).delete()
        logger.info('FacebookDeleteView END ------------------------------')
        return data


class AccountKitRedirectView(OAuthRedirectViewBase):
    serializer_class = AccountKitAuthTokenSerializer  # type: ignore


class FacebookRedirectView(OAuthRedirectViewBase):
    serializer_class = FacebookAuthTokenSerializer  # type: ignore


class GoogleRedirectView(OAuthRedirectViewBase):
    serializer_class = GoogleAuthTokenSerializer  # type: ignore
