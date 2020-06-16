from enum import Enum
import json
from urllib.request import urlopen

REPOSITORY = 'allestuetsmerweh/meteoswissdata'
BRANCH = 'data'
BASE_URL = f'https://raw.githubusercontent.com/{REPOSITORY}/{BRANCH}/'


class MeasurementType(Enum):
    AIR_TEMPERATURE = 'tre200s0'
    PRECIPITATION = 'rre150z0'
    SUNSHINE_DURATION = 'sre000z0'
    GLOBAL_RADIATION = 'gre000z0'
    RELATIVE_AIR_HUMIDITY = 'ure200s0'
    DEW_POINT = 'tde200s0'
    WIND_DIRECTION = 'dkl010z0'
    WIND_SPEED = 'fu3010z0'
    GUST_PEAK = 'fu3010z1'
    PRESSURE_STATION_LEVEL = 'prestas0'
    PRESSURE_SEA_LEVEL = 'pp0qffs0'
    PRESSURE_SEA_LEVEL_STANDARD_ATMOSPHERE = 'pp0qnhs0'
    GEOPOTENTIAL_HEIGHT_850_HPA = 'ppz850s0'
    GEOPOTENTIAL_HEIGHT_700_HPA = 'ppz700s0'
    WIND_DIRECTION_VECTORIAL_TOOL_1 = 'dv1towz0'
    WIND_SPEED_TOWER = 'fu3towz0'
    GUST_PEAK_TOWER = 'fu3towz1'
    AIR_TEMPERATURE_TOOL_1 = 'ta1tows0'
    RELATIVE_AIR_HUMIDITY_TOWER = 'uretows0'
    DEW_POINT_TOWER = 'tdetows0'

UNIT_BY_MEASUREMENT_TYPE = {
    AIR_TEMPERATURE: '°C'
    PRECIPITATION: 'mm'
    SUNSHINE_DURATION: 'min'
    GLOBAL_RADIATION: 'W/m²'
    RELATIVE_AIR_HUMIDITY: '%'
    DEW_POINT: '°C'
    WIND_DIRECTION: '°'
    WIND_SPEED: 'km/h'
    GUST_PEAK: 'km/h'
    PRESSURE_STATION_LEVEL: 'hPa'
    PRESSURE_SEA_LEVEL: 'hPa'
    PRESSURE_SEA_LEVEL_STANDARD_ATMOSPHERE: 'hPa'
    GEOPOTENTIAL_HEIGHT_850_HPA: 'gpm'
    GEOPOTENTIAL_HEIGHT_700_HPA: 'gpm'
    WIND_DIRECTION_VECTORIAL_TOOL_1: '°'
    WIND_SPEED_TOWER: 'km/h'
    GUST_PEAK_TOWER: 'km/h'
    AIR_TEMPERATURE_TOOL_1: '°C'
    RELATIVE_AIR_HUMIDITY_TOWER: '%'
    DEW_POINT_TOWER: '°C'
}


class StationMeasurementsFetcher:
    base_url: str = BASE_URL

    def get_stations(self):
        with urlopen(f'{self.base_url}stations_list.json') as uh:
            return json.load(uh)

    def get_stations_data(self):
        with urlopen(f'{self.base_url}station_measurements.json') as uh:
            return json.load(uh)

    def get_station_data(self, station):
        station = station.upper()
        with urlopen(f'{self.base_url}station_measurements/{station}.json') as uh:
            return json.load(uh)
