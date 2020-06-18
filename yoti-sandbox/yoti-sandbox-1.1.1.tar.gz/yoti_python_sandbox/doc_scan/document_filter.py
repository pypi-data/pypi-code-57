from yoti_python_sdk.utils import YotiSerializable


class SandboxDocumentFilter(YotiSerializable):
    def __init__(self, country_codes, document_types):
        self.__country_codes = country_codes
        self.__document_types = document_types

    @property
    def country_codes(self):
        return self.__country_codes

    @property
    def document_types(self):
        return self.__document_types

    def to_json(self):
        return {
            "document_types": self.document_types,
            "country_codes": self.country_codes,
        }


class SandboxDocumentFilterBuilder(object):
    def __init__(self):
        self.__country_codes = []
        self.__document_types = []

    def with_document_type(self, document_type):
        self.__document_types.append(document_type)
        return self

    def with_country_code(self, country_code):
        self.__country_codes.append(country_code)
        return self

    def build(self):
        return SandboxDocumentFilter(self.__country_codes, self.__document_types)
