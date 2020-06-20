class APIError(Exception):
    code = -1
    message = 'Unknown error'

    def __init__(self, message=None, details=None, data={}, response=None):
        self.message = message or self.message
        self.details = details
        self.data = data or {}
        self.response = response

    def __str__(self):
        message = self.message

        if self.details:
            message = f'{message}: {self.details}'

        if self.code:
            message = f'{self.code} {message}'

        return message

# Specific exception classes


class BadRequestException(APIError):
    code = 400
    message = (
        'The request was unacceptable, often due '
        'to missing a required parameter')


class UnauthorizedException(APIError):
    code = 401
    message = 'No valid API key provided'


class FailedException(APIError):
    code = 402
    message = 'The requested resource doesn\'t exist'


class NotFoundException(APIError):
    code = 404
    message = 'The parameters were valid but the request failed'


class MethodNotAllowedException(APIError):
    code = 405
    message = 'Method not allowed'


class ConflictException(APIError):
    code = 409
    message = 'The request conflicts with another request'


class TooManyRequestsException(APIError):
    code = 429
    message = 'Too many requests hit the API too quickly'


class InternalServerException(APIError):
    code = 500
    message = 'Something went wrong on services end'


# Mapping of API response codes to exception classes
API_RETURN_CODES = {
    -1: APIError,
    400: BadRequestException,
    401: UnauthorizedException,
    402: FailedException,
    404: NotFoundException,
    405: MethodNotAllowedException,
    409: ConflictException,
    429: TooManyRequestsException,
    500: InternalServerException,
}


def handle_error_response(resp):
    """Take a HTTP response object and translate it into an Exception
    instance."""
    response_json = resp.json()

    message = response_json.get('message')
    details = response_json.get('details')
    code = response_json.get('code', -1)
    data = response_json.get('data', {})

    # Build the appropriate exception class with as much data as we can pull
    # from the API response and raise it.
    raise API_RETURN_CODES[code](
        message=message, details=details, data=data, response=resp)
