import functools
import inspect
import json
from typing import Callable, AnyStr
import warnings

from arcane.core import CLIENTS_PARAM, ALL_CLIENTS_RIGHTS
from arcane.datastore import Client as DatastoreClient
from arcane.pubsub import Client as PubSubClient
from flask import request
from firebase_admin import auth as firebase_auth

from .tracking import send_tracking_information
from .log import adscale_log
from .services import ServiceEnum

rights_mapper = {
    'None': 0,
    'Viewer': 1,
    'Editor': 2,
    'Admin': 3
}

CLIENTS_KIND = 'base-clients'


class IncorrectAccessRightsRouteImplementation(TypeError):
    pass


def check_access_rights(service: str,
                        required_rights: str,
                        datastore_client: DatastoreClient,
                        pubsub_client: PubSubClient,
                        receive_rights_per_client: bool=False,
                        auth_enabled: bool=True,
                        project: str=None
                        ) -> Callable[[Callable], Callable]:
    """
    This functions checks the authorizations from the current HTTP call.
    /!\ Must be the last decorator (right above the decorated function) when there are multiples decorators on
    a function in order to get job_func_signature.
    if receive_rights_per_client is set to True, function must accept an argument corresponding to CLIENTS_PARAM either
    as the last positional argument or as an named argument.
    """
    if required_rights == 'None' and not receive_rights_per_client:
        def check_rights(job_func: Callable) -> Callable:
            return job_func
        return check_rights

    def check_rights(job_func: Callable) -> Callable:

        if receive_rights_per_client:
            error_message_clients = \
                "CHECK_ACCESS_RIGHTS incompatibility:\n" \
                f'function {job_func.__name__} should have an explicit argument "{CLIENTS_PARAM}' \
                "if receive_rights_per_client is set to True. \n"\
                "The argument must either be the last positional argument or a named argument"
            job_func_signature = inspect.getfullargspec(job_func)
            if (not job_func_signature.args or CLIENTS_PARAM != job_func_signature.args[-1]) \
                    and CLIENTS_PARAM not in job_func_signature.kwonlyargs:
                if CLIENTS_PARAM in job_func_signature.args:
                    error_message_clients += f'\n {CLIENTS_PARAM} is present in positional argument but not in last position.'
                raise IncorrectAccessRightsRouteImplementation(error_message_clients)

        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            is_appengine_cron = request.headers.get('X-Appengine-Cron', False)

            if is_appengine_cron:
                print("App Engine calls service : "+service)
                return job_func(*args, **kwargs)

            if not auth_enabled:
                authorized_clients = [ALL_CLIENTS_RIGHTS]
            else:
                claims = {}
                token = str(request.headers.get('Authorization', '')).split(' ').pop()
                try:
                    claims = firebase_auth.verify_id_token(token)
                except ValueError as e:
                    if required_rights != 'None':
                        return {'detail': 'You don\'t have access to Adscale resources\n', 'firebase_log': str(e)}, 401

                try:
                    send_tracking_information(claims['email'], service, job_func.__name__, project,
                                              pubsub_client, datastore_client)
                except KeyError:
                    adscale_log(ServiceEnum.TRACKING, f'The user email is not contained in the claims')

                rights = rights_mapper.get(claims.get('features_rights', {}).get(service, 'None'), 0)
                authorized_clients = claims.get(CLIENTS_PARAM, [])
                required_rights_mapped = rights_mapper.get(required_rights, 0)
                if rights < required_rights_mapped:
                    return {'detail': "You don't have access to this resource : your rights are "
                            f"'{claims.get('features_rights', {}).get(service, 'None')}' for service '{service}'. "
                            f"You need '{required_rights}'.",
                            'claims': f"Your current rights are {json.dumps(claims, indent=4, sort_keys=True)}"}, 401

            if receive_rights_per_client:
                if CLIENTS_PARAM in kwargs:
                    warnings.warn(f'field {CLIENTS_PARAM} when calling {job_func.__name__} was already filled.\n'
                                  f'Crushing existing value {str(kwargs[CLIENTS_PARAM])}')
                if ALL_CLIENTS_RIGHTS in authorized_clients:
                    authorized_clients.remove(ALL_CLIENTS_RIGHTS)
                    clients_query = datastore_client.query()
                    clients_query.kind = CLIENTS_KIND
                    clients_query.keys_only()
                    authorized_clients.extend(
                        [client_entity.key.name for client_entity in clients_query.fetch()
                         if client_entity.key.name not in authorized_clients])
                kwargs[CLIENTS_PARAM] = sorted(set(authorized_clients))

            return job_func(*args, **kwargs)

        return wrapper
    return check_rights


def get_user_email(token: AnyStr=None) -> str:
    """
    retrieves user id from connexion header.
    may raise ValueError if Authorization token is invalid or if token did not have uid specified
    """
    if token is None:
        token = request.headers.get('Authorization', '').split(' ').pop()
        if not token:
            raise ValueError(f"Failed to retrieve token from http header from token {request.headers.get('Authorization', '')}")
    claims = firebase_auth.verify_id_token(token)
    try:
        mail_str = claims['email']
    except KeyError as e:
        raise ValueError('Failed to retrieve uid from token') from e
    if not isinstance(mail_str, str):
        raise ValueError(f'Uid key is mapped to {repr(mail_str)} (type: {type(mail_str)}) value in claims')
    return mail_str

def get_user_uid(token: AnyStr=None) ->str:
    """
    Retrieve user firebase uid from connexion header.

    Arguments:
        token {AnyStr} -- Token provided by the connexion header

    Raises:
        ValueError -- If we failed to retrieve token

    Returns:
        [str] -- user uid
    """

    if token is None:
        token = request.headers.get('Authorization', '').split(' ').pop()
        if not token:
            raise ValueError(f"Failed to retrieve token from http header from token {request.headers.get('Authorization', '')}")
    claims = firebase_auth.verify_id_token(token)

    return claims['uid']
