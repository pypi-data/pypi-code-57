from datetime import datetime, timezone
from typing import List, Iterable

import dateutil

from .historical_tonnage_list import HistoricalTonnageList
from .tonnage_list import TonnageList
from .vessel_filter import VesselFilter
from .vessel import Vessel
from .open_area import OpenArea


def parse(json, vessel_filter: VesselFilter) -> HistoricalTonnageList:
    static_vessel_data = json.get('staticVesselData') or []
    tonnage_lists = json.get('tonnageLists') or []

    return HistoricalTonnageList(
        map(
            lambda tl: _to_tonnage_list(tl, static_vessel_data, vessel_filter),
            tonnage_lists
        )
    )


def _parse_datetime(value: str) -> datetime:
    result = dateutil.parser.isoparse(value) if value else None
    if (result is None):
        return None

    return result.replace(tzinfo=timezone.utc)


def _to_vessel(pit_vessel_data: dict, static_vessel_data: List[dict]) -> Vessel:
    imo = pit_vessel_data['imo']
    data_for_imo = next(
        filter(lambda v: v['imo'] == imo, static_vessel_data),
        {}
    )

    return Vessel(
        imo,
        data_for_imo.get('vesselName'),
        data_for_imo.get('vesselClass'),
        data_for_imo.get('iceClass'),
        data_for_imo.get('yearBuilt'),
        data_for_imo.get('deadWeight'),
        data_for_imo.get('lengthOverall'),
        data_for_imo.get('breadthExtreme'),
        pit_vessel_data.get('marketDeployment'),
        pit_vessel_data.get('pushType'),
        pit_vessel_data.get('openPort'),
        _parse_datetime(pit_vessel_data.get('openDate')),
        pit_vessel_data.get('operationalStatus'),
        pit_vessel_data.get('commercialOperator'),
        pit_vessel_data.get('commercialStatus'),
        _parse_datetime(pit_vessel_data.get('eta')),
        pit_vessel_data.get('lastFixed'),
        _parse_datetime(pit_vessel_data.get('latestAis')),
        data_for_imo.get('subclass'),
        data_for_imo.get('willingToSwitchSubclass'),
        pit_vessel_data.get('openPredictionAccuracy'),
        list(
            map(
                lambda a: OpenArea(a.get('name'), a.get('locationTaxonomy')),
                pit_vessel_data.get('openAreas') or []
            )
        )
    )


def _to_tonnage_list(
        tonnage_list_json: dict,
        static_vessel_data: List[dict],
        vessel_filter: VesselFilter) -> TonnageList:
    date = _parse_datetime(tonnage_list_json['date'])
    vessels = list(
        vessel_filter._apply(
            map(
                lambda pit_vessel_data: _to_vessel(
                    pit_vessel_data,
                    static_vessel_data
                ),
                tonnage_list_json['pointInTimeVesselData']
            ),
            date
        )
    )

    return TonnageList(date, vessels)
