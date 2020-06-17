from collections import UserList
from mdocument.document_dict import DocumentDict


class DocumentArray(UserList):

    def __getitem__(self, item):
        result = super().__getitem__(item)
        if isinstance(result, dict):
            return DocumentDict(result)
        return result
