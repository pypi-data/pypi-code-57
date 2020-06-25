import logging
from django.db.models import Max
from datetime import timedelta
from django.utils import timezone  # use timezone.now() not datetime.now() in Django projects
from django.contrib.auth import get_user_model
import requests
from urllib.parse import urlparse
import jwt
from .serializers import get_user_serializer
# User = get_user_model()

logger = logging.getLogger(__name__)


def send_updated_user_data_to_client_applications(sender, instance, **kwargs) -> None:
    from oauth2_provider.models import Application, AccessToken  # note: receive error if at top of module
    if get_user_model() == sender:
        # Note This actually gets triggered any time the user logs in because of the "last login" field
        assert get_user_model().objects.get(pk=instance.pk) == instance, "Something went wrong!"  # todo: move to a test
        # data_to_push = {
        #     "id": instance.id,
        #     "username": instance.username,
        #     "email": instance.email,
        #     "first_name": instance.first_name,
        #     "last_name": instance.last_name,
        # }
        # from djangito_server.serializers import UserSerializer
        UserSerializer = get_user_serializer(sender)
        data_to_push = UserSerializer(instance).data
        # logger.debug(data_to_push)

        # this_url = 'http://127.0.0.1:8001'
        # identify applications that have been granted a token to this user
        applications_dict = AccessToken.objects.filter(user=instance).values(
            'application').annotate(max_expires=Max('expires')).filter(
            max_expires__gt=timezone.now() - timedelta(days=90))

        for x in applications_dict:
            client = Application.objects.get(pk=x['application'])
            token = jwt.encode(data_to_push, client.client_secret, algorithm='HS256').decode('utf-8')
            # payload = jwt.decode(token, client.client_secret, algorithms=['HS256'])
            uri_list = client.redirect_uris.split(' ')
            for uri in uri_list:
                parsed = urlparse(uri)
                if parsed.port:
                    base_uri = f"{parsed.scheme}://{parsed.hostname}:{parsed.port}"
                else:
                    base_uri = f"{parsed.scheme}://{parsed.hostname}"
                try:
                    res = requests.post(f'{base_uri}/oidc/push_server_data_to_client/', data={'token': token}, headers={
                                'Content-Type': 'application/x-www-form-urlencoded',
                    })
                    logger.info(f"[Push data] {base_uri}: {res} {res.text}")
                    # assert False
                except requests.exceptions.ConnectionError as e:
                    logger.info(f"{repr(e)}")
