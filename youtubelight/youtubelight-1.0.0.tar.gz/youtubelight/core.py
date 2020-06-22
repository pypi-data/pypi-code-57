class CoreMixin:

    api_url = 'https://www.googleapis.com/youtube/v3'

    def __init__(self, api_key):
        self.api_key = api_key

        if not self.api_key:
            raise Exception('API key not set')