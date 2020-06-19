# -*- coding: utf-8 -*-
from crabpy.gateway.exception import GatewayRuntimeException

from oe_geoutils.validation.validators_location_elements import LocationElementSchemaNode
from tests import crab_gateway_mock, capakey_gateway_mock, list_kadastrale_afdelingen

try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch  # pragma: no cover
import colander
from pyramid import testing
import unittest


class LocatieAdresSchemaNodeLocatieElementAdresTests(unittest.TestCase):
    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.crab_gateway = Mock(return_value=crab_gateway_mock)
        self.request.capakey_gateway = Mock(return_value=capakey_gateway_mock)

        adressen_schema = LocationElementSchemaNode()

        self.schema = adressen_schema.bind(
            request=self.request
        )
        self.data = {
            "id": 1,
            "type": "https://id.erfgoed.net/vocab/ontology#LocatieElementAdres",
            "land": "BE",
            "provincie": {
                "naam": "West-Vlaanderen",
                "niscode": 30000
            },
            "postcode": "8300",
            "gemeente": {
                "naam": "Knokke-Heist",
                "id": 191
            },
            "straat": "Nieuwstraat",
            "straat_id": 48086,
            "huisnummer": "6",
            "subadres": "1",
        }

    def test_adres_None(self):
        with self.assertRaises(colander.Invalid) as inv:
            self.data['gemeente'] = {
                "naam": None,
                "id": None
            }
            self.schema.deserialize(self.data)
        self.assertEqual('geen correcte gemeente_id gevonden voor de gemeente None',
                         inv.exception.asdict()[''])

    def test_adres_None_2(self):
        with self.assertRaises(colander.Invalid) as inv:
            self.schema.deserialize(
                {
                    "type": "https://id.erfgoed.net/vocab/ontology#LocatieElementAdres"
                }
            )
        self.assertEqual('geen correcte gemeente_id gevonden voor de gemeente None',
                         inv.exception.asdict()[''])

    def test_adres_gemeente_id_from_gemeente_val(self):
        self.data['gemeente']['id'] = None
        res = self.schema.deserialize(self.data)
        self.assertEqual(191, res["gemeente"]["id"])

    def test_adres_validatie(self):
        res = self.schema.deserialize(self.data)
        self.assertEqual("Nieuwstraat", res['straat'])
        self.assertEqual("6", res['huisnummer'])
        self.assertEqual("1", res['subadres'])
        self.assertEqual(270059, res['huisnummer_id'])
        self.assertEqual(1441952, res['subadres_id'])
        self.assertEqual(31043, res["gemeente"]["niscode"])

    def test_adres_validatie_huisnummer_start_with_number(self):
        self.data['huisnummer'] = 'ab12'
        with self.assertRaises(colander.Invalid) as inv:
            self.schema.deserialize(self.data)
        self.assertEqual('Het huisnummer moet beginnen met een cijfer.',
                         inv.exception.msg)

    def test_adres_validatie_subadres_alphanumeric(self):
        self.data['subadres'] = '68#'
        with self.assertRaises(colander.Invalid) as inv:
            self.schema.deserialize(self.data)
        self.assertEqual('Het subadres kan enkel alfanumerieke tekens bevatten.',
                         inv.exception.msg)

    def test_adres_validatie_huisnummer_id_wrong(self):
        self.data['huisnummer_id'] = '1234123412341234'
        res = self.schema.deserialize(self.data)
        self.assertEqual(1234123412341234, res['huisnummer_id'])
        self.assertEqual('6', res['huisnummer'])

    def test_adres_validatie_subadres_id_wrong(self):
        self.data['subadres_id'] = '1234123412341234'
        res = self.schema.deserialize(self.data)
        self.assertEqual(1234123412341234, res['subadres_id'])
        self.assertEqual('1', res['subadres'])

    def test_adres_geen_crab(self):
        self.data['straat_id'] = None
        self.data['huisnummer_id'] = None
        self.data['subadres_id'] = None
        res = self.schema.deserialize(self.data)
        self.assertEqual(48086, res['straat_id'])
        self.assertEqual(270059, res['huisnummer_id'])
        self.assertEqual(1441952, res['subadres_id'])

    def test_adres_validatie_non_be(self):
        self.data['land'] = 'DE'
        res = self.schema.deserialize(self.data)
        self.assertIsNone(res["gemeente"]["id"])
        self.assertIsNone(res["huisnummer_id"])
        self.assertIsNone(res["straat_id"])
        self.assertIsNone(res["subadres_id"])

    def test_straat_niet_in_gemeente(self):
        self.data['gemeente'] = {
            "naam": "Lier",
            "id": None
        }
        with self.assertRaises(colander.Invalid) as inv:
            self.schema.deserialize(self.data)
        self.assertEqual('de straat Nieuwstraat met id 48086 ligt niet in gemeente Lier',
                         inv.exception.asdict()[''])

    def test_postcode(self):
        self.data['postcode'] = '1025'
        with self.assertRaises(colander.Invalid) as inv:
            self.schema.deserialize(self.data)
        self.assertEqual(
            "postcode 1025 is niet correct voor dit adres, mogelijke postcode is 8300",
            inv.exception.asdict()['']
        )

    def test_ongeldige_gemeente_id(self):
        self.data['gemeente']['id'] = 191023
        with self.assertRaises(colander.Invalid) as inv:
            self.schema.deserialize(self.data)
        self.assertEqual('ongeldig gemeente_id 191023',
                         inv.exception.asdict()[''])

    def test_ongeldige_gemeente(self):
        self.data['gemeente'] = {
            "naam": "Test",
            "id": None
        }
        with self.assertRaises(colander.Invalid) as inv:
            self.schema.deserialize(self.data)
        self.assertEqual('geen correcte gemeente_id gevonden voor de gemeente Test',
                         inv.exception.asdict()[''])

    def test_ongeldige_straat_id(self):
        self.data['straat_id'] = 480865567624
        with self.assertRaises(colander.Invalid) as inv:
            self.schema.deserialize(self.data)
        self.assertEqual('ongeldig straat_id',
                         inv.exception.asdict()[''])

    def test_buitenland(self):
        res = self.schema.deserialize(
            {
                "land": "DE",
                "type": "https://id.erfgoed.net/vocab/ontology#LocatieElementAdres",
                "gemeente": {
                    "naam": u"Köln",
                }
            }
        )
        self.assertEqual(u"Köln", res['gemeente']['naam'])

    def test_ongeldig_land(self):
        with self.assertRaises(colander.Invalid) as inv:
            self.schema.deserialize(
                {
                    "land": "XX",
                    "type": "https://id.erfgoed.net/vocab/ontology#LocatieElementAdres",
                    "gemeente": {
                        "naam": u"Köln",
                    }
                }
            )
        self.assertEqual("ongeldige landcode XX, dit is geen ISO 3166 code",
                         inv.exception.asdict()[''])

    def test_location_element_schema_handles_missing(self):
        class ParentSchema(colander.MappingSchema):
            child_schema = LocationElementSchemaNode(missing=colander.required)
            some_node = colander.SchemaNode(colander.String(), missing='some value')

        json_data = {'some_node': 'some other value'}
        schema = ParentSchema()
        with self.assertRaises(colander.Invalid) as ex:
            schema.deserialize(json_data)

    def test_location_element_schema_handles_missing_default(self):
        class ParentSchema(colander.MappingSchema):
            child_schema = LocationElementSchemaNode(missing=None)
            some_node = colander.SchemaNode(colander.String(), missing='some value')

        json_data = {'some_node': 'some other value'}
        schema = ParentSchema()
        deserialized = schema.deserialize(json_data)
        self.assertIsNotNone(deserialized)
        self.assertIn('some_node', deserialized)
        self.assertIn('child_schema', deserialized)
        self.assertEqual(deserialized['child_schema'], None)

    def test_missing_provincies(self):
        del self.data['provincie']
        res = self.schema.deserialize(self.data)
        self.assertEqual(30000, res["provincie"]["niscode"])
        self.assertEqual("West-Vlaanderen", res["provincie"]["naam"])

    def test_adres_missing_provincie_gemeente_id(self):
        self.data['provincie'] = {}
        del self.data['gemeente']['id']
        res = self.schema.deserialize(self.data)
        self.assertEqual(30000, res["provincie"]["niscode"])
        self.assertEqual("West-Vlaanderen", res["provincie"]["naam"])
        self.assertEqual(191, res["gemeente"]["id"])
        self.assertEqual(31043, res["gemeente"]["niscode"])
        self.assertEqual("Knokke-Heist", res["gemeente"]["naam"])

    def test_locatie_deelgemeente_no_niscode(self):
        self.data['gemeente'] = {'naam': 'Leuven'}
        self.data['postcode'] = '3000'
        self.data['deelgemeente'] = {"naam": "Heverlee"}
        with self.assertRaises(colander.Invalid) as inv:
            self.schema.deserialize(self.data)
        self.assertEqual("deelgemeente moet een niscode hebben",
                         inv.exception.asdict()[''])

    def test_locatie_deelgemeente_different_niscode(self):
        self.data['gemeente'] = {'naam': 'Leuven'}
        self.data['postcode'] = '3000'
        self.data['deelgemeente'] = {"naam": "Kessel - Lo"}
        with self.assertRaises(colander.Invalid) as inv:
            self.schema.deserialize(self.data)
        self.assertEqual(
            "niscode van gemeente en deelgemeente moet hetzelfde zijn "
            "(uitgezonderd, toegevoegde letters van deelgemeentes)",
            inv.exception.asdict()[''])

    def test_locatie_deelgemeente_niscode_letter(self):
        self.data['gemeente'] = {'naam': 'Leuven'}
        self.data['postcode'] = '3000'
        self.data['deelgemeente'] = {"naam": "Wilsele"}
        self.data['straat'] = 'Fonteinstraat'
        self.data['straat_id'] = 34819
        res = self.schema.deserialize(self.data)
        self.assertNotEqual(res['gemeente']['niscode'], res['deelgemeente']['niscode'])

    def test_locatie_deelgemeente_niscode(self):
        self.data['gemeente'] = {'naam': 'Leuven'}
        self.data['postcode'] = '3000'
        self.data['deelgemeente'] = {"niscode": "24062X"}
        self.data['straat'] = 'Fonteinstraat'
        self.data['straat_id'] = 34819
        res = self.schema.deserialize(self.data)
        self.assertEqual(res['deelgemeente']['naam'], 'Wilsele')


