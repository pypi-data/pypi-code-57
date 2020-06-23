# coding: utf-8
import unittest
from mock import Mock, patch

from otrs_somconnexio.otrs_models.internet_article import InternetArticle


class InternetArticleTestCase(unittest.TestCase):

    @patch('otrs_somconnexio.otrs_models.abstract_article.Article')
    def test_call(self, MockArticle):
        service_type = 'fibra'
        eticom_contract = Mock(spec=['id'])
        eticom_contract.id = 123

        expected_article_arguments = {
            "Subject": "Sol·licitud fibra 123",
            "Body": "",
            "ContentType": "text/plain; charset=utf8"
        }

        InternetArticle(service_type, eticom_contract).call()

        MockArticle.assert_called_once_with(expected_article_arguments)
