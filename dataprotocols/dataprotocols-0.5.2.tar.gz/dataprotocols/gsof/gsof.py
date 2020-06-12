from struct import unpack
import socket
from asyncio import shield
import asyncio
import math
import errno
from functools import reduce

import sys
import time
import datetime

from pathlib import Path
import os
from basic_logtools.filelog import LogFile

from networktools.time import timestamp, now
from networktools.library import my_random_string

from networktools.colorprint import rprint, bprint

from dataprotocols import BaseProtocol

'''
###############################################################################
CLASE GSOF  __authors__ = "Henry T. Berglund ----> David Pineda"
###############################################################################
Conexion TCP/IP con un determinado receptor.
Updated to python3.5 by David Pineda @pineiden dpineda@csn.uchile.cl

'''

try:
    from .gsof_settings import gsof_field_names, gsof_rec, gsof_table_names, logfile
except Exception:
    from gsof_settings import gsof_field_names, gsof_rec, gsof_table_names, logfile

def checksum256(data_check):
    """Calculate checksum"""
    # ord: string -> unicode int
    # map(a,b): opera a en b
    # list entrega lista o arrays
     #formula: 	(Status + type + length + data bytes) modulo 256
    data_bytes = data_check.get("DATA_BYTES")
    checksum = data_check.get("CHECKSUM")
    chk256  = sum(data_bytes) % 256
    return  checksum == chk256

