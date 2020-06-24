import os
from shutil import copyfile
from google.cloud import iam_credentials_v1

default_key_path = os.path.join(os.path.expanduser('~'), '.deepmap', 'access-key.json')


def get_service_account_request_token(cred, url):
    cred = cred.with_scopes(['https://www.googleapis.com/auth/iam'])

    client = iam_credentials_v1.IAMCredentialsClient(credentials=cred)
    name = client.service_account_path('-', cred.service_account_email)
    token = client.generate_id_token(name, url).token
    return token


def get_service_account_request_headers(cred, url):
    token = get_service_account_request_token(cred, url)
    headers = {'Authorization': f'bearer {token}'}
    return headers


def install_key(file: str):
    dir_name = os.path.dirname(default_key_path)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    copyfile(file, default_key_path)
