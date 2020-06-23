# coding: utf-8
from pyotrs.lib import Article


class AbstractArticle:

    subject = ""
    body = ""

    def call(self):
        return Article({
            "Subject": self.subject,
            "Body": self.body,
            "ContentType": "text/plain; charset=utf8"
        })
