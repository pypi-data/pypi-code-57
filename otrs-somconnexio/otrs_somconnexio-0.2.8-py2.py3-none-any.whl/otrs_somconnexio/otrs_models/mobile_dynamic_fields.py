from pyotrs.lib import DynamicField
from otrs_somconnexio.otrs_models.telecom_company import TelecomCompany
from otrs_somconnexio.ticket_exceptions import CustomerMailMissing,\
    CustomerVatNumberMissing


class MobileDynamicFields():
    service_type = {
        "new": "altaNova",
        "portability": "portabilitat"
    }
    minutes = {
        "0": "0min",
        "100": "100min",
        "200": "200min",
        "unlimited": "unlim",
    }

    def __init__(self, eticom_contract, otrs_process_id, otrs_activity_id):
        self.eticom_contract = eticom_contract
        self.party = eticom_contract.party
        self.otrs_process_id = otrs_process_id
        self.otrs_activity_id = otrs_activity_id

    def all(self):
        dynamic_fields = [
            self._process_id(),
            self._activity_id(),
            self._first_name(),
            self._name(),
            self._vat_number(),
            self._iban(),
            self._line(),
            self._icc_sc(),
            self._icc_donor(),
            self._minutes(),
            self._data(),
            self._service_type(),
            self._mail(),
            self._phone(),
            self._df_previous_provider(),
        ]
        return [field for field in dynamic_fields if field is not None]

    def _process_id(self):
        return DynamicField("ProcessManagementProcessID", self.otrs_process_id)

    def _activity_id(self):
        return DynamicField("ProcessManagementActivityID", self.otrs_activity_id)

    def _first_name(self):
        return DynamicField("nomSoci", self.party.first_name)

    def _name(self):
        return DynamicField("cognom1", self.party.name)

    def _vat_number(self):
        vat = self.eticom_contract.party.get_identifier()
        if vat:
            return DynamicField(name="NIFNIESoci", value=vat.code)
        raise CustomerVatNumberMissing(self.eticom_contract.id)

    def _iban(self):
        return DynamicField("IBAN", self.eticom_contract.bank_iban_service)

    def _line(self):
        return DynamicField("liniaMobil", self.eticom_contract.mobile_phone_number)

    def _icc_sc(self):
        return DynamicField("ICCSC", self.eticom_contract.mobile_sc_icc)

    def _icc_donor(self):
        return DynamicField("ICCdonant", self.eticom_contract.mobile_icc_number)

    def _minutes(self):
        minutes = self.eticom_contract.mobile_min
        return DynamicField("minutsMobil", self.minutes[minutes])

    def _data(self):
        data = self.eticom_contract.mobile_internet
        if not data:
            data = self.eticom_contract.mobile_internet_unlimited
        return DynamicField("dadesMobil", data)

    def _service_type(self):
        type = self.eticom_contract.mobile_option
        return DynamicField("tipusServeiMobil", self.service_type[type])

    def _mail(self):
        mail = self.eticom_contract.party.get_contact_email()
        if mail:
            return DynamicField(name="correuElectronic", value=mail.value)
        raise CustomerMailMissing(self.eticom_contract.id)

    def _phone(self):
        """ Return the phone value. If the party does not have phone return 0. """
        phone = self.eticom_contract.party.get_contact_phone()
        if phone:
            return DynamicField(name="telefonContacte", value=phone.value)
        return None

    def _df_previous_provider(self):
        return DynamicField(
            name="operadorDonantMobil",
            value=str(TelecomCompany('mobile', self.eticom_contract.mobile_telecom_company))
        )
