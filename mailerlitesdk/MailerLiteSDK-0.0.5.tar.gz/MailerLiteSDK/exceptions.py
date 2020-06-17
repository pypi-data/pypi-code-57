from __future__ import unicode_literals


class MailerLiteApiError(Exception):

    def __init__(self, status_code, headers,  error=None):
        super(MailerLiteApiError, self).__init__()

        self.status_code = status_code
        self.headers = headers
        self.error = error

    def __str__(self):
        """str.
        :rtype: str
        """
        return '{0}: status_code={1}, error_response={2}, headers={3}'.format(
            self.__class__.__name__, self.status_code,  self.error, self.headers)