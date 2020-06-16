import datetime
import os
import sys
import threading
import time
import webbrowser
from json import JSONDecodeError
import warnings

import keyring
import jwt
import requests
import logging
import socket
from http.cookiejar import CookiePolicy

# import webview
from keyring.errors import PasswordDeleteError, NoKeyringError
from wrapt import ObjectProxy
from http import HTTPStatus
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from collections import defaultdict
from dli import __version__, __product__
from dli.analytics import AnalyticsHandler
from dli.client.listener import _Listener, can_launch
from dli.client.adapters import DLIBearerAuthAdapter, DLIAccountsV1Adapter, \
    DLIInterfaceV1Adapter, DLISamAdapter
from dli.client.components.urls import sam_urls, identity_urls
from dli.client.environments import _Environment
from dli.models.organisation_model import OrganisationModel
from dli.siren import siren_to_entity
from dli.client.components.auto_reg_metadata import AutoRegMetadata
from dli.client.components.datafile import Datafile
from dli.client.components.dataset import Dataset, Dictionary
from dli.client.components.me import Me
from dli.client.components.package import Package
from dli.client.components.search import Search
from dli.client.components.accounts import Accounts
from dli.client.exceptions import (
    DatalakeException, InsufficientPrivilegesException,
    InvalidPayloadException, UnAuthorisedAccessException,
    CatalogueEntityNotFoundException, AuthenticationFailure
)
from dli.models.paginator import Paginator
from dli.modules.dataset_module import DatasetModule
from dli.modules.package_module import PackageModule
from dli.models.dictionary_model import DictionaryModel
from dli.models.file_model import FileModel
from dli.models.instance_model import InstanceModel, \
    InstancesCollection as InstancesCollection_
from dli.models.package_model import PackageModel
from dli.models.dataset_model import DatasetModel
from dli.siren import PatchedSirenBuilder


class ModelDescriptor:
    """
    This class is responsible for extending the base type passed
    into the __init__ method with the instance of DliClient it has
    been created within, following the descriptor pattern.

    What this means practicably, is that under _client attribute of the 'new'
    type (class instance) there is a backreference to the DliClient,
    which then permits the type to access the shared session object of DliClient,
    rather than having to pass the session into each instance.

    Using an instance instantiated from the base type will not have the
    _client attribute available.
    """

    def __init__(self, model_cls=None):
        self.model_cls = model_cls

    def __get__(self, instance, owner):
        """Returns a model thats bound to the client instance"""
        return type(
            self.model_cls.__name__, (self.model_cls, ),
            {
                '_client': instance
            }
        )


class DliClient(Accounts, AutoRegMetadata,
                Datafile, Dataset, Dictionary,
                Me, Package, Search):
    """
    Definition of a client. This client mixes in utility functions for
    manipulating packages, datasets and datafiles.
    """

    Dataset = ModelDescriptor(DatasetModel)
    Instance = ModelDescriptor(InstanceModel)
    _InstancesCollection = ModelDescriptor(InstancesCollection_)
    _Pagination = ModelDescriptor(Paginator)
    _File = ModelDescriptor(FileModel)
    _Package = ModelDescriptor(PackageModel)
    _Organisation = ModelDescriptor(OrganisationModel)
    _DictionaryV2 = ModelDescriptor(DictionaryModel)

    _packages = ModelDescriptor(PackageModule)
    _datasets = ModelDescriptor(DatasetModule)

    _environment_class = _Environment

    def __init__(self, api_root, host=None, debug=None, strict=True,
                 access_id=None, secret_key=None, use_keyring=True):
        self._environment = self._environment_class(api_root)
        self.access_id = access_id
        self.secret_key = secret_key
        self.host = host
        self.debug = debug
        self.strict = strict
        self.use_keyring = use_keyring
        self.logger = logging.getLogger(__name__)
        self.logger.info(
            'Starting SDK session',
            extra={
               'catalogue': self._environment.catalogue,
               'consumption': self._environment.consumption,
               'strict' : strict,
               'version': __version__
            }
        )

        self._session = self._new_session()
        self._analytics_handler = AnalyticsHandler(self)

        self.packages = self._packages()
        self.datasets = self._datasets()

        if access_id is None and secret_key is not None:
            warnings.warn(
                'The parameter `api_key` will be deprecated in the future. '
                'We will be contacting users in the following months to '
                'explain how to migrate to the new authentication flow.',
                PendingDeprecationWarning
            )


    def _new_session(self):
        session = Session(
            self.access_id,
            self.secret_key,
            self._environment,
            self.host,
            logger=self.logger,
            use_keyring=self.use_keyring
        )
        return session

    @property
    def session(self):
        # if the session expired, then reauth
        # and create a new context
        if self._session.has_expired:
            self._session = self._new_session()
        return self._session


