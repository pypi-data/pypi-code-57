from os.path import dirname, join, realpath
from pathlib import Path

from .station_measurements import StationMeasurementsFetcher

EXPECTED_ABC_DATA = {
    'time': '2020-06-15T20:40:00',
    'tre200s0': 8.8,
    'rre150z0': 0.1,
    'sre000z0': 0.0,
    'gre000z0': 2.0,
    'ure200s0': 96.0,
    'tde200s0': 8.2,
    'dkl010z0': 179.0,
    'fu3010z0': 4.3,
    'fu3010z1': 9.0,
    'prestas0': 871.6,
    'pp0qffs0': None,
    'pp0qnhs0': 1022.2,
    'ppz850s0': 1534.1,
    'ppz700s0': None,
    'dv1towz0': None,
    'fu3towz0': None,
    'fu3towz1': None,
    'ta1tows0': None,
    'uretows0': None,
    'tdetows0': None,
}


class TestStationMeasurementsFetcher:
    fetcher: StationMeasurementsFetcher

    @classmethod
    def setup_class(cls):
        base_path = realpath(join(
            dirname(__file__),
            'station_measurements_test_data',
        ))
        base_uri = Path(base_path).as_uri()
        cls.fetcher = StationMeasurementsFetcher()
        cls.fetcher.base_url = f'{base_uri}/'

    def test_get_stations(self):
        expected = ['ABC', 'XYZ']
        actual = self.fetcher.get_stations()
        assert actual == expected

    def test_get_stations_data(self):
        expected = {'ABC': EXPECTED_ABC_DATA}
        actual = self.fetcher.get_stations_data()
        assert actual == expected

    def test_get_station(self):
        expected = EXPECTED_ABC_DATA
        actual = self.fetcher.get_station_data('Abc')
        assert actual == expected
