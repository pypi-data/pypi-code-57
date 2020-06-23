from .inputs import *
from .objects import *
from .http import *


def change_urls(api_url=None, authorization_url=None, standard_push_data_url=None):
    """
    Change API URLS

    :param api_url: new API URL
    :param authorization_url: new AUTHORIZATION URL
    :param standard_push_data_url: new STANDARD PUSH DATA URL
    """
    import opisense_client as oc
    # We need to change all those because these variables are string and are consequently copied and not referenced
    if api_url is not None:
        oc.API_URL = api_url
        oc.inputs.API_URL = api_url
        oc.http.API_URL = api_url
    if authorization_url is not None:
        oc.AUTHORIZATION_URL = authorization_url
        oc.inputs.AUTHORIZATION_URL = authorization_url
        oc.http.AUTHORIZATION_URL = authorization_url
    if standard_push_data_url is not None:
        oc.STANDARD_PUSH_DATA_URL = standard_push_data_url
        oc.inputs.STANDARD_PUSH_DATA_URL = standard_push_data_url
        oc.objects.STANDARD_PUSH_DATA_URL = standard_push_data_url