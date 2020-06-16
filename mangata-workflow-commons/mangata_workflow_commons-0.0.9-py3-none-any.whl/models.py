# Copyright (C) 2019 Taylor Publishing Company. All Rights Reserved.
#
# Project:  digital-workflow-handler
# Module:   models.py
# Created:  2019-07-18
#

"""
Contains the model classes used by SQLAlchemy for Baan and Mysql database/repository interactions.

Copyright (C) 2020 Taylor Publishing Company. All Rights Reserved.

"""


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DATE, DECIMAL, Index, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import validates

Base = declarative_base()
SCHEMA = {"schema": "triton"}


# This Baan Database is here only for historical reference purposes, NetSuite404 is the new MySQL table model


# Baan Database
class DigitalAnnoucementOrders(Base):
    __tablename__ = "ttmxch404100"
    __table_args__ = (
        SCHEMA,
    )

    ORNO_LEN = 100
    GUID_LEN = 100
    ITEM_LEN = 100
    ITYP_LEN = 25
    PTYP_LEN = 5
    THEM_LEN = 100
    MORN_LEN = 9
    QNTY_LEN = 10
    SMIN_LEN = 19
    DSCA_LEN = 100
    SIZE_LEN = 100
    NAME_LEN = 100
    SRNO_LEN = 10
    SEQN_LEN = 10
    IDNO_LEN = 6
    REFCNTD_LEN = 1
    REFCNTU_LEN = 1
    EMNO_LEN = 7
    PDAT_LEN = 25
    NAMA_LEN = 50
    NAMC_LEN = 80
    NAMD_LEN = 80
    CITY_LEN = 50
    STATE_LEN = 2
    NAMF_LEN = 10
    CNTY_LEN = 50
    TELP_LEN = 15
    EMAIL_LEN = 100
    TOTL_LEN = 8
    SHIP_LEN = 8
    TAX_LEN = 8
    PRIC_LEN = 8
    ITTL_LEN = 8
    METH_LEN = 1
    ODIS_LEN = 8
    IDIS_LEN = 8
    CPNC_LEN = 50
    IQUA_LEN = 10

    orno = Column("T$ORNO", String(ORNO_LEN), primary_key=True)
    guid = Column("T$GUID", String(GUID_LEN))
    item = Column("T$ITEM", String(ITEM_LEN))
    ityp = Column("T$ITYP", NUMBER)
    ptyp = Column("T$PTYP", NUMBER)
    them = Column("T$THEM", String(THEM_LEN))
    morn = Column("T$MORN", String(MORN_LEN))
    qnty = Column("T$QNTY", NUMBER)
    smin = Column("T$SMIN", NUMBER)
    dsca = Column("T$DSCA", String(DSCA_LEN))
    size = Column("T$SIZE", String(SIZE_LEN))
    name = Column("T$NAME", String(NAME_LEN))
    srno = Column("T$SRNO", NUMBER)
    seqn = Column("T$SEQN", NUMBER, primary_key=True)
    idno = Column("T$IDNO", String(IDNO_LEN))
    emno = Column("T$EMNO", String(EMNO_LEN))
    pdat = Column("T$PDAT", String(PDAT_LEN))
    nama = Column("T$NAMA", String(NAMA_LEN))
    namc = Column("T$NAMC", String(NAMC_LEN))
    namd = Column("T$NAMD", String(NAMD_LEN))
    city = Column("T$CITY", String(CITY_LEN))
    state = Column("T$STATE", String(STATE_LEN))
    namf = Column("T$NAMF", String(NAMF_LEN))
    cnty = Column("T$CNTY", String(CNTY_LEN))
    telp = Column("T$TELP", String(TELP_LEN))
    email = Column("T$EMAIL", String(EMAIL_LEN))
    odat = Column("T$ODAT", DATE)
    totl = Column("T$TOTL", DECIMAL(10, 2))
    ship = Column("T$SHIP", DECIMAL(10, 2))
    tax = Column("T$TAX", DECIMAL(10, 2))
    pric = Column("T$PRIC", DECIMAL(10, 2))
    ittl = Column("T$ITTL", DECIMAL(10, 2))
    meth = Column("T$METH", NUMBER)
    odis = Column("T$ODIS", DECIMAL(10, 2))
    idis = Column("T$IDIS", DECIMAL(10, 2))
    cpnc = Column("T$CPNC", String(CPNC_LEN))
    iqua = Column("T$IQUA", NUMBER)
    proc = Column("T$PROC", NUMBER)
    refcntd = Column("T$REFCNTD", NUMBER)
    refcntu = Column("T$REFCNTU", NUMBER)


