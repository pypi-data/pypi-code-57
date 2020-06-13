from .extractor import Extractor
from postal.parser import parse_address
from ..simple_types import (FuzzyItalianZIPCodeType,
                            MunicipalityType, CountryType, RegionType)
from .default_extractor import DefaultExtractor
from typing import Dict
import compress_json


class AddressExtractor(Extractor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._default_extractor = DefaultExtractor()
        self._mapping = compress_json.local_load("libpostal_mapping.json")
        self._validators = {
            "ItalianZIPCodeType": FuzzyItalianZIPCodeType(),
            "Municipality": MunicipalityType(),
            "Country": CountryType(),
            "Region": RegionType()
        }

        self._unsupported = [
            "city_district", "unit", "state_district"
        ]

    def extract(self, candidate: str, candidate_type: str, **kwargs) -> Dict:
        lower = candidate.lower()
        parsed = parse_address(
            candidate, language="IT", country="IT")

        has_errored = False

        for _, key in parsed:
            if key in self._unsupported:
                has_errored = True
                break

        if has_errored:
            return self._default_extractor.extract(
                candidate, candidate_type, **kwargs
            )

        parsed = {
            self._mapping[prediction]: [
                candidate[
                    lower.find(value):lower.find(value)+len(value)
                ]
            ]
            for value, prediction in parsed
        }

        for key, (value,) in parsed.items():
            if key in self._validators:
                if not self._validators[key].validate(value):
                    has_errored = True
                    break

        if has_errored:
            return self._default_extractor.extract(
                candidate, candidate_type, **kwargs
            )

        return self.build_dictionary(
            candidate=candidate,
            values=parsed
        )
