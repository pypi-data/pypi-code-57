from typing import List

from pydantic import BaseModel, Field


class SnmpOIDData(BaseModel):
    oid: str
    value: str


class SnmpGetDeviceData(BaseModel):
    ip: str
    data: List[SnmpOIDData]
    message: str


class ReturnGetData(BaseModel):
    result: List[SnmpGetDeviceData]


class SnmpBulkRootOID(BaseModel):
    root_oid: str
    root_oid_data: List[SnmpOIDData]


class SnmpBulkDeviceData(BaseModel):
    ip: str
    data: List[SnmpBulkRootOID]
    message: str


class ReturnBulkData(BaseModel):
    result: List[SnmpBulkDeviceData]


class SnmpRequestData(BaseModel):
    snmp_version: int = Field(ge=2, le=3, default=...)
    ip_list: List[str]
    oids: List[str]
