class SandboxException(Exception):
    def __init__(self, message, response):
        """
        :param message: the error message
        :type message: str
        :param response: the response
        :type response: requests.Response
        """
        Exception.__init__(self, message)
        self.__response = response

    @property
    def status_code(self):
        return self.__response.status_code

    @property
    def text(self):
        return self.__response.text
