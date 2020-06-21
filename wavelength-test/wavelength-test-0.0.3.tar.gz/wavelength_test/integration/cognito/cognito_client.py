# -*- coding: utf-8 -*-
"""
    CognitoUserClient
"""
from contextlib import suppress
import json
import boto3

DEFAULT_ENTITLEMENTS = ['*']


class CognitoUserClient:
    """
        Standard client to automate user creation/authorization in Cognito
    """

    def __init__(self, region, user_pool_id, app_client_id):
        """
        Cognito values are injected from lambda_util.py from SSM
        :param region:
        :param user_pool_id:
        :param app_client_id:
        """
        self.region = region
        self.user_pool_id = user_pool_id
        self.client_id = app_client_id
        self.client = boto3.client('cognito-idp', region_name=self.region)

    def create_user(self, user_data):
        """
            Creates a new user with NEW_PASSWORD_REQUIRED status in the specified user pool.
            If the user exists already, except is triggered and the user is logged in to get JWT
            :param user_data: dict containing user information
            :return: a dictionary containing tokens and Cognito user data
        """

        with suppress(self.client.exceptions.UsernameExistsException):
            attributes = self._get_attributes(user_data)
            attrib_set = {attr['Name']: attr['Value'] for attr in attributes}
            user = None
            try:
                user = self.client.admin_get_user(
                    UserPoolId=self.user_pool_id,
                    Username=user_data['email']
                )
            except self.client.exceptions.UserNotFoundException:
                pass
            if user:
                user_attr_set = {attr['Name']: attr['Value'] for attr in user['UserAttributes']}
                user_attr_set.pop('sub')
                if user_attr_set != attrib_set:
                    self.client.admin_update_user_attributes(
                        UserPoolId=self.user_pool_id,
                        Username=user_data['email'],
                        UserAttributes=attributes
                    )
                return self.sign_in_user(user_data['email'], user_data['password'])

            user = self.client.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=user_data['email'],
                TemporaryPassword=user_data['password'] + 'temp',
                UserAttributes=attributes
            )
            return self._authorize_new_user(user['User']['Username'], user_data['password'])

    @staticmethod
    def _get_attributes(user_data):
        return [
            {
                'Name': 'email_verified',
                'Value': 'true'
            },
            {
                'Name': 'locale',
                'Value': user_data['locale']
            },
            {
                'Name': 'given_name',
                'Value': user_data['first_name']
            },
            {
                'Name': 'family_name',
                'Value': user_data['last_name']
            },
            {
                'Name': 'email',
                'Value': user_data['email']
            },
            {
                'Name': "custom:eids",
                'Value': json.dumps({'eids': user_data['entitlements']})
            }
        ]

    def _authorize_new_user(self, user_name, password):
        """
            Automates the authorization of a new user with a password challenge/answer and gets their tokens
            :param user_data: {} containing user data
            :return: {} containing Cognito user info and tokens
        """

        auth_params = {
            'USERNAME': user_name,
            'PASSWORD': password + 'temp'
        }

        challenges = {
            'USERNAME': user_name,
            'NEW_PASSWORD': password
        }

        # do a first time login to obtain the challenge session
        response = self.client.initiate_auth(AuthFlow='USER_PASSWORD_AUTH', AuthParameters=auth_params,
                                             ClientId=self.client_id)

        session = response['Session']

        # change user password to automate the status transitioning to CONFIRMED
        auth_response = self.client.respond_to_auth_challenge(ClientId=self.client_id,
                                                              ChallengeName='NEW_PASSWORD_REQUIRED',
                                                              Session=session, ChallengeResponses=challenges)

        # no need to return user information, its in the IdToken
        return auth_response

    def sign_in_user(self, username, password):
        """
        Signs in existing user with username(email) and password and get new JWTs
        :param username:
        :param password:
        :return: {} containing JWT tokens
        """

        return self.client.admin_initiate_auth(
            UserPoolId=self.user_pool_id,
            ClientId=self.client_id,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )

    def sign_out_user(self, username):
        """
        Signs out users from all devices, as an administrator.
        :param username: email address of user
        :return: {}
        """

        return self.client.admin_user_global_sign_out(
            UserPoolId=self.user_pool_id,
            Username=username
        )

    def delete_user(self, email):
        """
            Deletes a user as an administrator. Works on any user.
            :param email: String
            :return: {} containing HTTPStatusCode
        """

        try:
            return self.client.admin_delete_user(
                UserPoolId=self.user_pool_id,
                Username=email
            )
        except self.client.exceptions.UserNotFoundException:
            raise Exception('An account with the given email does not exist.')

    def get_user(self, email):
        """
            Gets the specified user by user name in a user pool as an administrator. Works on any user.
            :param email: String
            :return: {} containing all user data
        """

        try:
            return self.client.admin_get_user(
                Username=email,
                UserPoolId=self.user_pool_id
            )
        except self.client.exceptions.UserNotFoundException:
            raise Exception('An account with the given email does not exist.')
