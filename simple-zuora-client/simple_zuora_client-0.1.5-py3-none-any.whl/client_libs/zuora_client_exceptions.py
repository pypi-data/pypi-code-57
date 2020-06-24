class ZuoraExportQueryFormatError(Exception):
    """"Export query format error"""


class ZuoraExportQueryResultError(Exception):
    """"Export query response error"""

    def __init__(self, response):
        super().__init__(
            f'Error posting batch export query, error in the posted data, status is {response.status_code}'
            + f'\n{response.text()}')
        self.status_code = response.status_code
        # self.json_response = response.json()
        self.text_response = response.text


class ZuoraErrorResponseException(Exception):
    """"Error response form Zuora"""

    def __init__(self, response):
        super().__init__(f'Error getting data, status is {response.status_code}')
        self.status_code = response.status_code
        # self.json_response = response.json()
        self.text_response = response.text


class ZuoraErrorEmptyPostBody(Exception):
    """If you are trying to post nothing to the API"""

    def __init__(self):
        super().__init__('Empty data body to post')


class ZuoraErrorHeaderWrongDataType(Exception):
    """You are trying to put a crappy header"""

    def __init__(self):
        super().__init__('Wrong data type of the new header. It has to be a dict.')
