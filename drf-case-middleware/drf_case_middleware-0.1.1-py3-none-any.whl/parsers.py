import json

from django.conf import settings
from django.http.multipartparser import MultiPartParser as DjangoMultiPartParser, MultiPartParserError
from humps import camelize, decamelize
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FormParser, MultiPartParser, DataAndFiles, JSONParser


class CaseJSONParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)

        try:
            data = stream.read().decode(encoding)
            return decamelize(json.loads(data))
        except ValueError as err:
            raise ParseError(f'JSON parse error - {err}')


# Parser for form data
class CaseFormParser(FormParser):
    def parse(self, stream, media_type=None, parser_context=None):
        return decamelize(super().parse(stream, media_type, parser_context))


# Parser for multipart form data, which may include file data
class CaseMultiPartParser(MultiPartParser):
    media_type = 'multipart/form-data'

    def parse(self, stream, media_type=None, parser_context=None):
        '''
        Parses the incoming bytestream as a multipart encoded form,
        and returns a DataAndFiles object.
        `.data` will be a `QueryDict` containing all the form parameters.
        `.files` will be a `QueryDict` containing all the form files.
        '''
        parser_context = parser_context or {}
        request = parser_context['request']
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        meta = request.META.copy()
        meta['CONTENT_TYPE'] = media_type
        upload_handlers = request.upload_handlers

        try:
            parser = DjangoMultiPartParser(meta, stream, upload_handlers, encoding)
            data, files = parser.parse()

            return DataAndFiles(decamelize(data), decamelize(files), )
        except MultiPartParserError as err:
            raise ParseError(f'Multipart form parse error - {err}')
