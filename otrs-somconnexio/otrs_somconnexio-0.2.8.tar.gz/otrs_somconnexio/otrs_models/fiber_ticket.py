# coding: utf-8
from otrs_somconnexio.otrs_models.internet_ticket import InternetTicket
from otrs_somconnexio.otrs_models.fiber_dynamic_fields import FiberDynamicFields


class FiberTicket(InternetTicket):

    def service_type(self):
        return 'fiber'

    def _build_dynamic_fields(self):
        return FiberDynamicFields(
            self.eticom_contract,
            self.otrs_configuration.fiber_process_id,
            self.otrs_configuration.fiber_activity_id
        ).all()

    def _ticket_type(self):
        return self.otrs_configuration.fiber_ticket_type

    def _ticket_queue(self):
        return self.otrs_configuration.fiber_ticket_queue

    def _ticket_state(self):
        return self.otrs_configuration.fiber_ticket_state

    def _ticket_priority(self):
        return self.otrs_configuration.fiber_ticket_proprity

    def _ticket_activity_id(self):
        return self.otrs_configuration.fiber_activity_id

    def _ticket_process_id(self):
        return self.otrs_configuration.fiber_process_id
