from datetime import date, time
from urllib.parse import urljoin

import requests

from .. import Connection, Port, VesselClass
from .historical_tonnage_list import HistoricalTonnageList
from .vessel_filter import VesselFilter
from . import _historical_tonnage_list_json


class HistoricalTonnageListAPI:
    def __init__(self, connection: Connection = None):
        self.__connection = connection or Connection()

    def get_historical_tonnage_list(
            self,
            loading_port: Port,
            vessel_class: VesselClass,
            days_forward: int = None,
            start_date: date = None,
            end_date: date = None,
            time: time = None,
            vessel_filter: VesselFilter = None) -> HistoricalTonnageList:
        url = urljoin(
            self.__connection.api_host,
            'htl-api/historical-tonnage-list/'
        )
        query_string = {
            'loadingPort': loading_port.id,
            'vesselClass': vessel_class.id,
            'daysForward': days_forward,
            'startDate': _format_date(start_date),
            'endDate': _format_date(end_date),
            'time': time.strftime('%H:%M') if time else None
        }

        response = requests.get(
            url,
            params=query_string,
            headers=self.__connection.headers
        )
        response.raise_for_status()

        return _historical_tonnage_list_json.parse(
            response.json(),
            vessel_filter or VesselFilter()
        )


def _format_date(date: date) -> str:
    return date.strftime('%Y-%m-%d') if date else None
