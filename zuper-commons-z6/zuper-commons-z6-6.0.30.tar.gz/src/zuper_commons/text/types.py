from typing import NewType

__all__ = ['MarkdownStr', 'MD5Hash', 'SHA1Hash', 'HTMLString', 'XMLString']

MarkdownStr = str

MD5Hash = NewType('MD5Hash', str)

SHA1Hash = NewType('SHA1Hash', str)
HTMLString = str
XMLString = str
