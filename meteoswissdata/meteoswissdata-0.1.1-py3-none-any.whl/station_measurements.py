from enum import Enum
import json
from urllib.request import urlopen

REPOSITORY = 'allestuetsmerweh/meteoswissdata'
BRANCH = 'data'

def get_base_url(repository, branch):
    return f'https://raw.githubusercontent.com/{repository}/{branch}/'


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
    MeasurementType.AIR_TEMPERATURE: '°C',
    MeasurementType.PRECIPITATION: 'mm',
    MeasurementType.SUNSHINE_DURATION: 'min',
    MeasurementType.GLOBAL_RADIATION: 'W/m²',
    MeasurementType.RELATIVE_AIR_HUMIDITY: '%',
    MeasurementType.DEW_POINT: '°C',
    MeasurementType.WIND_DIRECTION: '°',
    MeasurementType.WIND_SPEED: 'km/h',
    MeasurementType.GUST_PEAK: 'km/h',
    MeasurementType.PRESSURE_STATION_LEVEL: 'hPa',
    MeasurementType.PRESSURE_SEA_LEVEL: 'hPa',
    MeasurementType.PRESSURE_SEA_LEVEL_STANDARD_ATMOSPHERE: 'hPa',
    MeasurementType.GEOPOTENTIAL_HEIGHT_850_HPA: 'gpm',
    MeasurementType.GEOPOTENTIAL_HEIGHT_700_HPA: 'gpm',
    MeasurementType.WIND_DIRECTION_VECTORIAL_TOOL_1: '°',
    MeasurementType.WIND_SPEED_TOWER: 'km/h',
    MeasurementType.GUST_PEAK_TOWER: 'km/h',
    MeasurementType.AIR_TEMPERATURE_TOOL_1: '°C',
    MeasurementType.RELATIVE_AIR_HUMIDITY_TOWER: '%',
    MeasurementType.DEW_POINT_TOWER: '°C',
}


class StationMeasurementsFetcher:
    base_url: str = get_base_url(REPOSITORY, BRANCH)

    def get_stations(self):
        url = f'{self.base_url}stations_list.json'
        with urlopen(url) as uh:
            return json.load(uh)

    def get_stations_data(self):
        url = f'{self.base_url}station_measurements.json'
        with urlopen(url) as uh:
            return json.load(uh)

    def get_station_data(self, station):
        station = station.upper()
        url = f'{self.base_url}station_measurements/{station}.json'
        with urlopen(url) as uh:
            return json.load(uh)