class NetSuite404(Base):
    __tablename__ = "NetSuite404"

    ID_LEN = 11
    ORNO_LEN = 100
    GUID_LEN = 100
    ITEM_LEN = 100
    ITYP_LEN = 10
    PTYP_LEN = 10
    THEM_LEN = 100
    MORN_LEN = 9
    QNTY_LEN = 10
    SMIN_LEN = 10
    DSCA_LEN = 100
    SIZE_LEN = 100
    NAME_LEN = 100
    SRNO_LEN = 10
    SEQN_LEN = 10
    IDNO_LEN = 6
    EMNO_LEN = 7
    PDAT_LEN = 25
    NAMA_LEN = 50
    NAMC_LEN = 80
    NAMD_LEN = 80
    CITY_LEN = 50
    STATE_LEN = 2
    NAMF_LEN = 10
    CNTY_LEN = 50
    TELP_LEN = 15
    EMAIL_LEN = 100
    METH_LEN = 10
    CPNC_LEN = 50
    IQUA_LEN = 10

    id = Column("ID", INTEGER(ID_LEN), primary_key=True)
    orno = Column("NetsuiteOrder", String(ORNO_LEN))
    guid = Column("GUID", String(GUID_LEN))
    item = Column("ItemSku", String(ITEM_LEN))
    ityp = Column("ItemType", INTEGER(ITYP_LEN))
    ptyp = Column("PaperType", INTEGER(PTYP_LEN))
    them = Column("Theme", String(THEM_LEN))
    morn = Column("MagentoOrder", String(MORN_LEN))
    qnty = Column("InventoryItemQuantity", INTEGER(QNTY_LEN))
    smin = Column("SMINumber", INTEGER(SMIN_LEN))
    dsca = Column("Description", String(DSCA_LEN))
    size = Column("Size", String(SIZE_LEN))
    name = Column("StudentLastName", String(NAME_LEN))
    srno = Column("ServiceRequestNo", INTEGER(SRNO_LEN))
    seqn = Column("Sequence", INTEGER(SEQN_LEN))
    idno = Column("FamilyID", String(IDNO_LEN))
    emno = Column("SalesRep", String(EMNO_LEN))
    pdat = Column("ProcessDate", String(PDAT_LEN))
    nama = Column("AddressName", String(NAMA_LEN))
    namc = Column("Address1", String(NAMC_LEN))
    namd = Column("Address2", String(NAMD_LEN))
    city = Column("City", String(CITY_LEN))
    state = Column("State", String(STATE_LEN))
    namf = Column("Zip", String(NAMF_LEN))
    cnty = Column("Country", String(CNTY_LEN))
    telp = Column("Phone", String(TELP_LEN))
    email = Column("Email", String(EMAIL_LEN))
    odat = Column("OrderDate", DATE)
    totl = Column("OrderTotal", DECIMAL(15, 2))
    ship = Column("Shipping", DECIMAL(15, 2))
    tax = Column("SalesTax", DECIMAL(15, 2))
    pric = Column("ItemPrice", DECIMAL(15, 2))
    ittl = Column("InventoryItemTotal", DECIMAL(15, 2))
    meth = Column("ShippingMethod", INTEGER(METH_LEN))
    odis = Column("OrderDiscount", DECIMAL(15, 2))
    idis = Column("ItemDiscount", DECIMAL(15, 2))
    cpnc = Column("CouponCode", String(CPNC_LEN))
    iqua = Column("SalesItemQuantity", INTEGER(IQUA_LEN))



    # refcntd = Column("T$REFCNTD", INTEGER(REFCNTD_LEN))
    # refcntu = Column("T$REFCNTU", INTEGER(REFCNTU_LEN))