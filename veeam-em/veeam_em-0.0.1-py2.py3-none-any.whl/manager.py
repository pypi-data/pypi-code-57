"""This module sends request to the Veeam Backup Enterprise Manager REST API.

`Veeam Backup Enterprise Manager
RESTful API  <https://helpcenter.veeam.com
/docs/backup/rest/em_web_api_reference.html?ver=100>`__,
and process response in JSON format.
"""

import os
import platform
from typing import Dict, List, Optional, Tuple, Union
from xml.etree import ElementTree

import requests
from requests import RequestException, Session
from requests.auth import HTTPBasicAuth
from veeam_em.const import (
    API_DEFAULT_CONTENT_TYPE, API_DEFAULT_XMLNS, API_ENDPOINT_BASE,
    API_VERSION, DEFAULT_DEBUG, DEFAULT_TIMEOUT, HORT_PLATFORMS, PACKAGE_NAME,
    VERIFY_SSL, __version__ as product_version)
from veeam_em.exceptions import VeeamEmError
from veeam_em.helper import debug_requests_on


class VeeamEm:
    """Class containing methods to interact with the Veeam EM REST API.

    Example::

       em = VeeamEm(tk)
       vss.get_accounts()

    If ``tk`` is ``None`` it will get the token from the
    ``VEEAMEM_API_TOKEN`` environment variable or generate a new
    via ``get_token`` with the function arguments or
    ``VEEAMEM_API_USER`` and ``VEEAMEM_API_USER_PASS``

    Example::

        em = VeeamEm(tk)
        em.get_token()

    """

    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'
    PATCH = 'PATCH'

    @property
    def api_token(self) -> str:
        """Return API token."""
        return self._api_token

    @api_token.setter
    def api_token(self, val: str) -> None:
        """Set API token."""
        self._api_token = val
        self.session.headers.update({'X-RestSvcSessionId': val})
        self.session.cookies.set(
            name='X-RestSvcSessionId', value=val, path='/api'
        )

    @property
    def content_type(self) -> str:
        """Return content_type set."""
        return self._content_type

    @content_type.setter
    def content_type(self, val: str) -> None:
        """Set content type in class and session."""
        self._content_type = val
        self.session.headers.update({'Accept': val, 'Content-Type': val})

    @property
    def user_agent(self) -> str:
        """Return user_agent."""
        return self._user_agent

    @user_agent.setter
    def user_agent(self, val: str):
        """Set user_agent in class and session."""
        self._user_agent = val
        self.session.headers.update({'User-Agent': val})

    @property
    def debug(self) -> str:
        """Get debug value."""
        return self._debug

    @debug.setter
    def debug(self, value) -> None:
        """Set debug value and turn on debug requests."""
        if value:
            debug_requests_on()
        self._debug = value

    @property
    def ssl_verify(self) -> bool:
        """Get ssl_verify value in class."""
        return self._ssl_verify

    @ssl_verify.setter
    def ssl_verify(self, val: bool) -> None:
        """Set ssl_verify value set."""
        if val is not None:
            self._ssl_verify = bool(val)

    def __init__(
        self,
        tk: Optional[str] = None,
        api_endpoint: Optional[str] = None,
        ssl_verify: Optional[bool] = None,
        debug: Optional[bool] = False,
        timeout: Optional[int] = None,
        session: Optional[Session] = None,
        content_type: Optional[str] = None,
        user_agent: Optional[str] = None,
        api_version: Optional[str] = None,
    ):
        """Create class instance of VeeamEm.

        :param tk: REST API Session Token. Also set by
          env var ``VEEAMEM_API_TOKEN``.
        :param api_endpoint: REST API endpoint base. Also
          set by env var ``VEEAMEM_API_ENDPOINT_BASE``.
        :param ssl_verify: Whether to verify ssl cert on
          server or not. Also set by env var
          ``VEEAMEM_VERIFY_SSL``.
        :param debug: Debug mode. Defaults to False. Also
          set by env var ``VEEAMEM_DEBUG``.
        :param timeout: Response timeout. Also set by env
          var ``VEEAMEM_TIMEOUT``.
        :param content_type: Accept and Content-Type
          headers are set. Either ``application/json`` or
          ``application/xml``. Defaults to ``application/json``.
          Also set by en var ``VEEAMEM_API_CONTENT_TYPE``.
        :param user_agent: Customize the user agent. Also
          set by env var ``VEEAMEM_API_UA``.
        :param api_version: Veeam API version. Defaults to
          ``latest``. Also set by env var ``VEEAMEM_API_VERSION``.
        :param session: Requests session in case session already
          exists.
        """
        self.xmlns = API_DEFAULT_XMLNS
        self.hor_platforms = HORT_PLATFORMS
        self._api_token = None
        # Veeam EM API uses session
        if session is None:
            session = Session()
        self.session = session
        # session data when get_token is called
        self.session_data = dict()
        # define user agent & content type
        self._user_agent = None
        self._content_type = None
        self._ssl_verify = None
        # set user agent & content type
        self.user_agent = user_agent or os.environ.get(
            'VEEAMEM_API_UA', self._default_user_agent()
        )
        self.content_type = content_type or os.environ.get(
            'VEEAMEM_API_CONTENT_TYPE', API_DEFAULT_CONTENT_TYPE
        )
        self._default_content_type = self.content_type
        # application token if any
        self.api_token = tk or os.environ.get('VEEAMEM_API_TOKEN')
        if ssl_verify is not None:
            self.ssl_verify = ssl_verify
        else:
            self.ssl_verify = os.environ.get('VEEAMEM_VERIFY_SSL', VERIFY_SSL)

        self.api_version = api_version or os.environ.get(
            'VEEAMEM_API_VERSION', API_VERSION
        )
        self._debug = False  # type: Optional[bool]
        self.debug = debug or os.environ.get('VEEAMEM_DEBUG', DEFAULT_DEBUG)
        self.timeout = timeout or os.environ.get(
            'VEEAMEM_TIMEOUT', DEFAULT_TIMEOUT
        )
        self.api_endpoint_base = api_endpoint or os.environ.get(
            'VEEAMEM_API_ENDPOINT_BASE', API_ENDPOINT_BASE
        )
        self.api_endpoint = f'{self.api_endpoint_base}/api'
        self.token_endpoint = '{}/sessionMngr/?v={}'.format(
            self.api_endpoint, self.api_version
        )

    def __repr__(self) -> str:
        """Return the representation of the Configuration."""
        view = {
            "api_endpoint": self.api_endpoint,
            "api_token_endpoint": self.token_endpoint,
            "access_token": 'yes' if self.api_token is not None else 'no',
            "timeout": self.timeout,
            "content-type": self.content_type,
            "debug": self.debug,
        }
        return f"<{self.__class__.__name__} ({view})"

    @staticmethod
    def _default_user_agent(
        name: str = PACKAGE_NAME,
        version: str = product_version,
        extensions: str = '',
    ) -> str:
        """Create default user agent value."""
        environment = {
            'product': name,
            'product_version': version,
            'python_version': platform.python_version(),
            'system': platform.system(),
            'system_version': platform.release(),
            'platform_details': platform.platform(),
            'extensions': extensions,
        }
        # User-Agent:
        # <product>/<version> (<system-information>)
        # <platform> (<platform-details>) <extensions>
        user_agent = (
            '{product}/{product_version}'
            ' ({system}/{system_version}) '
            'Python/{python_version} ({platform_details}) '
            '{extensions}'.format(**environment)
        )
        return user_agent

    def whoami(self) -> Optional[Dict]:
        """Check if sessionId is valid."""
        if 'SessionId' in self.session_data:
            return self.get_logon_session(self.session_data['SessionId'])
        return None

    def get_token(
        self, user: Optional[str] = None, password: Optional[str] = None
    ) -> str:
        """Generate a new access token based on user/pass."""
        username = user or os.environ.get('VEEAMEM_API_USER')
        password = password or os.environ.get('VEEAMEM_API_USER_PASS')
        username_u = (
            username.decode('utf-8')
            if isinstance(username, bytes)
            else username
        )
        password_u = (
            password.decode('utf-8')
            if isinstance(password, bytes)
            else password
        )
        rv = self.session.post(
            self.token_endpoint,
            auth=HTTPBasicAuth(username_u, password_u),
            timeout=self.timeout,
            verify=self.ssl_verify,
        )
        if rv.status_code == 201:
            try:
                self.api_token = rv.headers['X-RestSvcSessionId']
                data = self.process_rv(rv)
                # remove links
                del data['Links']
                self.session_data = data
            except KeyError:
                raise VeeamEmError('Could not generate token')
        else:
            rv.raise_for_status()
        return self.api_token

    def request(
        self,
        url: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        payload: Optional[Dict] = None,
        method: Optional[str] = None,
        auth: Optional[HTTPBasicAuth] = None,
        data: Optional[str] = None,
    ) -> Optional[Dict]:
        """Make request to given endpoint."""
        _headers = dict()
        _params = dict(v=self.api_version)
        if headers:
            _headers.update(headers)
        if params:
            _params.update(params)
        if not url.startswith('http'):
            url = self.api_endpoint + url

        # create kwargs
        request_kwargs = {
            'headers': _headers,
            'params': _params,
            'auth': auth,
            'url': url,
            'timeout': self.timeout,
            'verify': self.ssl_verify,
        }
        # validate which kind of content-type and
        # add payload/data accordingly
        if 'Content-Type' in _headers:
            self.content_type = _headers.get('Content-Type')
        if 'json' in self.content_type:
            request_kwargs['json'] = payload
        else:
            request_kwargs['data'] = data
        # method or default GET
        method = method or self.GET
        # lookup dictionary
        lookup = {
            self.POST: self.session.post,
            self.GET: self.session.get,
            self.DELETE: self.session.delete,
            self.PUT: self.session.put,
            self.OPTIONS: self.session.options,
            self.PATCH: self.session.patch,
        }
        try:
            try:
                resp = lookup[method](**request_kwargs)
                json = self.process_rv(resp)
            except KeyError:
                raise VeeamEmError(f"Unsupported method: {method}")
        except ValueError as e:  # requests.models.json.JSONDecodeError
            raise ValueError(
                "The API server did not "
                "respond with a valid JSON: {}".format(e)
            )
        except RequestException as e:  # errors from requests
            raise VeeamEmError(e)
        # set default content type
        self.content_type = self._default_content_type
        # set default response
        if resp.status_code not in [
            requests.codes.ok,
            requests.codes.accepted,
            requests.codes.no_content,
            requests.codes.created,
        ]:
            if json:
                if (
                    'Message' in json
                    or 'FirstChanceExceptionMessage' in json
                    or 'data' in json
                ):
                    msg = [f'{k}: {v}' for k, v in json.items()]
                    if self.debug:
                        _headers = [
                            f'{k}: {v}' for k, v in resp.headers.items()
                        ]
                        msg.extend(_headers)
                    msg = '; '.join(msg)
                    raise VeeamEmError(msg)
            resp.raise_for_status()
        return json

    def process_rv(self, response):
        """Process response data and code.

        :param response: request.response object
        :return: dict
        """
        _headers = dict(headers=response.headers)
        rv = dict(status=response.status_code)
        rv.update(_headers)
        # no content status
        if response.status_code == requests.codes.no_content:
            return rv.update(_headers) if self.debug else rv
        # 400s error
        elif 500 > response.status_code > 399:
            _rv = dict(
                error='user error', message='check request and try again'
            )
            if 'json' in response.headers.get('Content-Type', ''):
                # json content type
                _r = response.json()
                _rv['data'] = _r
            else:
                _rv['data'] = response.content
            rv.update(_rv)
        # 500+ server error
        elif response.status_code > 499:
            _rv = dict(error='server error', message='api error')
            if 'json' in response.headers.get('Content-Type', ''):
                # json content type
                _r = response.json()
                if 'Message' in _r:
                    _rv['Message'] = _r['Message']
                if 'FirstChanceExceptionMessage' in _r:
                    rv['FirstChanceExceptionMessage'] = _r[
                        'FirstChanceExceptionMessage'
                    ]
                if self.debug and 'StackTrace' in _r:
                    rv['StackTrace'] = _r['StackTrace']
                _rv['data'] = _r
            else:
                _rv['data'] = response.content
            rv.update(_rv)
        else:
            # everything else
            if response.headers.get(
                'Content-Disposition'
            ) and response.headers.get('Content-Type'):
                # validate if response is a file, if so, return
                # response object
                return response
            elif response.headers.get(
                'Content-Type'
            ) and 'json' in response.headers.get('Content-Type'):
                # json content type
                return response.json()
            elif response.headers.get(
                'Content-Type'
            ) and 'xml' in response.headers.get('Content-Type'):
                return dict(data=response.content)
            else:
                rv.update({})
        # add headers if debug
        if self.debug:
            rv.update(_headers)
        return rv

    @staticmethod
    def _get_uuid_from_uid(uid: str) -> Optional[str]:
        """Split uuid from uid."""
        if uid is not None:
            return uid.split(':')[3]
        return uid

    @staticmethod
    def _process_collection(items: List[Dict]) -> List[Dict]:
        """Process collection of items to add UID."""
        data = []
        for item in items:
            # Ugly API does not contain a UUID
            # just an URM. Extract UUID from URN
            # i.e:
            # urn:veeam:EnterpriseAccount:{uuid}
            # urn:veeam:EnterpriseRole:{uuid}
            item['UUID'] = VeeamEm._get_uuid_from_uid(item['UID'])
            data.append(item)
        return data

    def get_logon_sessions(self) -> Optional[List[Dict]]:
        """Get logon sessions.

        Represents a collection of currently existing
        logon sessions for Veeam Backup Enterprise
        Manager RESTful API.
        :return:
        """
        data = self.request('/logonSessions')
        return data.get('LogonSessions')

    def get_logon_session(self, session_id: str) -> Optional[Dict]:
        """Get logon session by session_id.

        Represents a currently existing logon session
        having the specified ID.

        Note:: returns 500 error if session
         does not exist. This may be a bug.

        :param session_id:
        :return:
        """
        data = self.request(f'/logonSessions/{session_id}')
        return data

    def create_account(
        self,
        name: str,
        a_type: str,
        roles_uid: List[str],
        flr_settings=None,
        sql_settings=None,
        h_scope_objects=None,
        restore_all_vms: bool = False,
        content_type: str = 'json',
    ):
        r"""Add a user or a group account with role and settings.

        :param name: Name of the account added to Veeam Backup
         Enterprise Manager. For a regular account, the name must
         be specified in the ``DOMAIN\\USERNAME`` format, for
         example: ``TECH\\william.fox``. For accounts of the
         ``ExternalUser`` and ``ExternalGroup`` type, the name
         must be specified in the User Principal Name (UPN) format,
         for example: ``william.fox@tech.com``.
        :param a_type: Type of account added to Veeam Backup
         Enterprise Manager. Possible values:
         - User
         - Group
         - ExternalUser
         - ExternalGroup
         Accounts of the ExternalUser and ExternalGroup type
         must be created for users who will access Veeam Backup
         Enterprise Manager using a single sign-on service.
        :param roles_uid: List of ID of the role assigned to the added account.
         To get a list of IDs for available roles,
         call :py:func:`get_roles`.
        :param h_scope_objects: Restore scope assigned to the
         added account.
        :param flr_settings: File-level restore restrictions
         assigned to the added account. see
         :py:func:`get_account_flr_settings_spec`
        :param sql_settings: SQL restore restrictions assigned
         to the added account. see :py:func:`get_account_sql_settings_spec`
        :param restore_all_vms: Defines whether the account must have
         permissions  to restore all VMs or not. If this
         parameter is set to False, the client must provide the
         restore scope in the ``h_scope_objects`` element.
        :param content_type: api format either json or xml
        :return:
        """
        optional = any([restore_all_vms, h_scope_objects])
        kwargs = dict(url='/security/accounts', method=self.POST)
        if not optional:
            raise VeeamEmError(
                'if restore_all_vms=False must provide h_scope_objects'
            )
        if content_type == 'json':
            payload = dict(
                AllowRestoreAllVms=restore_all_vms,
                AccountName=name,
                AccountType=a_type,
                Roles=list(map(self.get_account_role_spec, roles_uid)),
            )
            if flr_settings:
                payload['FlrSettings'] = flr_settings
            if sql_settings:
                payload['SqlSettings'] = sql_settings
            if h_scope_objects:
                payload['HierarchyScopeObjects'] = h_scope_objects
            # create payload
            kwargs.update(dict(payload=payload))
        else:
            xml_doc = ElementTree.Element(
                "EnterpriseAccountCreateSpec", attrib={'xmlns': self.xmlns}
            )
            # account type
            acc_type_node = ElementTree.SubElement(xml_doc, 'AccountType')
            acc_type_node.text = a_type
            # account name
            acc_name_node = ElementTree.SubElement(xml_doc, 'AccountName')
            acc_name_node.text = name
            # roles
            roles_node = ElementTree.SubElement(xml_doc, 'Roles')
            for role_uid in roles_uid:
                enterprise_role_node = ElementTree.SubElement(
                    roles_node, 'EnterpriseRole'
                )
                enterprise_role_uid_node = ElementTree.SubElement(
                    enterprise_role_node, 'EnterpriseRoleUid'
                )
                enterprise_role_uid_node.text = role_uid
            # restore all vms
            restore_all_vms_node = ElementTree.SubElement(
                xml_doc, 'AllowRestoreAllVms'
            )
            restore_all_vms_node.text = 'true' if restore_all_vms else 'false'
            # hierarchy scope objects
            if h_scope_objects:
                h_scope_objects_node = ElementTree.SubElement(
                    xml_doc, 'HierarchyScopeObjects'
                )
                for h_scope_object in h_scope_objects:
                    h_scope_object_dict = h_scope_object['HierarchyScopeItem']
                    h_scope_object_node = ElementTree.SubElement(
                        h_scope_objects_node, 'HierarchyScopeItem'
                    )
                    h_object_ref_node = ElementTree.SubElement(
                        h_scope_object_node, 'HierarchyObjRef'
                    )
                    h_object_ref_node.text = h_scope_object_dict[
                        'HierarchyObjRef'
                    ]
                    h_object_name_node = ElementTree.SubElement(
                        h_scope_object_node, 'ObjectName'
                    )
                    h_object_name_node.text = h_scope_object_dict['ObjectName']
            # File-Level Restore Settings
            if flr_settings:
                flr_settings_node = ElementTree.SubElement(
                    xml_doc, 'FlrSettings'
                )
                flr_in_place_node = ElementTree.SubElement(
                    flr_settings_node, 'FlrInplaceOnly'
                )
                flr_in_place_node.text = (
                    'true' if flr_settings.get('FlrInplaceOnly') else 'false'
                )
                if flr_settings.get('FlrExtentionRestrictions'):
                    flr_restr_node = ElementTree.SubElement(
                        flr_settings_node, 'FlrExtentionRestrictions'
                    )
                    flr_restr_node.text = flr_settings.get(
                        'FlrExtentionRestrictions'
                    )
            # SQL Restore Settings
            if sql_settings:
                sql_settings_node = ElementTree.SubElement(
                    xml_doc, 'SqlSettings'
                )
                deny_inp_node = ElementTree.SubElement(
                    sql_settings_node, 'DenyInPlaceRestore'
                )
                deny_inp_node.text = sql_settings.get('DenyInPlaceRestore')
            # creating payload aka data
            _kwargs = {
                'data': ElementTree.tostring(xml_doc),
                'headers': {'Content-Type': 'application/xml'},
            }
            kwargs.update(_kwargs)
        # make call
        data = self.request(**kwargs)
        return data

    @staticmethod
    def get_hierarchy_scope_object(
        h_object_ref: str, object_name: str
    ) -> Dict:
        """Get Hierarchy scope object.

        :param h_object_ref: Reference to the object in the
         virtual infrastructure hierarchy.
        :param object_name: Name of the object in the virtual
         infrastructure hierarchy.
        :return:
        """
        return dict(
            HierarchyScopeItem=dict(
                HierarchyObjRef=h_object_ref, ObjectName=object_name
            )
        )

    @staticmethod
    def get_hierarchy_scope_objects(objects: List[Tuple]) -> List[Dict]:
        """Get Hierarchy scope objects.

        :param objects: list of tuples. first item is ``HierarchyObjRef``:
        Reference to the object in the virtual infrastructure hierarchy.
        see :py:func:`get_hierarchy_obj_ref_type`.
        Second item is ``ObjectName``: Name of the object in the virtual
        infrastructure hierarchy.
        :return: list of dictionaries
        """
        result = []
        for obj in objects:
            item = VeeamEm.get_hierarchy_scope_object(obj[0], obj[1])
            result.append(item)
        return result

    @staticmethod
    def get_account_sql_settings_spec(deny_in_place_restore: bool) -> Dict:
        """Get SQL restore restrictions assigned to the added account.

        :param deny_in_place_restore: Defines whether you want to
         prevent user account from overriding production databases
         at restore.
        :return: dict
        """
        return dict(DenyInPlaceRestore=deny_in_place_restore)

    @staticmethod
    def get_account_flr_settings_spec(
        in_place_only: bool = False, ext_restriction: str = None
    ) -> Dict:
        """Get File-level restore restrictions assigned to the added account.

        :param in_place_only: Defines whether the account must have
         permissions to restore only files with specific filename
         extensions or not. If this parameter is set to True, the
         client must provide filename extensions for files that are
         permitted for restore in the ``ext_restriction`` element.
        :param ext_restriction: Filename extensions for files that
         are permitted for restore separated by ',' (comma),
         for example: doc,pptx,pdf.
        :return: dict
        """
        spec = dict(FlrInplaceOnly=in_place_only)
        if in_place_only and not ext_restriction:
            raise VeeamEmError('ext_restriction is required')
        if in_place_only and ext_restriction is not None:
            spec['FlrExtentionRestrictions'] = ext_restriction
        return spec

    @staticmethod
    def get_account_role_spec(uid):
        """Get account role specification."""
        return dict(EnterpriseRole=[dict(EnterpriseRoleUid=uid)])

    def get_accounts(self) -> List[Dict]:
        """Get available accounts.

        Represents a collection of accounts having
        specific security roles in Veeam Backup
        Enterprise Manager.

        :return:
        """
        _data = self.request('/security/accounts')
        items = _data.get('Refs')
        data = self._process_collection(items)
        return data

    def delete_account(self, uuid: str):
        """Remove account from system.

        Removes an account having the specified ID and a specific
        security role from Veeam Backup Enterprise Manager.
        :param uuid: account identifier
        :return:
        """
        return self.request(f'/security/accounts/{uuid}', method=self.DELETE)

    def get_account(self, uuid: str):
        """Get account by uuid.

        Represents an account having the specified ID.
        The account is added to Veeam Backup Enterprise
        Manager and is assigned a specific security role.

        :param uuid: item unique identifier
        :return:
        """
        data = self.request(
            f'/security/accounts/{uuid}', params=dict(format='Entity')
        )
        if data:
            data['UUID'] = self._get_uuid_from_uid(data['UID'])
        return data

    def get_accounts_by_name(self, name: str) -> List[Dict]:
        """Filter account by name.

        :param name: account name or substring
        :return: list of items
        """
        return list(
            filter(
                lambda x: name.lower() in x['Name'].lower(),
                self.get_accounts(),
            )
        )

    def get_account_roles(self, uuid: str) -> Dict:
        """Get account roles by user uuid.

        Represents a security role or a collection of security
        roles assigned to the specified account that is added
        to Veeam Backup Enterprise Manager.

        :param uuid: item unique identifier
        :return:
        """
        data = self.request(
            f'/security/accounts/{uuid}/roles', params=dict(format='Entity')
        )
        return data

    def enable_all_vms_restore_scope_account(self, uuid: str) -> bool:
        """Enable ``All virtual machines`` option specified for the account.

        Assign permission to restore all VMs in the virtual infrastructure.
        """
        return self.update_all_vms_restore_scope_account(uuid, value=True)

    def disable_all_vms_restore_scope_account(self, uuid: str) -> bool:
        """Disable ``All virtual machines`` option specified for the account.

        Remove permission to restore all VMs in the virtual infrastructure.
        """
        return self.update_all_vms_restore_scope_account(uuid, value=False)

    def update_all_vms_restore_scope_account(
        self, uuid: str, value: bool
    ) -> bool:
        """Enable or Disable ``All virtual machines`` option for the account.

        The account added to Veeam Backup Enterprise Manager
        can be assigned a permission to restore all VMs in
        the virtual infrastructure or only those VMs that
        belong to a specific level: for example, VMs that
        reside in a specific resource pool. By sending the
        POST HTTP request to the ``/security/accounts/{ID}``
        URL, the client can toggle this setting to enabled
        or disabled.

        :param uuid: Account uuid
        :param value: Enable ``true``, disable ``false``.
        :return:
        """
        user_settings = self.get_account(uuid)
        if user_settings['AllowRestoreAllVms'] is not value:
            data = self.request(f'/security/accounts/{uuid}', method=self.POST)
            if data.get('status') == 204:
                return value
            else:
                return not value
        else:
            return value

    def add_role_to_account(self, uuid, account_uuid: str) -> Dict:
        """Add role to account by role uuid and account uuid.

        Assigns a Veeam Backup Enterprise Manager security role
        to the specified user account.
        :param uuid:
        :param account_uuid:
        :return:
        """
        payload = dict(EnterpriseRoleUid=uuid)
        data = self.request(
            f'/security/accounts/{account_uuid}/roles',
            method=self.POST,
            payload=payload,
        )
        return data

    def remove_role_from_account(
        self, uuid: str, account_uuid: str
    ) -> Optional[Dict]:
        """Remove role from account by role uuid and account uuid.

        Removes the Veeam Backup Enterprise Manager security
        role from the account having the specified ID.

        :param uuid: role identifier
        :param account_uuid: account identifier
        :return:
        """
        data = self.request(
            f'/security/accounts/{account_uuid}/roles/{uuid}',
            method=self.DELETE,
        )
        return data

    def get_account_scopes(self, uuid: str) -> Dict:
        """Get Account Scopes.

        Represents a restore scope defined for the specified
        account that is added to Veeam Backup Enterprise
        Manager and is assigned a specific security role.

        :param uuid: item unique identifier
        :return:
        """
        data = self.request(
            f'/security/accounts/{uuid}/scopes', params=dict(format='Entity')
        )
        return data

    def get_account_scope(self, uuid: str, scope_uuid: str) -> Dict:
        """Get Account scope.

        Represents a specific restore scope defined for
        the specified account. The account is added to
        Veeam Backup Enterprise Manager and is assigned a
        specific security role.

        :return:
        """
        data = self.request(
            f'/security/accounts/{uuid}/scopes/{scope_uuid}',
            params=dict(format='Entity'),
        )
        return data

    def add_scope_to_account(
        self,
        account_uuid: str,
        h_object_ref: str,
        object_name: str,
        content_type: str = 'json',
    ):
        """Add Scope to Account.

        Assigns a restore scope to the account having the
        specified ID. The account is added to Veeam Backup
        Enterprise Manager and has a specific security role.

        :param account_uuid: account identifier
        :param h_object_ref: Reference to the object in the
         virtual infrastructure hierarchy.
        :param object_name: Name of the object in the virtual
         infrastructure hierarchy.
        :param content_type: whether to use xml or json api representation
        :return:
        """
        kwargs = dict(
            url=f'/security/accounts/{account_uuid}/scopes', method=self.POST,
        )
        if content_type == 'json':
            payload = self.get_hierarchy_scope_object(
                h_object_ref, object_name
            )
            # create payload
            kwargs.update(dict(payload=payload))
        else:
            xml_doc = ElementTree.Element(
                "HierarchyScopeCreateSpec", attrib={'xmlns': self.xmlns}
            )
            h_scope_object_node = ElementTree.SubElement(
                xml_doc, 'HierarchyScopeItem'
            )
            h_object_ref_node = ElementTree.SubElement(
                h_scope_object_node, 'HierarchyObjRef'
            )
            h_object_ref_node.text = h_object_ref
            h_object_name_node = ElementTree.SubElement(
                h_scope_object_node, 'ObjectName'
            )
            h_object_name_node.text = object_name
            # creating payload aka data
            _kwargs = {
                'data': ElementTree.tostring(xml_doc),
                'headers': {'Content-Type': 'application/xml'},
            }
            kwargs.update(_kwargs)
        data = self.request(**kwargs)
        return data

    def remove_scope_from_account(
        self, scope_uuid: str, account_uuid: str
    ) -> Optional[Dict]:
        """Remove scope from account.

        Removes a restore scope having the specified ID from the
        account having the specified ID. The account is added
        to Veeam Backup Enterprise Manager and is assigned a
        specific security role.

        :param scope_uuid: scope identifier
        :param account_uuid: account identifier
        :return:
        """
        data = self.request(
            f'/security/accounts/{account_uuid}/scopes/{scope_uuid}'
        )
        return data

    def get_roles(self) -> List[Dict]:
        """Get available Roles.

        Represents a collection of security roles used in
        Veeam Backup Enterprise Manager.

        Veeam Backup Enterprise Manager RESTful API exposes
        the following security roles:

         - Portal User
         - Portal Administrator
         - VM Restore Operator
         - File Restore Operator
         - Exchange Restore Operator
         - SQL Restore Operator

        :return: list
        """
        _data = self.request('/security/roles')
        items = _data.get('Refs')
        data = self._process_collection(items)
        return data

    def get_role(self, uuid: str) -> Dict:
        """Get role by UUID.

        Represents a Veeam Backup Enterprise Manager security
        role having the specified ID.

        :param uuid: item unique identifier
        :return: dict
        """
        data = self.request(
            f'/security/roles/{uuid}', params=dict(format='Entity')
        )
        if data:
            data['UUID'] = self._get_uuid_from_uid(data['UID'])
        return data

    def get_roles_by_name(self, name: str) -> List[Optional[Dict]]:
        """Get Roles by name.

        Returns Veeam Backup Enterprise Manager security
        roles with the provided name string
        :param name: name to filter
        :return:
        """
        filtered = list(
            filter(
                lambda x: name.lower() in x['Name'].lower(), self.get_roles()
            )
        )
        return filtered

    def get_hierarchy_roots(self):
        """Get Hierarchy Roots.

        Represents a collection of all virtualization hosts
        added to the Veeam backup servers connected to Veeam
        Backup Enterprise Manager.
        :return: list
        """
        _data = self.request('/hierarchyRoots')
        items = _data.get('Refs')
        data = self._process_collection(items)
        return data

    def get_hierarchy_root(self, uuid: str) -> Dict:
        """Get Hierarchy Root by UUID.

        Represents a virtualization host having the specified ID.
        The virtualization host is added to the Veeam backup
        server connected to Veeam Backup Enterprise Manager.

        :param uuid: item unique identifier
        :return:
        """
        data = self.request(
            f'/hierarchyRoots/{uuid}', params=dict(format='Entity')
        )
        if data:
            data['UUID'] = self._get_uuid_from_uid(data['UID'])
        return data

    def get_hierarchy_roots_by_name(self, name: str) -> List[Dict]:
        """Filter Hierarchy root by name.

        :param name: hierarchy root name or substring
        :return: list of items
        """
        return list(
            filter(
                lambda x: name.lower() in x['Name'].lower(),
                self.get_hierarchy_roots(),
            )
        )

    def get_hierarchy_obj_ref_platforms(self) -> List:
        """Get Hierarchy Object Reference Platforms.

        Platform is the platform on which the virtual infrastructure
        object is created: VMware, Hyperv or vCloud
        :return:
        """
        return [
            {'platform': k, 'types': v} for k, v in self.hor_platforms.items()
        ]

    def get_hierarchy_obj_ref_platform(
        self, platform_name: str
    ) -> Optional[Dict]:
        """Get Hierarchy Object Reference by platform name.

        Platform is the platform on which the virtual infrastructure
        object is created: VMware, Hyperv or vCloud
        :param platform_name: VMware, Hyperv or vCloud
        :return: dict
        """
        try:
            types = self.hor_platforms[platform_name]
            return {'platform': platform_name, 'types': types}
        except KeyError:
            return None

    def get_hierarchy_obj_ref_type(
        self,
        ref_platform: str,
        ref_type: str,
        ref_h_root_id: str,
        object_ref: str,
    ) -> str:
        """Get Hierarchy object reference type.

        The HierarchyObjRefType object describes a specific node in the virtual
        infrastructure hierarchy. This object must be constructed for requests
        that refer to some node or level in the virtual infrastructure
        hierarchy, for example, a request editing a job or assigning a restore
        scope to the account in Veeam Backup Enterprise Manager.

        The HierarchyObjRefType object is constructed as a string that has the
        following pattern:

            urn:<ref_platform>:<ref_type>:<ref_h_root_id>.<object_ref>

        :param ref_platform: is the platform on which the virtual
         infrastructure object is created: VMware, Hyperv or vCloud.
        :param ref_type: Type is the object type.
        :param ref_h_root_id: is an ID of the host on which the virtual
         infrastructure object resides. The HierarchyRootID can be
         obtained using the :py:func:`get_hierarchy_roots` or
         :py:func:`get_hierarchy_root` methods.
         is an ID of the host on which the virtual infrastructure
         object resides.
        :param object_ref: ObjectRef is an ID of the virtual infrastructure
         object itself: mo-ref or ID, depending on the virtualization platform.
        :return: str
        """
        # validate platform
        try:
            _platform_types = self.hor_platforms[ref_platform]
        except KeyError:
            _ps_s = ', '.join(self.hor_platforms.keys())
            raise VeeamEmError('platform error. choose from: %s' % _ps_s)
        # validate ref
        if ref_type not in _platform_types:
            _pt_s = ', '.join(_platform_types)
            raise VeeamEmError('type error. choose from: %s' % _pt_s)
        # validate ref_h_root_id if root does not exist,
        # 400 will be thrown
        _ = self.get_hierarchy_root(ref_h_root_id)
        return 'urn:{platform}:{type}:{h_root_id}.{object_ref}'.format(
            platform=ref_platform,
            type=ref_type,
            h_root_id=ref_h_root_id,
            object_ref=object_ref,
        )

    def get_lookup_service(
        self,
        host_uid: str,
        h_ref: str,
        obj_type: str = None,
        obj_name: str = None,
    ):
        """Get a resource of a specific virtual infrastructure object.

        /lookup?host={hostUID}&hierachyRef={hierachyRef}&name={objName}&type={objType}
        :param host_uid: hierarchy root id :py:func:`get_hierarchy_root`
        :param h_ref: hierachy reference :py:func:`get_hierarchy_obj_ref_type`
        :param obj_type: object type (optional)
        :param obj_name: object name. '*' to search by any name
        :return:
        """
        any_of = [host_uid, h_ref]
        if not any(any_of):
            raise VeeamEmError('must contain either one of: %s' % any_of)
        params = dict()
        if host_uid is not None:
            _ = self.get_hierarchy_root(host_uid)
            params['host'] = host_uid
        if h_ref is not None:
            params['hierachyRef'] = h_ref
        if obj_name is not None:
            params['name'] = obj_name
        if obj_type is not None:
            params['type'] = obj_type
        # call service
        data = self.request('/lookup', params=params)
        # TODO: verify response representation: collection, dict?
        return data
