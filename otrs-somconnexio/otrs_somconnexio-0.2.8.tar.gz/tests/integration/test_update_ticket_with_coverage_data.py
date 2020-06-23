# coding: utf-8
import os
import unittest
from mock import Mock, patch
from pyotrs.lib import DynamicField

from otrs_somconnexio.otrs_models.coverage_ticket import CoverageTicket

from otrs_somconnexio.services.update_process_ticket_with_coverage_tickets_info_service import \
    UpdateProcessTicketWithCoverageTicketsInfoService

USER = 'user'
PASSW = 'passw'
URL = 'https://otrs-url.coop/'


class UpdateTicketWithCoverageTicketInfoTestCase(unittest.TestCase):

    @patch.dict(os.environ, {
        'OTRS_USER': USER,
        'OTRS_PASSW': PASSW,
        'OTRS_URL': URL
    })
    @patch('otrs_somconnexio.client.Client', return_value=Mock(
        spec=['session_create', 'ticket_update']
    ))
    @patch('otrs_somconnexio.otrs_models.abstract_article.Article')
    def test_run(self, MockArticle, MockClient):
        ticket_id = 123

        ticket = Mock(spec=['response'])
        ticket.response = Mock(spec=['dynamic_field_get'])

        def get_df_side_effect(name):
            return DynamicField(name, 'foo')

        ticket.response.dynamic_field_get.side_effect = get_df_side_effect
        coverage_ticket = CoverageTicket(ticket)

        coverage_article = object()
        MockArticle.return_value = coverage_article

        UpdateProcessTicketWithCoverageTicketsInfoService(ticket_id, [coverage_ticket]).run()

        MockClient.return_value.ticket_update.assert_called_with(ticket_id, coverage_article)
        MockArticle.assert_called_with({
            "Subject": "Sol·licitud cobertura",
            "Body": "tipusVia: foo\nnomVia: foo\nnumero: foo\nbloc: foo\nportal: foo\npis: foo\nescala: foo\nporta: foo\npoblacioServei: foo\nprovinciaServei: foo\nCPservei: foo\naltresCobertura: foo\ncoberturaADSL: foo\ncoberturaFibraMM: foo\ncoberturaFibraVdf: foo\nIDhogar: foo\n",  # noqa
            "ContentType": "text/plain; charset=utf8"
        })
