import time
import uuid
from datetime import datetime

import maya
from faker import Faker
from pydantic import BaseModel, Field

fake = Faker()


def random_day():
    start = fake.date_between(start_date="-10y")
    current_datetime = datetime.fromordinal(start.toordinal())
    mayatime = maya.MayaDT.from_datetime(current_datetime)
    return mayatime._epoch


def hex_uuid():
    return uuid.uuid4().hex


class BacktestConfig(BaseModel):
    name:str = Field(default_factory=fake.company)
    description: str = Field(default_factory=fake.sentence)
    user:str = Field(default_factory=hex_uuid)

    base:str = "USD"
    initial:str = 10000.0
    exchange:str = "binance"

    start: float = Field(default_factory=random_day)
    end: float = Field(default_factory=random_day)
    lookback: dict = {}
    step: dict = {}

    strategy:str = Field(default_factory=hex_uuid)
    universe:str = Field(default_factory=hex_uuid)

