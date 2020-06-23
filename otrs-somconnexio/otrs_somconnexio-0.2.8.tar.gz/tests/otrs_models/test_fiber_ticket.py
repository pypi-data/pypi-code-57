# coding: utf-8
import unittest
from mock import Mock, patch

from otrs_somconnexio.otrs_models.fiber_ticket import FiberTicket
from otrs_somconnexio.ticket_exceptions import CustomerMailMissing, CustomerUserMissing


class FiberTicketTestCase(unittest.TestCase):

    @patch('otrs_somconnexio.otrs_models.internet_ticket.Ticket')
    def test_build_ticket(self, MockTicket):
        party = Mock(spec=[
            'get_contact_email',
            'get_identifier'
        ])
        email = Mock(spec=['value'])
        email.value = 'contact@mail.com'
        party.get_contact_email.return_value = email
        vat = Mock(spec=['code'])
        vat.code = 'VatCode'
        party.get_identifier.return_value = vat

        eticom_contract = Mock(spec=[
            'id',
            'party'
        ])
        eticom_contract.id = 123
        eticom_contract.party = party

        otrs_configuration = Mock(spec=[
            'fiber_ticket_type',
            'fiber_ticket_queue',
            'fiber_ticket_state',
            'fiber_ticket_priority',
            'fiber_process_id',
            'fiber_activity_id',
        ])
        otrs_configuration.fiber_ticket_type = 'fiber_ticket_type'
        otrs_configuration.fiber_ticket_queue = 'fiber_ticket_queue'
        otrs_configuration.fiber_ticket_state = 'fiber_ticket_state'
        otrs_configuration.fiber_ticket_proprity = 'fiber_ticket_priority'
        otrs_configuration.fiber_process_id = 'fiber_process_id'
        otrs_configuration.fiber_activity_id = 'fiber_activity_id'

        expected_ticket_arguments = {
            "Title": "Sol·licitud fiber {}".format(eticom_contract.id),
            "Type": otrs_configuration.fiber_ticket_type,
            "Queue": otrs_configuration.fiber_ticket_queue,
            "State": otrs_configuration.fiber_ticket_state,
            "Priority": otrs_configuration.fiber_ticket_proprity,
            "CustomerUser": 'contact@mail.com',
            "CustomerID": 'contact@mail.com'
        }

        FiberTicket(eticom_contract, otrs_configuration)._build_ticket()
        MockTicket.assert_called_with(expected_ticket_arguments)

    @patch('otrs_somconnexio.otrs_models.internet_ticket.Ticket')
    def test_build_ticket_raise_CustomerMailMissing_error(self, MockTicket):
        party = Mock(spec=[
            'get_contact_email'
        ])
        party.get_contact_email.return_value = None

        eticom_contract = Mock(spec=[
            'id',
            'party'
        ])
        eticom_contract.id = 123
        eticom_contract.party = party

        otrs_configuration = Mock(spec=[
            'fiber_ticket_type',
            'fiber_ticket_queue',
            'fiber_ticket_state',
            'fiber_ticket_priority',
            'fiber_process_id',
            'fiber_activity_id',
        ])
        otrs_configuration.fiber_ticket_type = 'fiber_ticket_type'
        otrs_configuration.fiber_ticket_queue = 'fiber_ticket_queue'
        otrs_configuration.fiber_ticket_state = 'fiber_ticket_state'
        otrs_configuration.fiber_ticket_proprity = 'fiber_ticket_priority'
        otrs_configuration.fiber_process_id = 'fiber_process_id'
        otrs_configuration.fiber_activity_id = 'fiber_activity_id'

        with self.assertRaises(CustomerMailMissing):
            FiberTicket(eticom_contract, otrs_configuration)._build_ticket()

    @patch('otrs_somconnexio.otrs_models.internet_ticket.Ticket')
    def test_build_ticket_raise_CustomerUserMissing_error(self, MockTicket):
        eticom_contract = Mock(spec=[
            'id',
            'party'
        ])
        eticom_contract.id = 123
        eticom_contract.party = None

        otrs_configuration = Mock(spec=[
            'fiber_ticket_type',
            'fiber_ticket_queue',
            'fiber_ticket_state',
            'fiber_ticket_priority',
            'fiber_process_id',
            'fiber_activity_id',
        ])
        otrs_configuration.fiber_ticket_type = 'fiber_ticket_type'
        otrs_configuration.fiber_ticket_queue = 'fiber_ticket_queue'
        otrs_configuration.fiber_ticket_state = 'fiber_ticket_state'
        otrs_configuration.fiber_ticket_proprity = 'fiber_ticket_priority'
        otrs_configuration.fiber_process_id = 'fiber_process_id'
        otrs_configuration.fiber_activity_id = 'fiber_activity_id'

        with self.assertRaises(CustomerUserMissing):
            FiberTicket(eticom_contract, otrs_configuration)._build_ticket()

    @patch('otrs_somconnexio.otrs_models.internet_ticket.InternetArticle')
    def test_build_article(self, MockInternetArticle):
        eticom_contract = Mock(spec=['id'])
        eticom_contract.id = 123

        otrs_configuration = Mock(spec=[])

        mock_mobile_article = MockInternetArticle.return_value

        FiberTicket(eticom_contract, otrs_configuration)._build_article()

        MockInternetArticle.assert_called_with('fiber', eticom_contract)
        mock_mobile_article.call.assert_called_once()

    @patch('otrs_somconnexio.otrs_models.fiber_ticket.FiberDynamicFields')
    def test_build_dynamic_fields(self, MockFiberDynamicFields):
        eticom_contract = Mock(spec=[])

        otrs_configuration = Mock(spec=[
            'fiber_process_id'
            'fiber_activity_id'
        ])
        otrs_configuration.fiber_process_id = 'fiber_process_id'
        otrs_configuration.fiber_activity_id = 'fiber_activity_id'

        mock_fiber_dynamic_fields = MockFiberDynamicFields.return_value

        FiberTicket(eticom_contract, otrs_configuration)._build_dynamic_fields()

        MockFiberDynamicFields.assert_called_with(
            eticom_contract,
            otrs_configuration.fiber_process_id,
            otrs_configuration.fiber_activity_id,
        )
        mock_fiber_dynamic_fields.all.assert_called_once()

    @patch('otrs_somconnexio.otrs_models.internet_ticket.OTRSClient')
    def test_create(self, MockOTRSClient):
        eticom_contract = Mock(spec=[
            'id',
            'party'
            'bank_iban_service',
            "internet_now",
            "internet_telecom_company",
            "internet_phone_now",
            "internet_street",
            "internet_city",
            "internet_zip",
            "internet_subdivision",
            "internet_country",
            "internet_delivery_street",
            "internet_delivery_city",
            "internet_delivery_zip",
            "internet_delivery_subdivision",
            "internet_delivery_country",
            "internet_vat_number",
            "internet_name",
            "internet_surname",
            "internet_lastname",
            "notes",
            "internet_speed",
            "coverage_availability",
            "change_address",
        ])
        eticom_contract.party = Mock(spec=[
            'get_identifier',
            'get_contact_email',
            'get_contact_phone',
            'first_name',
            'name',
            'party_type',
        ])
        eticom_contract.mobile_phone_number = "666666666"
        eticom_contract.mobile_option = "new"
        eticom_contract.mobile_min = "0"
        eticom_contract.bank_iban_service = "ES6621000418401234567891"

        otrs_configuration = Mock(spec=[
            'fiber_ticket_type',
            'fiber_ticket_queue',
            'fiber_ticket_state',
            'fiber_ticket_proprity',
            'fiber_process_id',
            'fiber_activity_id',
        ])

        mock_otrs_client = Mock(spec=['create_otrs_process_ticket'])
        mock_otrs_client.create_otrs_process_ticket.return_value.id = 123
        mock_otrs_client.create_otrs_process_ticket.return_value.number = '#123'
        MockOTRSClient.return_value = mock_otrs_client

        ticket = FiberTicket(eticom_contract, otrs_configuration)
        ticket.create()

        MockOTRSClient.assert_called_once_with()
        mock_otrs_client.create_otrs_process_ticket.assert_called_once()

        self.assertEqual(ticket.id, 123)
        self.assertEqual(ticket.number, '#123')
