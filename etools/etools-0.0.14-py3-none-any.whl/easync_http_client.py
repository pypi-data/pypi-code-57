from etools.async_http_client import AsyncHttpClient
from etools.singleton_meta import SingletonMeta
from etools.http_common import extract_result


class EAsyncHttpClient(AsyncHttpClient, metaclass=SingletonMeta):

    async def post(self, url, data, timeout=5, timeout_retry=3, clear_none=True, **kwargs):
        response = await super(EAsyncHttpClient, self).post(
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


easync_http_client = EAsyncHttpClient()
