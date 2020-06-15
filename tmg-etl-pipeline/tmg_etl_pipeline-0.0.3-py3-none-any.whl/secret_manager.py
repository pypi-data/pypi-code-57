from google.cloud import secretmanager_v1
from google.cloud.exceptions import NotFound
import json


class Client:

    def __init__(self, project, secret_name):

        self._secrets = self.get_secret(project, secret_name)

    @property
    def secrets(self):
        return self._secrets

    @staticmethod
    def get_secret(project, secret_name, version='latest'):

        client = secretmanager_v1.SecretManagerServiceClient()
        name = client.secret_version_path(project, secret_name, version)

        try:
            response = client.access_secret_version(name)
            return json.loads(response.payload.data.decode('UTF-8'))
        except NotFound:
            return None
