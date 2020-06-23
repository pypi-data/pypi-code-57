#!/usr/bin/python
# coding: utf8

# Copyright 2019 Skiply

from __future__ import unicode_literals


from .base import db_session, SkiplyBase

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from skiply.cdm.associationContractService import AssociationContractService
from skiply.cdm.service import Service

import skiply.cdm.service


class Monitoring(SkiplyBase):
    ''' Device '''
    __tablename__ = 'so_monitoring'

    TYPE_CLASS_C = 'CLASS_C'
    TYPE_BATTERY = 'BATTERY'
    TYPE_NETWORK = 'NETWORK'
    TYPE_OTHER = 'OTHER'
    
    id = Column(Integer, primary_key=True, autoincrement=True)

    monitoring_type = Column('type', String(), default='OTHERS')
    monitoring_last_alert = Column('last_alert', DateTime())
    monitoring_quittance = Column('quittance', Boolean(), default=False)

    device_skiply_id = Column('devicename', String(), ForeignKey("so_boitier.devicename"))
    device_last_network_check = Column('last_network_check', String())

    #services = relationship('AssociationContractService', back_populates="contract")

    def __init__(self, device_skiply_id, monitoring_type=None, monitoring_last_alert=None, device_last_network_check=None, monitoring_quittance=False):#, service):
        self.monitoring_type = monitoring_type
        self.monitoring_last_alert = monitoring_last_alert
        self.monitoring_quittance = monitoring_quittance

        self.device_skiply_id = device_skiply_id
        self.device_last_network_check = monitoring_last_network_check

        #self.services = services

    def __repr__(self):
        return '<Monitoring %r - Alert %r>' % (self.device_skiply_id, self.monitoring_type)

    def update_monitoring_last_alert(new_monitoring_last_alert):
        session = db_session()
        try:
            if new_monitoring_last_alert != None:
                self.monitoring_last_alert = new_monitoring_last_alert
        except Exception as e:
            print("DB Request update_monitoring_last_alert(new_monitoring_last_alert) Failed with error : {}".format(e))
        finally:
            session.close()        

    def update_device_last_network_check(new_device_last_network_check):
        session = db_session()
        try:
            if new_device_last_network_check != None:
                self.device_last_network_check = new_device_last_network_check
        except Exception as e:
            print("DB Request update_device_last_network_check(new_monitoring_last_network_check) Failed with error : {}".format(e))
        finally:
            session.close()

def create_monitoring_alert(device_skiply_id, monitoring_type=None, monitoring_last_alert=None, monitoring_last_network_check=None, monitoring_quittance=False):
    session = db_session()
    try:
        results = Monitoring(device_skiply_id, monitoring_type, monitoring_last_alert, monitoring_last_network_check, monitoring_quittance)
        session.add(results)
        session.commit()
    except Exception as e:
        print("DB Request create_monitoring_alert(device_skiply_id, monitoring_type=None, monitoring_last_alert=None, monitoring_last_network_check=None, monitoring_quittance=False) Failed with error : {}".format(e))
        results=None
    finally:
        session.close()

    return results

def get_monitoring_alert(monitoring_id):
    session = db_session()
    try:
        results = session.query(Monitoring).filter(Monitoring.id == monitoring_id).first()
    except Exception as e:
        print("DB Request get_monitoring(monitoring_id) Failed with error : {}".format(e))
        results=None
    finally:
        session.close()

    return results

def get_monitoring_alerts():
    session = db_session()
    try:
        results = session.query(Monitoring).all()
    except Exception as e:
        print("DB Request get_monitoring_alerts() Failed with error : {}".format(e))
        results=None
    finally:
        session.close()

    return results

def get_monitoring_alerts_for_device(device_skiply_id):
    session = db_session()
    try:
        results = session.query(Monitoring).filter(Monitoring.device_skiply_id == device_skiply_id).all()
    except Exception as e:
        print("DB Request get_monitoring_for_device(device_skiply_id) Failed with error : {}".format(e))
        results=None
    finally:
        session.close()

    return results

def get_monitoring_alerts_for_devices(device_skiply_ids):
    session = db_session()
    try:
        results = session.query(Monitoring).filter(Monitoring.device_skiply_id.in_(device_skiply_ids)).all()
    except Exception as e:
        print("DB Request get_monitoring_for_device(device_skiply_id) Failed with error : {}".format(e))
        results=None
    finally:
        session.close()

    return results

def get_monitoring_alerts_last_alerts(hours_start=None, hours_end=None, limit=1000):
    session = db_session()
    try:
        if (hours_start != None) and (hours_end != None):
            results = session.query(Monitoring).filter(Monitoring.monitoring_last_alert >= hours_start, Monitoring.monitoring_last_alert < hours_end).order_by(Monitoring.monitoring_last_alert).limit(limit).all()
        else: 
            results = session.query(Monitoring).order_by(Monitoring.monitoring_last_alert).limit(limit).all()
    except Exception as e:
        print("DB Request get_contracts_for_services(service_ids) Failed with error : {}".format(e))
        results = None
    finally:
        session.close()

    return results