class Session(requests.Session):

    def __init__(
        self, access_id, secret_key, environment, host, auth_key=None,
            logger=None, auth_prompt=True, use_keyring=True
    ):
        super().__init__()
        self.auth_key = None
        self.logger = logger
        self.access_id = access_id
        self.secret_key = secret_key
        self._environment = environment
        self.use_keyring = use_keyring
        self.host = host
        self.siren_builder = PatchedSirenBuilder()
        if auth_prompt:
            self._auth_init(auth_key)
        # mount points to add headers to specific routing requests
        self._set_mount_adapters()

        # Don't allow cookies to be set.
        # The new API will reject requests with both a cookie
        # and a auth header (as there's no predictable crediential to choose).
        #
        # However the old API, once authenticated using a Bearer token, will
        # as a side effect of a request return a oidc_id_token which matches
        # the auth header. This is ignored.
        self.cookies.set_policy(BlockAll())

    def _reload_or_web_flow(self, raises=False):

        check_key = None
        issplit = False
        splitlen = 0

        if hasattr(self, "use_keyring") and self.use_keyring:
            try:
                check_key = keyring.get_password(
                    __product__, self._environment.catalogue)
                if check_key:
                    split_check = check_key.split("**split**")
                    if len(split_check) > 1:
                        issplit = True
                        splitlen = split_check[-1]
                        chunked_jwt = ''
                        # we must re-form the jwt
                        for ix in range(int(splitlen)):
                            chunked_jwt += keyring.get_password(
                                __product__, self._environment.catalogue + f"-{ix}")

                        check_key = chunked_jwt

            except NoKeyringError as nke:
                # disable the use of keyring
                self.use_keyring = False
                check_key = None
                print(
                    f"We've noticed that you seem to be trying to run the SDK in a "
                    f"headless machine but your application credential "
                    f" environment variables (DLI_ACCESS_KEY_ID and DLI_SECRET_ACCESS_KEY) "
                    f" aren't set or there is no keyring manager available.\n\n"
                    f"YOU MAY NEED TO LOGIN EVERY TIME.\n"
                    f"Please contact support at datalake-support@ihsmarkit.com.\n"
                    f"{str(nke)}"
                )
                if raises:
                    raise nke

        reloaded = None
        if check_key:
            try:
                reloaded = check_key
                decoded = jwt.decode(str.encode(reloaded), verify=False)
                if decoded.get("exp", 0) <= time.time():
                    try:
                        keyring.delete_password(__product__,
                                                self._environment.catalogue)
                        if issplit:
                            for ix in range(splitlen):
                                keyring.delete_password(
                                    __product__,
                                    self._environment.catalogue + f"-{ix}"
                                )
                    except PasswordDeleteError as e:
                        if hasattr(self, "logger"):
                            self.logger.info("No such password")
                    finally:
                        reloaded = None
            except Exception as e:
                raise e

        if reloaded:
            if hasattr(self, "logger") and self.logger is not None:
                self.logger.info(f"Using vault JWT "
                                 f"{__product__} "
                                 f"{self._environment.catalogue}")
            self.auth_key = reloaded
        elif not self.secret_key and not self.access_id:
            self.auth_key = self._get_web_auth_key()

    def _auth_init(self, auth_key=None):

        if auth_key:
            self.auth_key = auth_key
        elif self.secret_key and not self.access_id:
            self.auth_key = self._get_auth_key()
        elif self.access_id and self.secret_key:
            self.auth_key = self._get_SAM_auth_key()
        else:
            self._reload_or_web_flow()

        self.decoded_token = self._get_decoded_token()
        self.token_expires_on = self._get_expiration_date()

    def request(self, method, url, *args, **kwargs):

        if not urlparse(url).netloc:
            url = urljoin(self._environment.catalogue, url)

        kwargs.pop('hooks', None)
        hooks = {'response': self._response_hook}

        try:
            if self.logger:
                self.logger.debug(
                    'Request',
                    extra={
                        'method': method,
                        'request': url,
                        '-args': args,
                        '-kwargs': kwargs
                    }
                )

            return super().request(method, url, hooks=hooks, *args, **kwargs)
        except socket.error as e:
            raise ValueError(
                'Unable to process request due to a networking issue '
                'root cause could be a bad connection, '
                'not being on the correct VPN, '
                'or a network timeout '
            ) from e

    @property
    def has_expired(self):
        # We subtract timedelta from the expiration time in order to allow a safety window for
        # a code block to execute after a check has been asserted.
        return datetime.datetime.utcnow() > \
               (self.token_expires_on - datetime.timedelta(minutes=1))

    def _response_hook(self, response, *args, **kwargs):
        # Apologies for the ugly code. The startswith siren check
        # is to make this only relevant to the old API.
        response = Response(response, self.siren_builder)

        if self.logger:
            self.logger.debug(
                'Response',
                extra={
                    # 'content': response.content,
                    'status': response.status_code,
                    'method': response.request.method,
                    'request': response.request.url,
                    'headers': response.request.headers
                }
            )

        if not response.ok:
            exceptions = defaultdict(
                lambda: DatalakeException,
                {HTTPStatus.BAD_REQUEST: InvalidPayloadException,
                 HTTPStatus.UNPROCESSABLE_ENTITY: InvalidPayloadException,
                 HTTPStatus.UNAUTHORIZED: UnAuthorisedAccessException,
                 HTTPStatus.FORBIDDEN: InsufficientPrivilegesException,
                 HTTPStatus.NOT_FOUND: CatalogueEntityNotFoundException}
            )

            try:
                message = response.json()
            except (JSONDecodeError, ValueError):
                message = response.text

            raise exceptions[response.status_code](
                message=message,
                params=parse_qs(urlparse(response.request.url).query),
                response=response
            )

        return response

    def _set_mount_adapters(self):
        self.mount(
            urljoin(self._environment.catalogue, '__api/'),
            DLIInterfaceV1Adapter(self)
        )

        self.mount(
            urljoin(self._environment.catalogue, '__api_v2/'),
            DLIBearerAuthAdapter(self)
        )

        self.mount(
            self._environment.consumption, DLIBearerAuthAdapter(self)
        )

        self.mount(
            urljoin(self._environment.accounts, 'api/identity/v1/'),
            DLIAccountsV1Adapter(self)
        )

        self.mount(
            urljoin(self._environment.accounts, 'api/identity/v2/'),
            DLIBearerAuthAdapter(self)
        )

        self.mount(
            self._environment.sam, DLISamAdapter(self)
        )

        self.mount(
            self._environment.consumption, DLIBearerAuthAdapter(self)
        )

    def _get_decoded_token(self):
        return jwt.decode(self.auth_key, verify=False)

    def _get_expiration_date(self):
        default_timeout = (
            datetime.datetime.utcnow() +
            datetime.timedelta(minutes=55)
        )

        if 'exp' not in self.decoded_token:
            return default_timeout

        return datetime.datetime.utcfromtimestamp(
            self.decoded_token['exp']
        ) - datetime.timedelta(minutes=5)

    def _get_auth_key(self):
        # todo - calling this when JWT from web flow fails.
        try:
            response = self.post(
                '/__api/start-session',
                headers={
                    'Authorization': 'Bearer {}'.format(
                        self.secret_key
                    )
                }
            )
        except DatalakeException as e:
            raise AuthenticationFailure(
                message='Could not authenticate API key'
            ) from e

        return response.text

    def _get_SAM_auth_key(self):

        sam_response = self.post(
            urljoin(self._environment.sam, sam_urls.sam_token),
            data={
                "client_id": self.access_id,
                "client_secret":  self.secret_key,
                "grant_type": "client_credentials"
            },
            hooks={'response': self._response_hook}
        )

        token = sam_response.json()["access_token"]

        catalogue_response = self.post(
            urljoin(self._environment.accounts,
                    identity_urls.identity_token),
            data={
                "client_id": self.access_id,
                "subject_token": token
            },
            hooks={'response': self._response_hook},
        )

        _jwt = catalogue_response.json()["access_token"]
        return _jwt

    def _get_web_auth_key(self, callback=None):

        result, reason = can_launch(_Listener.DEFAULT_PORT)
        if not result:

            if not reason.startswith("[Errno 98]"):
                # we cannot simply raise, since another SDK may be blocking 8080
                # (98 already in use)
                # and be usable - but we can raise if we get a refusal
                # (111 connection refused)
                raise Exception(f"Cannot authenticate via user flow. Contact DL-Support"
                                f" or your system administrator.\nThis occurred because"
                                f" whilst trying to start the callback listener at"
                                f" {_Listener.LOCALHOST}:{_Listener.DEFAULT_PORT}.\n"
                                f"We received {reason} from the socket. This may indicate"
                                f" the socket is already in use or your firewall is"
                                f" blocking inbound connections.")
            else:
                # so we need to just hit it first, to see if it replies as expected
                try:
                    query = requests.get(
                        f"{_Listener.LOCALHOST}:{_Listener.DEFAULT_PORT}" \
                        f"/get/test")

                    if query.status_code != 404 or \
                            "jwt" not in query.json().keys() or \
                            query.json()["jwt"] != "None":
                        raise Exception(
                            f"Cannot authenticate via user flow. Contact DL-Support"
                            f" or your system administrator.\nThis occurred because"
                            f" whilst trying to contact the callback listener at"
                            f" {_Listener.LOCALHOST}:{_Listener.DEFAULT_PORT}.\n"
                            f"We received {reason} from the socket. This may indicate"
                            f" the socket is already in use (and not by another SDK"
                            f" instance or your firewall is blocking inbound "
                            f"connections.")
                    else:
                        result = True
                except requests.ConnectionError as e:
                    # may not even be up
                    result = True

        postbox = _Listener.run(_Listener.DEFAULT_PORT)
        time.sleep(1)
        # we may need a little time to start the instance in
        # some systems - else we request /get before started

        if callback is None:
            url = f"{_Listener.LOCALHOST}:{_Listener.DEFAULT_PORT}" \
                  f"/login?postbox={postbox}&{urlencode(self._environment.__dict__)}"
            try:
                # we need to check that the listener can actually listen
                # before we open the browser - so establish that a listener
                # is up and running, or can listen (not firewalled)
                # else we need to tell the user that their firewall is shut.
               webbrowser.open(url, new=1)

            except webbrowser.Error as e:
                print(f"We couldn't open a usable browser for you to authenticate."
                      f"Please copy this {url} into a browser on your system")

            # implement this instead if SAM changes made
            # as we can close the window once value captured.
            # window = webview.create_window(
            #     'Login', f"http://localhost:{_Listener.DEFAULT_PORT}/login",
            #     resizable=False
            # )
            #
            # def get_elements(window):
            #     heading = window.get_elements('#emailaddress')
            #
            #     if not heading:
            #         window = webview.create_window(
            #             'Login', f"https://catalogue-dev.udpmarkit.net/login",
            #             resizable=False
            #         )
            #         webview.start(get_elements, window, debug=False)
            #
            #
            # webview.start(get_elements, window, debug=False)

        else:
            callback(_Listener.DEFAULT_PORT, postbox)

        if result:
            while True:
                query = requests.get(f"{_Listener.LOCALHOST}:{_Listener.DEFAULT_PORT}" \
                      f"/get/{postbox}")
                if query.status_code != 200:
                    time.sleep(0.5)
                else:
                    str_jwt = query.json()["jwt"]
                    if str_jwt != "invalid":
                        _jwt = str.encode(str_jwt)
                        break
                    else:
                        print("You have another SDK login open. Complete that first.")
                        sys.exit(0)


            if hasattr(self, "use_keyring") and self.use_keyring:
                try:
                    keyring.set_password(__product__, self._environment.catalogue, str_jwt)
                except (Exception, OSError) as e:
                    # length issue on Windows > 1280 chars in Windows Credentials
                    if os.name == 'nt':
                        lens = 1000
                        chunks = [
                            str_jwt[i:i + lens]
                            for i in range(0, len(str_jwt), lens)
                        ]
                        try:
                            # index
                            keyring.set_password(
                                __product__,
                                self._environment.catalogue,
                                f"**split**{len(chunks)}"
                            )

                            # segments
                            for ix, chunk in enumerate(chunks):
                                keyring.set_password(
                                    __product__,
                                    self._environment.catalogue + f"-{ix}",
                                    chunk
                                )
                        except Exception as e:
                            logging.warning(str(e))
                    else:
                        logging.warning(str(e))

            # cleanup
            requests.post(f"{_Listener.LOCALHOST}:{_Listener.DEFAULT_PORT}/shutdown")
            # window.destroy()
            return str_jwt


class Response(ObjectProxy):

    def __init__(self, wrapped, builder, *args, **kwargs):
        super(Response, self).__init__(wrapped, *args, **kwargs)
        self.builder = builder

    def to_siren(self):
        # Pypermedias terminology, not mine
        python_object = self.builder._construct_entity(
            self.json()
        ).as_python_object()

        # Keep the response availible
        python_object._raw_response = self

        return python_object

    def to_many_siren(self, relation):
        return [
            siren_to_entity(c) for c in
            self.to_siren().get_entities(rel=relation)
        ]


class BlockAll(CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False
