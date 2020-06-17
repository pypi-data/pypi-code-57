from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Iterable

from .vessel import Vessel


@dataclass(eq=False)
class VesselFilter:
    push_types: List[str] = field(default_factory=list)
    market_deployments: List[str] = field(default_factory=list)
    commercial_statuses: List[str] = field(default_factory=list)
    subclasses: List[str] = field(default_factory=list)
    add_willing_to_switch_subclass: bool = False
    latest_ais_since: timedelta = timedelta.max

    def _apply(self, vessels: Iterable[Vessel], tonnage_list_date: datetime) -> Iterable[Vessel]:
        return filter(
            lambda vessel: self.__does_vessel_match(vessel, tonnage_list_date),
            vessels
        )

    def __does_vessel_match(self, vessel: Vessel, tonnage_list_date: datetime) -> bool:
        matches_push_type = _matches_filter(
            vessel.push_type,
            self.push_types
        )
        matches_market_deployment = _matches_filter(
            vessel.market_deployment,
            self.market_deployments
        )
        matches_commercial_status = _matches_filter(
            vessel.commercial_status,
            self.commercial_statuses
        )

        ignore_subclass = (
            self.add_willing_to_switch_subclass and vessel.willing_to_switch_subclass)
        matches_subclass = ignore_subclass or _matches_filter(
            vessel.subclass,
            self.subclasses
        )

        is_outdated = (tonnage_list_date - vessel.latest_ais > self.latest_ais_since
                       if tonnage_list_date and vessel.latest_ais else False)

        return (
            matches_push_type
            and matches_market_deployment
            and matches_commercial_status
            and matches_subclass
            and not is_outdated)


def _matches_filter(vessel_value, filter_values: List) -> bool:
    return (
        not filter_values
        or any(v == vessel_value for v in filter_values)
    )
