class MultipleObjectsFound(Exception):

    def __init__(self):
        Exception.__init__(self)
        self.message = 'More than one records returned'


class NotFound(Exception):

    def __init__(self):
        Exception.__init__(self)
        self.message = 'Record not found'


class WrongParameters(Exception):

    def __init__(self):
        Exception.__init__(self)
        self.message = 'Wrong parameters inserted'


class ApiError(Exception):
    """Error while connecting to the API."""
