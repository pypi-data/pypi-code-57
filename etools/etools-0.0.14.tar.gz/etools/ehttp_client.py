from etools.http_client import HttpClient
from etools.http_common import extract_result


class EHttpClient(HttpClient):

    def post(self, url, data, timeout=5, timeout_retry=3, clear_none=True, **kwargs):
        response = super(EHttpClient, self).post(
                url, data, timeout=timeout,
                timeout_retry=timeout_retry, decode_json=True, **kwargs)
        if response is None:
            return response
        result = extract_result(response, clear_none)
        if result is None:
            self.logger.error("post [%s], data[%s] kwargs[%s] error, response [%s]",
                              url, data, kwargs, response)
            return None
        return result


ehttp_client = EHttpClient()
