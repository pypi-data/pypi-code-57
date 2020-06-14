import requests
from f1.models import Schedule, Race, Circuit, Location
from datetime import datetime

SCHEDULE_ENDPOINT = 'http://ergast.com/api/f1/current.json'


def __get_location(location_data) -> Location:
    return Location(
        float(location_data['lat']),
        float(location_data['long']),
        location_data['locality'],
        location_data['country']
    )


def __get_circuit(circuit_data) -> Circuit:
    location = __get_location(circuit_data['Location'])
    return Circuit(
        circuit_data['circuitId'],
        circuit_data['url'],
        circuit_data['circuitName'],
        location
    )


def __get_race(race_data) -> Race:
    circuit_data = race_data['Circuit']
    circuit = __get_circuit(circuit_data)
    return Race(
        int(race_data['round']),
        race_data['url'],
        race_data['raceName'],
        circuit,
        datetime.strptime(race_data['date'], '%Y-%m-%d').date(),
        datetime.strptime(race_data['time'], '%H:%M:%SZ').time()
    )


def get_current_schedule() -> Schedule:
    json = requests.get(SCHEDULE_ENDPOINT).json()
    data = json['MRData']['RaceTable']
    season = data['season']
    races = [__get_race(r) for r in data['Races']]
    return Schedule(season, races)
