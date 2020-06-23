# coding: utf-8
import os
import unittest
from mock import Mock, patch

from otrs_somconnexio.ticket_exceptions import ServiceTypeNotAllowedError
from otrs_somconnexio.otrs_models.adsl_ticket import ADSLTicket
from otrs_somconnexio.otrs_models.fiber_ticket import FiberTicket
from otrs_somconnexio.otrs_models.mobile_ticket import MobileTicket

from otrs_somconnexio.otrs_models.ticket_factory import TicketFactory

USER = 'user'
PASSW = 'passw'
URL = 'https://otrs-url.coop/'


@patch.dict(os.environ, {
    'OTRS_USER': USER,
    'OTRS_PASSW': PASSW,
    'OTRS_URL': URL
})
class TicketFactoryTestCase(unittest.TestCase):

    def setUp(self):
        self.eticom_contract = Mock(spec=['id'])
        self.otrs_configuration = Mock(spec=[
            'fiber_ticket_type',
            'fiber_ticket_queue',
            'fiber_ticket_state',
            'fiber_ticket_priority',
            'fiber_process_id',
            'fiber_activity_id',
            'adsl_ticket_type',
            'adsl_ticket_queue',
            'adsl_ticket_state',
            'adsl_ticket_priority',
            'adsl_process_id',
            'adsl_activity_id',
            'mobile_ticket_type',
            'mobile_ticket_queue',
            'mobile_ticket_state',
            'mobile_ticket_priority',
            'mobile_process_id',
            'mobile_activity_id',
        ])
        self.otrs_configuration.mobile_ticket_type = 'mobile_ticket_type'
        self.otrs_configuration.mobile_ticket_queue = 'mobile_ticket_queue'
        self.otrs_configuration.mobile_ticket_state = 'mobile_ticket_state'
        self.otrs_configuration.mobile_ticket_priority = 'mobile_ticket_priority'
        self.otrs_configuration.mobile_process_id = 'mobile_process_id'
        self.otrs_configuration.mobile_activity_id = 'mobile_activity_id'
        self.otrs_configuration.adsl_ticket_type = 'adsl_ticket_type'
        self.otrs_configuration.adsl_ticket_queue = 'adsl_ticket_queue'
        self.otrs_configuration.adsl_ticket_state = 'adsl_ticket_state'
        self.otrs_configuration.adsl_ticket_proprity = 'adsl_ticket_priority'
        self.otrs_configuration.adsl_process_id = 'adsl_process_id'
        self.otrs_configuration.adsl_activity_id = 'adsl_activity_id'
        self.otrs_configuration.fiber_ticket_type = 'fiber_ticket_type'
        self.otrs_configuration.fiber_ticket_queue = 'fiber_ticket_queue'
        self.otrs_configuration.fiber_ticket_state = 'fiber_ticket_state'
        self.otrs_configuration.fiber_ticket_proprity = 'fiber_ticket_priority'
        self.otrs_configuration.fiber_process_id = 'fiber_process_id'
        self.otrs_configuration.fiber_activity_id = 'fiber_activity_id'

    def test_build_raise_service_type_not_allowed_error(self):
        ticket_factory = TicketFactory(
            'no allowed_type',
            self.eticom_contract,
            self.otrs_configuration
        )
        with self.assertRaises(ServiceTypeNotAllowedError):
            ticket_factory.build()

    @patch('otrs_somconnexio.client.Client')
    def test_build_mobile_ticket(self, MockClient):
        self.eticom_contract = Mock(spec=[
            'id',
            'party',
            'bank_iban_service',
            'mobile_phone_number',
            'mobile_sc_icc',
            'mobile_icc_number',
            'mobile_min',
            'mobile_internet',
            'mobile_option',
            'mobile_telecom_company',
        ])
        self.eticom_contract.mobile_min = '0'
        self.eticom_contract.mobile_option = 'new'

        service_type = 'mobile'
        ticket = TicketFactory(
            service_type,
            self.eticom_contract,
            self.otrs_configuration
        ).build()
        self.assertIsInstance(ticket, MobileTicket)

    @patch('otrs_somconnexio.client.Client')
    def test_build_adsl_ticket(self, MockClient):
        self.eticom_contract = Mock(spec=[
            'id',
            'party',
            'bank_iban_service',
            'internet_now',
            'internet_telecom_company',
            'internet_phone',
            'internet_phone_now',
            'internet_phone_minutes',
            'internet_phone_number',
            'internet_street',
            'internet_city',
            'internet_zip',
            'internet_subdivision',
            'internet_country',
            'internet_delivery_street',
            'internet_delivery_city',
            'internet_delivery_zip',
            'internet_delivery_subdivision',
            'internet_delivery_country',
            'internet_vat_number',
            'internet_name',
            'internet_surname',
            'internet_lastname',
            'notes',
            'coverage_availability',
            'change_address',
        ])
        service_type = 'adsl'
        ticket = TicketFactory(
            service_type,
            self.eticom_contract,
            self.otrs_configuration
        ).build()
        self.assertIsInstance(ticket, ADSLTicket)

    @patch('otrs_somconnexio.client.Client')
    def test_build_fibre_ticket(self, MockClient):
        self.eticom_contract = Mock(spec=[
            'id',
            'party',
            'bank_iban_service',
            'internet_now',
            'internet_telecom_company',
            'internet_speed',
            'internet_phone_now',
            'internet_street',
            'internet_city',
            'internet_zip',
            'internet_subdivision',
            'internet_country',
            'internet_delivery_street',
            'internet_delivery_city',
            'internet_delivery_zip',
            'internet_delivery_subdivision',
            'internet_delivery_country',
            'internet_vat_number',
            'internet_name',
            'internet_surname',
            'internet_lastname',
            'notes',
            'coverage_availability',
            'change_address',
        ])
        service_type = 'fiber'
        ticket = TicketFactory(
            service_type,
            self.eticom_contract,
            self.otrs_configuration
        ).build()
        self.assertIsInstance(ticket, FiberTicket)
