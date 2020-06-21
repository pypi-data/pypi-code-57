from wavelength_test.integration.cognito.cognito_client import (CognitoUserClient,
                                                         DEFAULT_ENTITLEMENTS)


def get_cognito_id_token(service_name, region, ssm_client):
    """
    Creates a new Cognito user and retrieves their JWT 'IdToken'
    :return: JWT 'IdToken'
    """
    pool_id_response = ssm_client.get_parameter(Name='/cognito/wavelength/user_pool_id')
    app_id_response = ssm_client.get_parameter(Name='/cognito/wavelength/web_client_id')
    pool_id = pool_id_response['Parameter']['Value']
    app_id = app_id_response['Parameter']['Value']

    cognito_client = CognitoUserClient(region, pool_id, app_id)
    cognito_user_data = {
        'email': f'test_{service_name}@yopmail.com',
        'first_name': f'first_name_{service_name}',
        'last_name': f'last_name_{service_name}',
        'password': 'Password1*',
        'locale': 'en_US',
        'entitlements': DEFAULT_ENTITLEMENTS
    }
    cognito_user = cognito_client.create_user(cognito_user_data)
    cognito_token = cognito_user['AuthenticationResult']['IdToken']
    return cognito_token


def get_api_key(service_name, ssm_client, gateway_client):
    """
    Get the apikeyID according to service name
    :param service_name:
    :return:
    """
    response = ssm_client.get_parameter(
        Name=f'/apigateway/{service_name}/apikeyID/default'
    )
    logical_id = response['Parameter']['Value']
    response = gateway_client.get_api_key(
        apiKey=logical_id,
        includeValue=True
    )
    return response['value']