class Gsof(BaseProtocol):
    """ Class to connect to tcp port and parse GSOF messages """
    tipo = "GSOF"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg_0 = None
        self.msg_bytes = None
        self.rec_dict = {}
        self.batt_status = 0
        self.tables = gsof_table_names
        # manage asyncronous clients


    async def get_message_header(self, idc):
        # receive data from source
        # max amount of data
        # N ammount of bites
        self.data_check = {}
        reader = self.clients[idc]['reader']
        writer = self.clients[idc]['writer']
        self.timestamp = timestamp()
        BytesData = 7
        bufsize = BytesData
        msg_field_names = ('STX', 'STATUS', 'TYPE', 'LENGTH',
                           'T_NUM', 'PAGE_INDEX', 'MAX_PAGE_INDEX')

        try:
            if writer.transport.is_closing():
                self.logger.error("La conexión se cerró %s" % writer)
                self.status = False
                raise Exception("Conexión perdida para idc %s station %s" %(idc, self.station))
            data = None

            try:
                data = await shield(self.readbytes(reader, bufsize))
                self.msg_dict = dict(zip(
                    msg_field_names,
                    unpack('>' + str(bufsize) + 'B', data)))
                campos_unpack =unpack('>%dB'%bufsize, data)
                self.msg_dict = dict(zip(msg_field_names, campos_unpack))
                status = self.msg_dict['STATUS']
                bin_status = bin(status)
                batt_status = bin_status[3]
                self.msg_dict["LOW_BATTERY"] = bool(int(batt_status))
                self.msg_bytes = await shield(self.readbytes(reader,self.msg_dict['LENGTH']-3))
                self.msg_0 = self.msg_bytes
                n = 2
                check_etx =  await shield(self.readbytes(reader, n))
                (checksum, etx) = unpack('>2B', check_etx)
                self.data_check["CHECKSUM"] = checksum                
                self.data_check["DATA_BYTES"] = list(self.msg_bytes+data[1:])
                self.checksum = checksum256(self.data_check)
                self.msg_dict["CHECKED"] = self.checksum
            except asyncio.TimeoutError as te:
                self.logger.exception("Get message TimeoutError, %s"%te)
                return False
            except asyncio.IncompleteReadError as ir:
                print("Incomplete read on set header", reader, n)
                self.logger.exception("Station %s, Tiempo fuera al no poder leer en readbytes %s bytes, %s"%(n, self.station,ir))
                return False
            except socket.timeout as timeout:
                self.logger.exception(
                    "La conexión se cerró, socket timeout %s, STATION %S" % (timeout, self.station))
                self.on_blocking()
                self.logger.exception("Esperando mucho tiempo")
                self.status = False
                return False
            except Exception as ex:
                print("Escepcion as ex: %s" %ex)
                self.logger.exception(
                    "La conexión se cerró, error en comunicación %s" % ex)
                await self.close(idc)
                self.on_blocking()
                info = "Error %s en estación %s. Encabezado con data %s" % (
                    ex, self.station, data)
                print(info)
                self.logger.info(info)
                self.logger.error(ex)
                self.status = False
                return False
            return True

        except asyncio.IncompleteReadError as e:
            self.logger.exception("Error de mensaje incompleto %s" % e)
            self.logger.error(
                "Error de mensaje esperado en n bytes %s" % e.expected)
            self.logger.error("Error de mensaje recibido %s" % e.partial)
            raise e

        except socket.timeout:
            self.close()
            self.sock = self.create_socket(None)
            self.on_blocking()
            raise socket.timeout

        except socket.error as ex:
            self.close()
            print("Error de conexión %s error %s" % (self.station, ex))
            self.logger.error(ex)
            self.sock = self.create_socket(None)
            self.on_blocking()
            raise ex

    async def get_records(self):
        msg = {}        
        while self.msg_bytes:
            # READ THE FIRST TWO BYTES FROM RECORD HEADER
            try:
                record_type, record_length = unpack('>2B', self.msg_bytes[0:2])
            except Exception as ex:
                self.status = False
                qex = "Error %s en estación %s, tabla %s" % (
                    ex, self.station, 'Header')
                self.logger.debug(qex)
                return False, {}
            self.msg_bytes = self.msg_bytes[2:]
            try:
                msg_table = self.select_record(record_type, record_length)
                msg.update(msg_table)
            except Exception as ex:
                self.status = False
                self.logger.error(ex)
                print("No hay mensaje que traducir")
                self.logger.error("Desconectando debido a error en mensaje")
                self.logger.error(
                    "Reconectando debido a error en mensaje, luego de desconexión")
                self.on_blocking()
                return False, {}
        msg["HEADER"] = self.msg_dict
        done = self.checksum
        return done, msg

    def select_record(self, record_type, record_length):
        field_names = gsof_field_names
        rec_input = gsof_rec
        msg = []
        table_name = self.tables.get(record_type)
        timestamp = self.timestamp
        try:
            rec_field_names = field_names.get(record_type)
            if not record_type in [13, 14, 33, 48] and record_type in field_names.keys():
                # print("Base recibida")
                try:
                    rec_values = unpack(
                        rec_input[record_type], self.msg_bytes[:record_length])
                    msg = dict(list(zip(rec_field_names, rec_values)))
                    msg['TIMESTAMP'] = timestamp
                    self.rec_dict.update({table_name: msg})
                    self.msg_bytes = self.msg_bytes[record_length:]
                except Exception as ex:
                    self.status = False
                    self.logger.exception("Error al hacer unpack",ex)
                    raise ex

            elif record_type in [13, 14, 33, 48] and record_type in field_names.keys():
                L = len(self.msg_bytes)-1
                bNUM = self.msg_bytes[0:1]
                try:
                    code = rec_input[record_type][0]
                    NUM_OF_SVS = unpack(code, bNUM)  # char-> pass to int
                except Exception as ex:
                    self.status = False
                    qex = "Error %s en estación %s, tabla %s" % (
                        ex, self.station, record_type)
                    self.logger.exception(qex)
                    raise ex
                u = int(L/NUM_OF_SVS[0])
                # Acortar el NSVS quitando primer byte
                self.msg_bytes = self.msg_bytes[1:]
                # for field in range(len(rec_field_names)):
                #    self.rec_dict[rec_field_names[field]] = []
                for sat in range(NUM_OF_SVS[0]):
                    try:
                        code = rec_input[record_type][1]
                        rec_values = unpack(
                            code, self.msg_bytes[0:u])  # why [0:10]
                        msg_k = dict(list(zip(rec_field_names, rec_values)))
                        msg_k['TIMESTAMP'] = timestamp
                        msg.append(msg_k)
                    except Exception as ex:
                        self.status = False
                        self.logger.debug(ex)
                        raise ex
                    self.msg_bytes = self.msg_bytes[u:]
                    tname = table_name+"_"+str(sat)
                    self.rec_dict.update({table_name: msg})
            else:
                """Unknown record type? Skip it for now!"""
                # print record_type
                msg = self.msg_bytes[record_length + 2:]
                self.msg_bytes = self.msg_bytes[record_length + 2:]
        except Exception as ex:
            self.status = False
            raise ex
        return {table_name: msg}


