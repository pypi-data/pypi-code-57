from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from .open_area import OpenArea
from .location_taxonomy import LocationTaxonomy


@dataclass(frozen=True, eq=False)
class Vessel:
    imo: int
    name: str
    vessel_class: str
    ice_class: str
    year_built: int
    deadweight: int
    length_overall: float
    breadth_extreme: int
    market_deployment: str
    push_type: str
    open_port: str
    open_date: datetime
    operational_status: str
    commercial_operator: str
    commercial_status: str
    eta: datetime
    last_fixed: int
    latest_ais: datetime
    subclass: str
    willing_to_switch_subclass: bool
    open_prediction_accuracy: str
    open_areas: List[OpenArea]

    def __post_init__(self):
        if self.open_areas is None:
            object.__setattr__(self, 'open_areas', [])

    @property
    def open_country(self) -> str:
        return self.__area_name_by_taxonomy(LocationTaxonomy.COUNTRY)

    @property
    def open_narrow_area(self) -> str:
        return self.__area_name_by_taxonomy(LocationTaxonomy.NARROW_AREA)

    @property
    def open_wide_area(self) -> str:
        return self.__area_name_by_taxonomy(LocationTaxonomy.WIDE_AREA)

    def __area_name_by_taxonomy(self, taxonomy: str) -> str:
        return next(
            iter([a.name for a in self.open_areas if a.location_taxonomy == taxonomy]),
            None)
