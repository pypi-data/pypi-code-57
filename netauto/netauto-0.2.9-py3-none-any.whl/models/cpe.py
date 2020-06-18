from datetime import datetime
from typing import List

from pydantic import BaseModel


class CPEInterfaces(BaseModel):
    interface_name: str
    description: str


class CPEVirtualInterface(CPEInterfaces):
    ip: str
    subnetmask: str
    network_type: str
    vrf: str
    ip_helper: List[str]


class CPEPhysicalInterface(CPEInterfaces):
    service_policy: List[str]
    access: bool
    trunk: bool
    routed: bool


class CPE(BaseModel):
    hostname: str
    model: str
    circuit_id: str
    circuit_bandwidth: int
    circuit_fiber_redundancy: bool
    circuit_4g: bool
    virtual_interface: List[CPEVirtualInterface]
    physical_interface: List[CPEPhysicalInterface]
    mgmt_ip: str
    syslocation: str
    address: str
    zip_code: int
    city: str


class CPEInDB(CPE):
    last_change: datetime
    first_seen: datetime


class CPEInDBList(BaseModel):
    result: List[CPEInDB]


class CPEDeleted(BaseModel):
    circuit_id: str


class SSHInput(BaseModel):
    username: str
    password: str
    ip: str
    commands: List[str]


class SSHCommandOutput(BaseModel):
    command: str
    output: List[str]


class SSHReturn(BaseModel):
    result: List[SSHCommandOutput]