class LocatieAdresSchemaNodeTests(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.crab_gateway = Mock(return_value=crab_gateway_mock)
        self.request.capakey_gateway = Mock(return_value=capakey_gateway_mock)

        adressen_schema = LocationElementSchemaNode()

        self.schema = adressen_schema.bind(
            request=self.request
        )

    def test_perceel(self):
        res = self.schema.deserialize(
            {
                "id": 1,
                "type": "https://id.erfgoed.net/vocab/ontology#LocatieElementPerceel",
                "provincie": {
                    "naam": "Vlaams-Brabant",
                    "niscode": 20001
                },
                "gemeente": {
                    "naam": "Leuven",
                    "id": 143,
                    "niscode": 24062
                },
                "perceel": {
                    "afdeling": u"LEUVEN  5 AFD",
                    "perceel": u"0415/00F000",
                    "capakey": u"24505F0415/00F000",
                    "sectie": u"F"
                }
            }
        )
        self.assertEqual(20001, res["provincie"]["niscode"])
        self.assertEqual("24505F0415/00F000", res["perceel"]["capakey"])

    def test_perceel_missing_gemeente(self):
        res = self.schema.deserialize(
            {
                "id": 1,
                "type": "https://id.erfgoed.net/vocab/ontology#LocatieElementPerceel",
                "provincie": {
                    "naam": "Vlaams-Brabant",
                    "niscode": 20001
                },
                "gemeente": {
                },
                "perceel": {
                    "afdeling": u"LEUVEN  5 AFD",
                    "perceel": u"0415/00F000",
                    "capakey": u"24505F0415/00F000",
                    "sectie": u"F"
                }
            }
        )
        self.assertEqual(143, res["gemeente"]["id"])
        self.assertEqual(24062, res["gemeente"]["niscode"])
        self.assertEqual("Leuven", res["gemeente"]["naam"])

    def test_perceel_missing_provincie(self):
        res = self.schema.deserialize(
            {
                "id": 1,
                "type": "https://id.erfgoed.net/vocab/ontology#LocatieElementPerceel",
                "provincie": {
                },
                "gemeente": {
                    "naam": "Leuven",
                    "id": 143,
                    "niscode": 24062
                },
                "perceel": {
                    "afdeling": u"LEUVEN  5 AFD",
                    "perceel": u"0415/00F000",
                    "capakey": u"24505F0415/00F000",
                    "sectie": u"F"
                }
            }
        )
        self.assertEqual(20001, res["provincie"]["niscode"])
        self.assertEqual("Vlaams-Brabant", res["provincie"]["naam"])

    def test_perceel_capakey_wrong_format(self):
        with self.assertRaises(colander.Invalid) as inv:
            self.schema.deserialize(
                {
                    "id": 1,
                    "type": "https://id.erfgoed.net/vocab/ontology#LocatieElementPerceel",
                    "provincie": {
                        "naam": "Vlaams-Brabant",
                        "niscode": 20001
                    },
                    "gemeente": {
                        "naam": "Leuven",
                        "id": 143,
                        "niscode": 24062
                    },
                    "perceel": {
                        "afdeling": u"LEUVEN  5 AFD",
                        "perceel": u"0415/00F000",
                        "capakey": u"24505F04TTTTEES15/00F000",
                        "sectie": u"F"
                    }
                }
            )
        self.assertEqual("Ongeldige capakey", inv.exception.asdict()['perceel'])

    def test_perceel_non_existing_afdeling(self):
        with self.assertRaises(colander.Invalid) as inv:
            self.schema.deserialize(
                {
                    "id": 1,
                    "type": "https://id.erfgoed.net/vocab/ontology#LocatieElementPerceel",
                    "provincie": {
                        "naam": "Vlaams-Brabant",
                        "niscode": 20001
                    },
                    "gemeente": {
                        "naam": "Leuven",
                        "id": 143,
                        "niscode": 24062
                    },
                    "perceel": {
                        "afdeling": u"x",
                        "perceel": u"0415/00F000",
                        "capakey": u"55555F0415/00F000",
                        "sectie": u"F"
                    }
                }
            )
        self.assertEqual("ongeldige kadastrale afdeling voor capakey 55555F0415/00F000",
                         inv.exception.asdict()[''])

    def test_perceel_afdeling_non_existing_gemeente_non_given(self):
        with self.assertRaises(colander.Invalid) as inv:
            self.schema.deserialize(
                {
                    "id": 1,
                    "type": "https://id.erfgoed.net/vocab/ontology#LocatieElementPerceel",
                    "perceel": {
                        "afdeling": u"x",
                        "perceel": u"0415/00F000",
                        "capakey": u"66666F0415/00F000",
                        "sectie": u"F"
                    }
                }
            )
        self.assertEqual("geen correcte gemeente_id gevonden voor de gemeente None",
                         inv.exception.asdict()[''])

    def test_perceel_only_capakey(self):
        res = self.schema.deserialize(
            {
                "id": 1,
                "type": "https://id.erfgoed.net/vocab/ontology#LocatieElementPerceel",
                "provincie": {
                },
                "gemeente": {
                    "naam": "Leuven",
                    "id": 143,
                    "niscode": 24062
                },
                "perceel": {
                    "afdeling": None,
                    "perceel": None,
                    "capakey": u"24505F0415/00F000",
                    "sectie": None
                }
            }
        )
        self.assertEqual("LEUVEN  5 AFD", res["perceel"]["afdeling"])
        self.assertEqual("0415/00F000", res["perceel"]["perceel"])
        self.assertEqual("F", res["perceel"]["sectie"])

    def test_public_domain_locatie(self):
        res = self.schema.deserialize(
            {
                "type": "https://id.erfgoed.net/vocab/ontology#LocatieElementOpenbaarDomein",
                "provincie": {
                    "niscode": 20001,
                    "naam": "Vlaams-Brabant"
                },
                "gemeente": {
                    "naam": "Leuven",
                    "id": 143,
                    "niscode": 24062
                },
                "omschrijving": "Gemeentepark van Atlantis"
            }
        )
        self.assertEqual("Gemeentepark van Atlantis", res["omschrijving"])

    def test_locatie(self):
        res = self.schema.deserialize(
            {
                "type": "https://id.erfgoed.net/vocab/ontology#LocatieElement",
                "provincie": {
                    "niscode": 20001,
                    "naam": "Vlaams-Brabant"
                },
                "gemeente": {
                    "naam": "Leuven",
                    "id": 143,
                    "niscode": 24062
                },
            }
        )
        self.assertEqual("Vlaams-Brabant", res["provincie"]["naam"])

    def test_locatie_gemeente_id(self):
        res = self.schema.deserialize(
            {
                "type": "https://id.erfgoed.net/vocab/ontology#LocatieElement",
                "provincie": {
                },
                "gemeente": {
                    "id": 143
                },
            }
        )
        self.assertEqual(20001, res["provincie"]["niscode"])
        self.assertEqual("Vlaams-Brabant", res["provincie"]["naam"])
        self.assertEqual(143, res["gemeente"]["id"])
        self.assertEqual(24062, res["gemeente"]["niscode"])
        self.assertEqual("Leuven", res["gemeente"]["naam"])

    def test_locatie_gemeente_niscode(self):
        res = self.schema.deserialize(
            {
                "type": "https://id.erfgoed.net/vocab/ontology#LocatieElement",
                "provincie": {
                },
                "gemeente": {
                    "niscode": 24062
                },
            }
        )
        self.assertEqual(20001, res["provincie"]["niscode"])
        self.assertEqual("Vlaams-Brabant", res["provincie"]["naam"])
        self.assertEqual(143, res["gemeente"]["id"])
        self.assertEqual(24062, res["gemeente"]["niscode"])
        self.assertEqual("Leuven", res["gemeente"]["naam"])

    def test_locatie_gemeente_naam(self):
        res = self.schema.deserialize(
            {
                "type": "https://id.erfgoed.net/vocab/ontology#LocatieElement",
                "provincie": {
                },
                "gemeente": {
                    "naam": "Leuven"
                },
            }
        )
        self.assertEqual(20001, res["provincie"]["niscode"])
        self.assertEqual("Vlaams-Brabant", res["provincie"]["naam"])
        self.assertEqual(143, res["gemeente"]["id"])
        self.assertEqual(24062, res["gemeente"]["niscode"])
        self.assertEqual("Leuven", res["gemeente"]["naam"])

    def test_locatie_gemeente_wrong_id(self):
        with self.assertRaises(colander.Invalid) as inv:
            self.schema.deserialize(
                {
                    "type": "https://id.erfgoed.net/vocab/ontology#LocatieElement",
                    "provincie": {
                    },
                    "gemeente": {
                        "id": 14
                    },
                }
            )
        self.assertEqual("geen correcte gemeente_id gevonden voor de gemeente None",
                         inv.exception.asdict()[''])

    def test_locatie_gemeente_wrong_niscode(self):
        with self.assertRaises(colander.Invalid) as inv:
            self.schema.deserialize(
                {
                    "type": "https://id.erfgoed.net/vocab/ontology#LocatieElement",
                    "provincie": {
                    },
                    "gemeente": {
                        "niscode": 2402
                    },
                }
            )
        self.assertEqual("geen correcte gemeente_id gevonden voor de gemeente None",
                         inv.exception.asdict()[''])

    def test_locatie_gemeente_wrong_naam(self):
        with self.assertRaises(colander.Invalid) as inv:
            self.schema.deserialize(
                {
                    "type": "https://id.erfgoed.net/vocab/ontology#LocatieElement",
                    "provincie": {
                    },
                    "gemeente": {
                        "naam": "Leuvenxxx"
                    },
                }
            )
        self.assertEqual("geen correcte gemeente_id gevonden voor de gemeente Leuvenxxx",
                         inv.exception.asdict()[''])

    def test_muliple_location_elements(self):
        location_elements = [
            {
                "id": 1,
                "type": "https://id.erfgoed.net/vocab/ontology#LocatieElementAdres",
                "land": "BE",
                "postcode": "8300",
                "gemeente": {
                    "naam": "Knokke-Heist",
                    "id": 191
                },
                "straat": "Nieuwstraatje",
                "straat_id": 48086,
                "huisnummer": "6",
                "huisnummer_id": None,
                "subadres": "1",
                "subadres_id": None
            },
            {
                "perceel": {
                    "afdeling": u"LEUVEN  5 AFD",
                    "perceel": u"0415/00F000",
                    "capakey": u"24505F0415/00F000",
                    "sectie": u"F"
                },
                "land": "BE",
                "type": "https://id.erfgoed.net/vocab/ontology#LocatieElementPerceel"
            }
        ]

        class LocatieElementen(colander.SequenceSchema):
            item = LocationElementSchemaNode()

        adressen_schema = LocatieElementen()
        schema = adressen_schema.bind(request=self.request)
        result = schema.deserialize(location_elements)
        self.assertEqual("Knokke-Heist", result[0]['gemeente']['naam'])
        self.assertEqual("West-Vlaanderen", result[0]['provincie']['naam'])
        self.assertEqual("Leuven", result[1]['gemeente']['naam'])
        self.assertEqual("Vlaams-Brabant", result[1]['provincie']['naam'])

    def test_if_crab_is_unavailable_a_warning_will_be_logged_when_deserializing_locatie_element_adres(self):
        capakey_gateway = Mock()
        self.first_time = True
        capakey_gateway.list_kadastrale_afdelingen = Mock()
        capakey_gateway.list_kadastrale_afdelingen.side_effect = self._list_kadastrale_afdelingen_with_exception_first_time
        self.request.capakey_gateway = Mock(return_value=capakey_gateway)

        log = Mock(warning=Mock())
        with patch('oe_geoutils.validation.validators_location_elements.log', log):
            self.schema.deserialize(
                {
                    "id": 1,
                    "type": "https://id.erfgoed.net/vocab/ontology#LocatieElementPerceel",
                    "provincie": {
                        "naam": "Vlaams-Brabant",
                        "niscode": 20001
                    },
                    "gemeente": {
                        "naam": "Leuven",
                        "id": 143,
                        "niscode": 24062
                    },
                    "perceel": {
                        "afdeling": u"LEUVEN  5 AFD",
                        "perceel": u"0415/00F000",
                        "capakey": u"24505F0415/00F000",
                        "sectie": u"F"
                    }
                }
            )
            self.assertEqual(log.warning.call_count, 1)

    def _list_kadastrale_afdelingen_with_exception_first_time(self):
        if self.first_time:
            self.first_time = False
            raise GatewayRuntimeException('timeout', None)
        else:
            return list_kadastrale_afdelingen()
