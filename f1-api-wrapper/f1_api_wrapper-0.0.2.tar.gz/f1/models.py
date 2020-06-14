from dataclasses import dataclass
from datetime import date, time
from typing import List


@dataclass
class Location:
    lat: float
    long: float
    locality: str
    country: str


@dataclass
class Circuit:
    circuit_id: str
    url: str
    circuit_name: str
    location: Location


@dataclass
class Race:
    round: int
    url: str
    race_name: str
    circuit: Circuit
    date: date
    time: time


@dataclass
class Schedule:
    season: int
    races: List[Race]
