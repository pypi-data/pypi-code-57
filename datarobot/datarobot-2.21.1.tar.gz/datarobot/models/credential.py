import trafaret as t
from trafaret.contrib.rfc_3339 import DateTime

from datarobot.models.api_object import APIObject
from ..utils import logger, encode_utf8_if_py2, pagination

logger = logger.get_logger(__name__)


class Credential(APIObject):
    _path = 'credentials/'
    _converter = t.Dict({
        t.Key('name'): t.String(),
        t.Key('credential_id'): t.String(),
        t.Key('creation_date'): DateTime(),
        t.Key('credential_type'): t.String(),
        t.Key('description'): t.String(allow_blank=True),
    }).allow_extra('*')

    def __init__(
        self,
        credential_id=None,
        name=None,
        credential_type=None,
        creation_date=None,
        description=None,
    ):
        self.credential_id = credential_id
        self.name = name
        self.credential_type = credential_type
        self.creation_date = creation_date
        self.description = description

    @classmethod
    def list(cls):
        """
        Returns list of available credentials.

        Returns
        -------
        credentials : list of Credential instances
            contains a list of available credentials.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> data_sources = dr.Credential.list()
            >>> data_sources
            [
                Credential('5e429d6ecf8a5f36c5693e03', 'my_s3_cred', 's3'),
                Credential('5e42cc4dcf8a5f3256865840', 'my_jdbc_cred', 'jdbc'),
            ]
        """

        return [
            cls.from_server_data(item) for item in
            pagination.unpaginate(
                cls._path, {}, cls._client
            )
        ]

    @classmethod
    def get(cls, credential_id):
        """
        Gets the Credential.

        Parameters
        ----------
        credential_id : str
            the identifier of the credential.

        Returns
        -------
        credential : Credential
            the requested credential.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> cred = dr.Credential.get('5a8ac9ab07a57a0001be501f')
            >>> cred
            Credential('5e429d6ecf8a5f36c5693e03', 'my_s3_cred', 's3'),
        """
        return cls.from_location('{}{}/'.format(cls._path, credential_id))

    def delete(self):
        """
        Deletes the Credential the store.

        Parameters
        ----------
        credential_id : str
            the identifier of the credential.

        Returns
        -------
        credential : Credential
            the requested credential.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> cred = dr.Credential.get('5a8ac9ab07a57a0001be501f')
            >>> cred.delete()
        """
        self._client.delete('{}{}/'.format(self._path, self.credential_id))

    @classmethod
    def create_basic(cls, name, user, password, description=None):
        """
        Creates the credentials.

        Parameters
        ----------
        name : str
            the name to use for this set of credentials.
        user : str
            the username to store for this set of credentials.
        password : str
            the password to store for this set of credentials.
        description : str, optional
            the description to use for this set of credentials.

        Returns
        -------
        credential : Credential
            the created credential.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> cred = dr.Credential.create_basic(
            ...     name='my_basic_cred',
            ...     user='username',
            ...     password='password',
            ... )
            >>> cred
            Credential('5e429d6ecf8a5f36c5693e03', 'my_basic_cred', 'basic'),
        """
        payload = {
            'name': name,
            'credentialType': 'basic',
            'user': user,
            'password': password,
            'description': description,
        }
        return cls.from_server_data(
            cls._client.post(cls._path, data=payload).json()
        )

    @classmethod
    def create_oauth(cls, name, token, refresh_token, description=None):
        """
        Creates the OAUTH credentials.

        Parameters
        ----------
        name : str
            the name to use for this set of credentials.
        token: str
            the OAUTH token
        refresh_token: str
            The OAUTH token
        description : str, optional
            the description to use for this set of credentials.

        Returns
        -------
        credential : Credential
            the created credential.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> cred = dr.Credential.create_oauth(
            ...     name='my_oauth_cred',
            ...     token='XXX',
            ...     refresh_token='YYY',
            ... )
            >>> cred
            Credential('5e429d6ecf8a5f36c5693e03', 'my_oauth_cred', 'oauth'),
        """
        payload = {
            'name': name,
            'credentialType': 'oauth',
            'token': token,
            'refreshToken': refresh_token,
            'description': description,
        }
        return cls.from_server_data(
            cls._client.post(cls._path, data=payload).json()
        )

    @classmethod
    def create_s3(
        cls,
        name,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        aws_session_token=None,
        description=None,
    ):
        """
        Creates the S3 credentials.

        Parameters
        ----------
        name : str
            the name to use for this set of credentials.
        aws_access_key_id : str, optional
            the AWS access key id.
        aws_secret_access_key : str, optional
            the AWS secret access key.
        aws_session_token : str, optional
            the AWS session token.
        description : str, optional
            the description to use for this set of credentials.

        Returns
        -------
        credential : Credential
            the created credential.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> cred = dr.Credential.create_s3(
            ...     name='my_s3_cred',
            ...     aws_access_key_id='XXX',
            ...     aws_secret_access_key='YYY',
            ...     aws_session_token='ZZZ',
            ... )
            >>> cred
            Credential('5e429d6ecf8a5f36c5693e03', 'my_s3_cred', 's3'),
        """
        payload = {
            'name': name,
            'credentialType': 's3',
            'awsAccessKeyId': aws_access_key_id,
            'awsSecretAccessKey': aws_secret_access_key,
            'awsSessionToken': aws_session_token,
            'description': description,
        }
        return cls.from_server_data(
            cls._client.post(cls._path, data=payload).json()
        )

    @classmethod
    def create_azure(
        cls,
        name,
        azure_connection_string,
        description=None,
    ):
        """
        Creates the Azure storage credentials.

        Parameters
        ----------
        name : str
            the name to use for this set of credentials.
        azure_connection_string : str
            the Azure connection string.
        description : str, optional
            the description to use for this set of credentials.

        Returns
        -------
        credential : Credential
            the created credential.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> cred = dr.Credential.create_azure(
            ...     name='my_azure_cred',
            ...     azure_connection_string='XXX',
            ... )
            >>> cred
            Credential('5e429d6ecf8a5f36c5693e03', 'my_azure_cred', 'azure'),
        """
        payload = {
            'name': name,
            'credentialType': 'azure',
            'azureConnectionString': azure_connection_string,
            'description': description,
        }
        return cls.from_server_data(
            cls._client.post(cls._path, data=payload).json()
        )

    def __repr__(self):
        return encode_utf8_if_py2(u'{}(\'{}\', \'{}\', \'{}\')'.format(
            self.__class__.__name__,
            self.credential_id,
            self.name,
            self.credential_type,
        ))
