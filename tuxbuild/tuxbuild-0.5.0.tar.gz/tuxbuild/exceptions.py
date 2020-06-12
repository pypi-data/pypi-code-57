# -*- coding: utf-8 -*-


class TuxbuildError(Exception):
    """ Base class for all Tuxbuild exceptions """

    error_help = ""
    error_type = ""


class CantGetConfiguration(TuxbuildError):
    error_help = "Problem reading configuration"
    error_type = "configuration"


class InvalidConfiguration(TuxbuildError):
    error_help = "Invalid configuration"
    error_type = "configuration"


class TokenNotFound(TuxbuildError):
    error_help = "No token provided"
    error_type = "Configuration"


class URLNotFound(TuxbuildError):
    error_help = "A tuxbuild URL cannot be found"
    error_type = "Configuration"


class BadRequest(TuxbuildError):
    error_help = "A tuxbuild API call failed"
    error_type = "API"


class InvalidToken(TuxbuildError):
    error_help = "The provided token was not accepted by the server"
    error_type = "API"


class Timeout(TuxbuildError):
    error_help = "A tuxbuild API call failed"
    error_type = "API"
