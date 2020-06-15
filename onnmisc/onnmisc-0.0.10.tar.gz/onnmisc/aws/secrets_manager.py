import boto3
from botocore.exceptions import ClientError

DEFAULT_CLIENT = boto3.client('secretsmanager')


def create_secret(name, secret_string, description='', tags=(), client=DEFAULT_CLIENT) -> None:
    """Description:
        Creates/updates a Secrets Manager secret

    Args:
        name: Name of the secret
        secret_string: Secret string
        description: Description of the secret
        tags: AWS tags
        client: Boto3 client

    Example:
        Example usage:

            >>> from onnmisc.aws.secrets_manager import create_secret
            >>> from onnmisc.aws.cfn import dict_to_cfn_tags
            >>>
            >>> dict_tags = {'Name': 'Conformity', 'Team': 'Security'}
            >>> tags = dict_to_cfn_tags(dict_tags)
            >>> create_secret('Conformity', 'aaaaabbbbbccccc', description='Conformity API key', tags=tags)

    Returns:
        None

    """
    try:
        client.create_secret(
            Name=name,
            Description=description,
            SecretString=secret_string,
            Tags=tags,
        )

        return

    except ClientError as e:
        msg = e.response['Error']['Message']
        if 'already exists' not in msg:
            raise

    # Create new version if secret already exists
    client.put_secret_value(
        SecretId=name,
        SecretString=secret_string,
        VersionStages=['AWSCURRENT'],
    )

