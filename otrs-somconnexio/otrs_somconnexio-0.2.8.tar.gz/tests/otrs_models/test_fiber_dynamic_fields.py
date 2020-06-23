import unittest
from mock import Mock

from otrs_somconnexio.otrs_models.fiber_dynamic_fields import FiberDynamicFields
from otrs_somconnexio.ticket_exceptions import CustomerVatNumberMissing


def dynamic_fields_to_dct(dynamic_fields):
    """
    Convert the MobileDynamicFields object in a dict with the name of the dynamic
    field as key and the value as value.
    Only used to test the MobileDynamicFields object.
    """
    dct = {}
    for df in dynamic_fields:
        dct[df.name] = df.value
    return dct


class FiberDynamicFieldsTestCase(unittest.TestCase):
    def setUp(self):
        self.party = Mock(spec=[
            "first_name",
            "name",
            "get_identifier",
            "get_contact_phone",
            "get_contact_email",
            "party_type"
        ])
        self.eticom_contract = Mock(spec=[
            "id",
            "party",
            "bank_iban_service",
            "internet_now",
            "internet_telecom_company",
            "internet_phone",
            "internet_phone_now",
            "internet_phone_minutes",
            "internet_phone_number",
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

        self.adsl_otrs_process_id = "ADSLProcessID"
        self.adsl_otrs_activity_id = "ADSLActivityID"

    def test_process_id_field(self):
        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["ProcessManagementProcessID"], "ADSLProcessID")

    def test_activity_id_field(self):
        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["ProcessManagementActivityID"], "ADSLActivityID")

    def test_contract_id_field(self):
        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["IDContracte"], self.eticom_contract.id)

    def test_name_field_person_type(self):
        self.party.first_name = "First Name"
        self.party.party_type = "person"

        self.eticom_contract.party = self.party

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["nomSoci"], "First Name")

    def test_name_field_organization_type(self):
        self.party.name = "First Name"
        self.party.party_type = "organization"

        self.eticom_contract.party = self.party

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["nomSoci"], "First Name")

    def test_surname_field_organization_type(self):
        self.party.name = "Surname"
        self.party.party_type = "person"

        self.eticom_contract.party = self.party

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["cognom1"], "Surname")

    def test_vat_number_field(self):
        mock_vat = Mock(spec=["code"])
        mock_vat.code = "NIFCode"
        self.party.get_identifier.return_value = mock_vat

        self.eticom_contract.party = self.party

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["NIFNIESoci"], "NIFCode")

    def test_vat_number_field_raise_CustomerVatNumberMissing(self):
        self.party.get_identifier.return_value = None

        self.eticom_contract.party = self.party

        with self.assertRaises(CustomerVatNumberMissing):
            FiberDynamicFields(
                self.eticom_contract,
                self.adsl_otrs_process_id,
                self.adsl_otrs_activity_id
            ).all()

    def test_IBAN_field(self):
        self.eticom_contract.bank_iban_service = "ES6621000418401234567891"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["IBAN"], "ES6621000418401234567891")

    def test_contact_phone_field(self):
        mock_phone = Mock(spec=["value"])
        mock_phone.value = "666666666"
        self.party.get_contact_phone.return_value = mock_phone

        self.eticom_contract.party = self.party

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["telefonContacte"], "666666666")

    def test_contact_email_field(self):
        mock_email = Mock(spec=["value"])
        mock_email.value = "test@email.org"
        self.party.get_contact_email.return_value = mock_email

        self.eticom_contract.party = self.party

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["correuElectronic"], "test@email.org")

    def test_previous_service_adsl_field(self):
        self.eticom_contract.internet_now = "adsl"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["serveiPrevi"], "ADSL")

    def test_previous_service_fiber_field(self):
        self.eticom_contract.internet_now = "fibre"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["serveiPrevi"], "Fibra")

    def test_none_previous_provider_field(self):
        self.eticom_contract.internet_telecom_company = None

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["proveidorPrevi"], "None")

    def test_other_previous_provider_field(self):
        self.eticom_contract.internet_telecom_company = Mock(spec=[])
        self.eticom_contract.internet_telecom_company.name = "NewProvider"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["proveidorPrevi"], "Other")

    def test_mapped_previous_provider_field(self):
        self.eticom_contract.internet_telecom_company = Mock(spec=[])
        self.eticom_contract.internet_telecom_company.name = "Aire / Nubip"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["proveidorPrevi"], "Nubip")

    def test_landline_number_field(self):
        self.eticom_contract.internet_phone_now = "666666666"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["telefonFixVell"], "666666666")

    def test_address_field(self):
        self.eticom_contract.internet_street = "Street"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["direccioServei"], "Street")

    def test_city_field(self):
        self.eticom_contract.internet_city = "City"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["poblacioServei"], "City")

    def test_zip_field(self):
        self.eticom_contract.internet_zip = "000000"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["CPservei"], "000000")

    def test_subdivision_field(self):
        self.eticom_contract.internet_subdivision = Mock(spec=[])
        self.eticom_contract.internet_subdivision.name = "Subdivision"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["provinciaServei"], "Subdivision")

    def test_delivery_address_field(self):
        self.eticom_contract.internet_delivery_street = "Street"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["direccioEnviament"], "Street")

    def test_delivery_city_field(self):
        self.eticom_contract.internet_delivery_city = "City"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["poblacioEnviament"], "City")

    def test_delivery_zip_field(self):
        self.eticom_contract.internet_delivery_zip = "000000"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["CPenviament"], "000000")

    def test_delivery_subdivision_field(self):
        self.eticom_contract.internet_delivery_subdivision = Mock(spec=[])
        self.eticom_contract.internet_delivery_subdivision.name = "Subdivision"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["provinciaEnviament"], "Subdivision")

    def test_owner_vat_number_field(self):
        self.eticom_contract.internet_vat_number = "12345M"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["NIFNIEtitular"], "12345M")

    def test_owner_name_field(self):
        self.eticom_contract.internet_name = "Name"
        self.eticom_contract.internet_surname = "Surname"
        self.eticom_contract.internet_lastname = "Lastname"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["titular"], "Name Surname Lastname")

    def test_owner_surname_field(self):
        self.eticom_contract.internet_surname = "Surname"
        self.eticom_contract.internet_lastname = "Lastname"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["cognom1Titular"], "Surname Lastname")

    def test_notes_field(self):
        self.eticom_contract.notes = "Note"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["notes"], "Note")

    def test_adsl_coverage_field(self):
        self.eticom_contract.coverage_availability = Mock(spec=[
            "adsl",
            "mm_fiber",
            "vdf_fiber"
        ])
        self.eticom_contract.coverage_availability.adsl = "20"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["coberturaADSL"], "20")

    def test_mm_fiber_coverage_field(self):
        self.eticom_contract.coverage_availability = Mock(spec=[
            "adsl",
            "mm_fiber",
            "vdf_fiber"
        ])
        self.eticom_contract.coverage_availability.mm_fiber = "CoberturaMM"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["coberturaFibraMM"], "CoberturaMM")

    def test_vdf_fiber_coverage_field(self):
        self.eticom_contract.coverage_availability = Mock(spec=[
            "adsl",
            "mm_fiber",
            "vdf_fiber"
        ])
        self.eticom_contract.coverage_availability.vdf_fiber = "FibraVdf"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["coberturaFibraVdf"], "FibraVdf")

    def test_change_address_field(self):
        self.eticom_contract.change_address = True

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["canviUbicacioMateixTitular"], "yes")

    def test_change_address_field_doent_set(self):
        self.eticom_contract.change_address = False

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertNotIn("canviUbicacioMateixTitular", dynamic_fields_dct.keys())

# Service Dynamic Fields

    def test_speed_field(self):
        self.eticom_contract.internet_speed = "120MB"

        dynamic_fields = FiberDynamicFields(
            self.eticom_contract,
            self.adsl_otrs_process_id,
            self.adsl_otrs_activity_id
        ).all()

        dynamic_fields_dct = dynamic_fields_to_dct(dynamic_fields)
        self.assertEqual(dynamic_fields_dct["velocitatSollicitada"], "120MB")
