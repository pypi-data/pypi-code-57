from google.cloud import secretmanager


class SecretManager(object):

    def __init__(self, project_id: str, service_accout_json_file_path=None):
        """
        Init your google cloud secret manager handler
        :param project_id: str, required
        :param service_accout_json_file_path: str, optional. The file path to your service account json key file. If
                not specified, the client uses the default credentials from your environment.
        """

        self.project_id = project_id
        self.service_accout_json_file_path = service_accout_json_file_path

        # Create the Secret Manager client.
        if service_accout_json_file_path is None:
            self.client = secretmanager.SecretManagerServiceClient()
        else:
            self.client = secretmanager.SecretManagerServiceClient.from_service_account_file(service_accout_json_file_path)

        # Build the parent name from the project.
        self.project_path = self.client.project_path(project_id)

    def create_secret(self, secret_id: str, value=None, regions=None, labels=None):
        """
        If you not specify a value, you only create the secret, without value.

        :param secret_id: str, required. The secret_id you want to create.
        :param value: str, optional. Your secret value.
        :param regions: list, optional. Your list of regions where you want replicas of your secret.
        :param labels: dict, optional. Your GCP labels.
        :return: secret_id name or secret_id version (str)

        """
        # Create the secret.
        replicas = [{'location': 'europe-west4'}]
        if isinstance(regions, list):
            replicas = [{'location': region} for region in regions]

        response = self.client.create_secret(self.project_path, secret_id, {
            'replication': {
                'user_managed': {'replicas': replicas},
            },
            'labels': labels
        })

        if value is None:
            return response.name
        else:
            # Add secret version
            return self.add_secret_version(secret_id, value)

    def add_secret_version(self, secret_id: str, value: str):
        """
        Add a secret version with a value to your existing secret

        :param secret_id: str, required.
        :param value: str, required. Your secret value.
        :return:  secret_id version (str)
        """
        # Convert the string payload into a bytes.
        payload = value.encode('UTF-8')
        parent = self.client.secret_path(self.project_id, secret_id)

        # Add the secret version.
        response = self.client.add_secret_version(parent, {'data': payload})
        return response.name

    def access_secret_version(self, secret_id, version_id):
        """
        Get the value of your secret.

        :param secret_id: str, required
        :param version_id: str or int, required
        :return: secret data (str)  !!!WARNING: Do not print the secret in a production environment!!!
        """
        # Build the resource name of the secret version.
        name = self.client.secret_version_path(self.project_id, secret_id, version_id)
        # Access the secret version.
        response = self.client.access_secret_version(name)
        return response.payload.data.decode('UTF-8')

    def list_secret_versions(self, secret_id: str):
        """
        List all version of a specified secret.

        :param secret_id: str, required
        :return: list of all versions of your secret
        """
        parent = self.client.secret_path(self.project_id, secret_id)
        return [version for version in self.client.list_secret_versions(parent)]

    def list_secrets(self):
        """
        List all secrets in the given project.

        :return: list of all secret names
        """
        # Build the resource name of the parent project.
        parent = self.client.project_path(self.project_id)
        return [secret for secret in self.client.list_secrets(parent)]

    def get_secret(self, secret_id):
        """
        Get information about the given secret. This only returns metadata about
        the secret container, not any secret material.

        :param secret_id: str, required
        :return: A :class:`~google.cloud.secretmanager_v1.types.Secret` instance.

        """
        # Build the resource name of the secret.
        name = self.client.secret_path(self.project_id, secret_id)

        # Get the secret.
        return self.client.get_secret(name)

    def delete_secret(self, secret_id):
        """
        Delete the secret with the given name and all of its versions.

        :param secret_id: str, required
        """
        # Build the resource name of the secret.
        name = self.client.secret_path(self.project_id, secret_id)

        # Delete the secret.
        self.client.delete_secret(name)

if __name__ == '__main__':

    # First, enable the secret manager API  on GCP console

    # Init secretmanager object with your the default credential from your environment:
    #secretmanager = SecretManager("v135-5683-playground-goppold")
    # Init secretmanager object with your a service account json file - specify the path to your file:
    secretmanager = SecretManager("v135-5683-playground-goppold", "test.json")

    # Create a secret value
    secret_name = secretmanager.create_secret("my-secret")
    print(secret_name)
    # Create a secret with value
    secret_version_name = secretmanager.create_secret("my-secret-with-value", "This is my secret value")
    print(secret_version_name)
    # By default: regions=["europe-west4"] and labels=None. Please specify this params of you need to.

    # Add a secret value to a existing secret:
    secret_version_name_1 = secretmanager.add_secret_version("my-secret", "This is another secret value")
    print(secret_version_name_1)
    secret_version_name_2 = secretmanager.add_secret_version("my-secret", "This is a new verison of my secret value")
    print(secret_version_name_2)

    # Accessing value of a secret version: (!!!WARNING: Do not print the secret in a production environment!!!)
    value_1 = secretmanager.access_secret_version("my-secret", 1)
    print(value_1)
    value_2 = secretmanager.access_secret_version("my-secret", 2)
    print(value_2)
    value_3 = secretmanager.access_secret_version("my-secret-with-value", 1)
    print(value_3)

    # List all version of a specified secret:
    secret_verions = secretmanager.list_secret_versions("my-secret")
    print(secret_verions)

    # List all secrets in my project:
    secrets = secretmanager.list_secrets()
    print(secrets)

    # Get metadata of a specific secret:
    metadata = secretmanager.get_secret("my-secret")
    print(metadata.name)

    # Delete a secret with the given name and all of its versions:
    secretmanager.delete_secret("my-secret")
    secretmanager.delete_secret("my-secret-with-value")

