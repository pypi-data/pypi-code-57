import jwt
import requests


class AtlantisClient:
    """Cliente HTTP para comunicação com Atlantis

    :param str atlantis_url: Endereço da API do serviço Atlantis
    :param str client_id: ID do cliente cadastrado no Atlantis
    :param str client_secret: Secret do cliente cadastrado no Atlantis
    """

    def __init__(self, client_id=None, client_secret=None, atlantis_url='https://accounts.spacetimeanalytics.com'):
        self.atlantis_url = atlantis_url
        self._client_id = client_id
        self._client_secret = client_secret

    @property
    def client_id(self):
        if self._client_id is None:
            raise InvalidInitParameters('Missing ATLANTIS_CLIENT_ID on AtlantisClient initialization.')
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret

    def issue_token(self, code, redirect_uri):
        """Realiza a troca do code pelo token

        .. deprecated:: 0.0.8
            Use a biblioteca authlib.

        Exemplo:

        .. code-block:: python

            from stl_sdk.torpedo import AtlantisClient

            client = AtlantisClient('https://accounts.spacetimeanalytics.com', 'client_id_abc123', 'client_secret_123abc')
            token = client.issue_token('code123abc')

        :param code: Código concedido pelo Atlantis via redirect (authorization_code)
        :type code: str
        :param redirect_uri: Endereço de redirecionamento
        :type redirect_uri: str
        :return: Dicionário com os tokens: ``access_token``, ``id_token`` e ``refresh_token``
        :rtype: dict
        """
        response = requests.post(
            '{}/api/token'.format(self.atlantis_url),
            data={
                'code': code,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'
            })
        response.raise_for_status()
        return response.json()

    def get_public_key(self):
        """Obtém a chave pública do Atlantis para validação do token de acesso

        .. deprecated:: 0.0.8
            Use a biblioteca authlib.

        :return: Chave pública
        :rtype: str
        """
        response = requests.get('{}/api/jwks'.format(self.atlantis_url))
        response.raise_for_status()
        return response.json()

    def validate_token(self, id_token):
        """Valida token de acesso do usuário

        .. deprecated:: 0.0.8
            Use a biblioteca authlib.

        Exemplo:

        .. code-block:: python

            from stl_sdk.torpedo import AtlantisClient

            client = AtlantisClient('https://accounts.spacetimeanalytics.com', 'client_id_abc123', 'client_secret_123abc')
            token_payload = client.validate_token('tokenJwT')

        :param id_token: Token JWT do usuário gerado pelo Atlantis
        :type id_token: str
        :raises InvalidTokenError: Se o token estiver expirado ou alterado
        :return: Retorna o payload do token JWT
        :rtype: dict
        """
        public_key = self.get_public_key()

        try:
            return jwt.decode(id_token, public_key, audience=self.client_id)
        except Exception as err:
            raise InvalidTokenError(err)

    def introspect_token(self, access_token, raise_for_inactive=True):
        """Verifica se o access_token está válido

        :param access_token: Token do usuário gerado pelo Atlantis
        :type access_token: str
        :param raise_for_inactive: Retorna um erro caso o token esteja inativo, valor padrão `True`
        :type access_token: bool, opcional
        :return: Retorna dados do token: ``active``, ``email``, ``scope``, ``client_id``, ``exp``, etc..
        :rtype: dict
        """
        response = requests.post(
            '{}/api/introspect-token'.format(self.atlantis_url),
            data={
                'token': access_token,
                'token_type_hint': 'access_token',
                'client_id': self.client_id,
                'client_secret': self.client_secret
            })
        response.raise_for_status()

        json = response.json()

        if raise_for_inactive and json['active'] is False:
            raise InvalidTokenError('Inactive token')

        return json

    def introspect_api_key(self, api_key):
        """Verifica se a Api key é válida

        :param api_key: Api key gerada pelo Atlantis
        :type api_key: str
        :return: Retorna dados da api key: ``actions``, ``description``, ``created_at``, etc..
        :rtype: dict
        """
        response = requests.post(
            '{}/api/introspect-apikey'.format(self.atlantis_url),
            data={
                'apikey': api_key,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            })
        response.raise_for_status()
        return response.json()


class AtlantisClientFlask(AtlantisClient):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
        super().__init__()

    def init_app(self, app):
        self.atlantis_url = app.config['ATLANTIS_URL']
        self._client_id = app.config['ATLANTIS_CLIENT_ID']
        self._client_secret = app.config.get('ATLANTIS_CLIENT_SECRET')


class InvalidTokenError(RuntimeError):
    pass


class InvalidInitParameters(RuntimeError):
    pass
