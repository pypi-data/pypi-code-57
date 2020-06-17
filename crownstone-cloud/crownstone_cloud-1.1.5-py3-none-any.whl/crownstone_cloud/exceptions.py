"""Exceptions for crownstone lib connection lib"""


AuthError = {
    'LOGIN_FAILED': 'Wrong email or password provided',
    'USERNAME_EMAIL_REQUIRED': 'Email or password not provided',
    'LOGIN_FAILED_EMAIL_NOT_VERIFIED': 'Email has not been verified, please do that first',
}


class CrownstoneAuthenticationError(Exception):
    """Raised when authentication with API ended in error"""
    type = None
    message = None

    def __init__(self, type, message=None):
        self.type = type
        self.message = message


class CrownstoneUnknownError(Exception):
    """Raised when the error is not known / no data"""
