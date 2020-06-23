# coding: utf-8
from otrs_somconnexio.otrs_models.internet_ticket import InternetTicket
from otrs_somconnexio.otrs_models.adsl_dynamic_fields import ADSLDynamicFields


class ADSLTicket(InternetTicket):

    def service_type(self):
        return 'adsl'

    def _build_dynamic_fields(self):
        return ADSLDynamicFields(
            self.eticom_contract,
            self.otrs_configuration.adsl_process_id,
            self.otrs_configuration.adsl_activity_id
        ).all()

    def _ticket_type(self):
        return self.otrs_configuration.adsl_ticket_type

    def _ticket_queue(self):
        return self.otrs_configuration.adsl_ticket_queue

    def _ticket_state(self):
        return self.otrs_configuration.adsl_ticket_state

    def _ticket_priority(self):
        return self.otrs_configuration.adsl_ticket_proprity

    def _ticket_activity_id(self):
        return self.otrs_configuration.adsl_activity_id

    def _ticket_process_id(self):
        return self.otrs_configuration.adsl_process_id
