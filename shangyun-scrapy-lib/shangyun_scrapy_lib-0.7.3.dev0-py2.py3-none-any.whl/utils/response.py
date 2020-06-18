from jsonpath_rw import Child
from jsonpath_rw.parser import JsonPathParser
from scrapy.http import TextResponse, Response


class JsonResponse(TextResponse):

    def __init__(self, *args, **kwargs):
        super(JsonResponse, self).__init__(*args, **kwargs)
        self._cached_json_path: Child = None

    @classmethod
    def copy_from(self, r: TextResponse):
        # _encoding = r._encoding if "_encoding" in r.__dict__ else "utf8"
        return JsonResponse(url=r.url, status=r.status, headers=r.headers, body=r.body, flags=r.flags,
                            request=r.request, encoding=r.encoding)

    @property
    def json_parser(self) -> Child:
        from jsonpath_rw import jsonpath, parse
        if self._cached_json_path:
            return self._cached_json_path
        self._cached_json_path = parse(self.text)
        return self._cached_json_path

    def find(self, *args, **kwargs):
        return self.json_parser.find(*args, **kwargs)
