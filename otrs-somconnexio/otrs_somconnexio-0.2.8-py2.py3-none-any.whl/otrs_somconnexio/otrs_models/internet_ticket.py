# coding: utf-8
import logging

from pyotrs.lib import Ticket

from otrs_somconnexio.client import OTRSClient
from otrs_somconnexio.otrs_models.internet_article import InternetArticle

from otrs_somconnexio.ticket_exceptions import CustomerIDMissing, CustomerUserMissing, CustomerMailMissing


log = logging.getLogger('otrs_somconnexio')


class InternetTicket():

    def __init__(self, econtract, otrs_configuration):
        self.eticom_contract = econtract
        self.otrs_configuration = otrs_configuration

    def create(self):
        """
        Creates an OTRSClient instance and sends the request to create the Ticket. Then, updates the EticomContract.
        """
        self.otrs_ticket = OTRSClient().create_otrs_process_ticket(
            self._build_ticket(),
            self._build_article(),
            self._build_dynamic_fields())

    @property
    def id(self):
        return self.otrs_ticket.id

    @property
    def number(self):
        return self.otrs_ticket.number

    def _build_ticket(self):
        return Ticket({
            "Title": "Sol·licitud {} {}".format(self.service_type(), self.eticom_contract.id),
            "Type": self._ticket_type(),
            "Queue": self._ticket_queue(),
            "State": self._ticket_state(),
            "Priority": self._ticket_priority(),
            "CustomerUser": self._customer_user(),
            "CustomerID": self._customer_id()
        })

    def _customer_id(self):
        if not self.eticom_contract.party:
            raise CustomerIDMissing(self.eticom_contract.id)
        return self._mail()

    def _customer_user(self):
        if not self.eticom_contract.party:
            raise CustomerUserMissing(self.eticom_contract.id)
        return self._mail()

    def _customer_lang(self):
        if not self.eticom_contract.party:
            return 'es_ES'
        return self.eticom_contract.party.lang.code

    def _build_article(self):
        """ Return a instance of OTRS Article to create a OTRS Ticket from Eticom Contract. """
        return InternetArticle(self.service_type(), self.eticom_contract).call()

    def _mail(self):
        mail = self.eticom_contract.party.get_contact_email()
        if mail:
            return mail.value
        raise CustomerMailMissing(self.eticom_contract.id)
