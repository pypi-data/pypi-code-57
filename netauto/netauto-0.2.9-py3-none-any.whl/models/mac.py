from datetime import datetime
from typing import List

from pydantic import BaseModel


class Mac(BaseModel):
    active: bool
    mac_address: str
    switch_ip: str
    switch_port_id: int
    switch_serial_number: str
    vlan_id: int


class MacInDB(Mac):
    oui: str
    kit_printer: bool
    last_seen: datetime
    first_seen: datetime


class MacInDBList(BaseModel):
    result: List[MacInDB]


class MacDeleted(BaseModel):
    mac_address: str
