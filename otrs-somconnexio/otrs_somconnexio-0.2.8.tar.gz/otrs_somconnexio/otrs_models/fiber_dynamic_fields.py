# coding: utf-8
from pyotrs.lib import DynamicField

from otrs_somconnexio.otrs_models.internet_dynamic_fields import InternetDynamicFields


class FiberDynamicFields(InternetDynamicFields):

    def _build_specific_dynamic_fields(self):
        """ Return list of OTRS DynamicFields to create a OTRS Process Ticket from Eticom Contract.
        Return only the specifics fields of Fiber Ticket. """
        return [
            self._df_speed(),
        ]

    def _df_speed(self):
        return DynamicField(
            name="velocitatSollicitada",
            value=self.eticom_contract.internet_speed)
