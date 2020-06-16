# same module
from basic_logtools.filelog import LogFile as FileLog
from .subscribe import SubscribeData
from .message import MessageManager
# stdlilb python
import datetime
import asyncio
from asyncio import shield, wait_for

import os
import socket
import functools
import concurrent.futures
import multiprocessing as mp
import time
from pathlib import Path
# contrib @dpineda
from networktools.time import timestamp, now
from networktools.colorprint import gprint, bprint, rprint
from networktools.library import my_random_string
from basic_queuetools.queue import read_queue_gen
from dataprotocols import Gsof, Eryo
from data_rdb import Rethink_DBS
from orm_collector.manager import SessionCollector, object_as_dict
from networktools.library import check_type

from networktools.library import (pattern_value,
                                  fill_pattern, context_split,
                                  gns_loads, gns_dumps)
from networktools.time import gps_time, now

# Tasktools
from tasktools.taskloop import coromask, renew, simple_fargs, simple_fargs_out
from tasktools.scheduler import TaskScheduler
# GSOF Protocol

# DBS Rethinkdb
from rethinkdb import RethinkDB

rdb = RethinkDB()

# base settings
try:
    from .conf.settings import COMMANDS, groups, dirs

except:
    from conf.settings import COMMANDS, groups, dirs


def load_stations(server_name, datadb, log_path='~/log'):
    print("Obteniendo estaciones....", server_name, datadb)
    dbmanager = SessionCollector(log_path=log_path, active='true', server=server_name, **datadb)
    u = dbmanager.get_station_data(server=server_name)
    print(u)
    dbmanager.close()
    return u


def load_databases(datadb, log_path='~/log'):
    print("Obteniendo datadb lista")
    dbmanager = SessionCollector(log_path=log_path, **datadb)
    u = dbmanager.get_dbdata_data()
    print("Resultado...", u)
    dbmanager.close()
    return u


def active_server(server_name, datadb, log_path='~/log'):
    print("Activando server", server_name, datadb)
    dbmanager = SessionCollector(log_path=log_path, **datadb)
    u = dbmanager.get_server_id(server_name)
    if u:
        dbmanager.active_server(u)
    dbmanager.close()
    return u


def deactive_server(server_name, datadb, log_path='~/log'):
    dbmanager = SessionCollector(log_path=log_path, **datadb)
    u = dbmanager.get_server_id(server_name)
    if u:
        dbmanager.deactive_server(u)
    dbmanager.close()
    return u


"""
Engine basic for collector
"""


class Aux:
    async def stop(self):
        pass


class Engine(TaskScheduler):
    """
    A class for data adquisition, receive meshttp://www.cursodeprogramacion.cl/sages from anageser and
    save data on db

    """
    log_manager = {}

    def __init__(self,
                 set_queue,
                 sleep_time,
                 est_by_proc,
                 stations,
                 enqueued,
                 dbtype,
                 protocol,
                 status_sta,
                 db_instances_sta,
                 status_conn,
                 db_data,
                 dump_list,
                 proc_tasks,
                 assigned_tasks,
                 free_ids,
                 wait,
                 inc_msg,
                 ids,
                 idd,
                 ipt,
                 idm,
                 ico,
                 gsof_timeout,
                 sta_init,
                 db_init,
                 db_connect,
                 status_tasks,
                 nproc,
                 idc,
                 rdb_address=None,
                 uin=8, *args, **kwargs):

        # init taskschduler
        self.server_name = kwargs.get('server', "atlas")
        self.log_path = Path(kwargs.get('log_path', '~/log'))
        self.timeout = kwargs.get("timeout", 5)
        self.datadb = kwargs.get("dbdata", {})        
        self.raise_timeout = kwargs.get("raise_timeout", False)
        args = []
        kwargs_extra = {
            'ipt': ipt,
            'ico': ico,
            'assigned_tasks': assigned_tasks,
            'nproc': nproc,
            'sta_init': sta_init
        }
        kwargs.update(kwargs_extra)
        super().__init__(*args, **kwargs)
        self.enqueued = enqueued
        #
        self.sep = '|'
        self.rq = set_queue[0]
        self.queue_n2t = self.rq
        self.wq = set_queue[1]
        self.queue_t2n = self.wq
        self.queue_process = set_queue[2]
        self.queue_ans_process = set_queue[3]
        self.time = sleep_time
        self.status_sta = status_sta
        self.status_tasks = status_tasks
        self.stations = stations
        self.dbtype = dbtype
        self.protocol = protocol
        self.instances = dict()
        self.db_instances_sta = db_instances_sta
        self.status_conn = status_conn
        self.db_data = db_data
        self.db_instances = dict()
        self.free_ids = free_ids
        self.wait = wait
        self.uin = uin
        self.folder = 'data'
        self.nproc = mp.cpu_count()
        # list of objects
        self.collect_objects = dict(
            GSOF=Gsof,
            ERYO=Eryo
        )
        self.database_objects = dict(
            RethinkDB=Rethink_DBS
        )
        self.dump_list = dump_list

        # LOAD DATA TO STATIONS
        self.tasks = dict()
        self.proc_tasks = proc_tasks
        self.status_tasks = status_tasks
        self.lnproc = est_by_proc
        self.inc_msg = inc_msg
        self.ids = ids
        self.idd = idd
        self.ipt = ipt
        self.ico = ico
        self.idm = idm
        self.first_time = dict()
        self.gsof_timeout = gsof_timeout
        self.rethinkdb_address = rdb_address
        self.rethinkdb = {}
        self.rethinkdb_address = rdb_address
        self.idc = idc  # dict shared
        self.dt_criteria = kwargs.get('dt_criteria',3)
        self.db_init = db_init
        self.db_connect = db_connect
        # set the main task
        coros_callback_dict = {
            'run_task': self.process_data,
        }
        # must be in every new process ATENTION!
        self.message_manager = MessageManager(self)
        self.subscribe_data = SubscribeData(
            'collector_subscribe', self.queue_t2n)
        self.LOG_STA = check_type(os.environ.get('LOG_STA', False))
        ###############################################
        self.set_new_run_task(**coros_callback_dict)
        self.server = active_server(self.server_name, self.datadb)

    def set_datafolder(self, folder):
        """
        Set another, different, folder to save data
        """
        self.folder = folder

    def set_id(self, lista):
        """
        Defines a new id for stations, check if exists
        """
        ids = my_random_string(self.uin)
        while True:
            if ids not in lista:
                lista.append(ids)
                break
            else:
                ids = my_random_string(self.uin)
        return ids

    def set_ids(self):
        """
        Defines a new id for stations, check if exists
        """
        return self.set_id(self.ids)

    def set_idd(self):
        """
        Defines a new id for stations, check if exists
        """
        return self.set_id(self.idd)

    def set_ipt(self):
        """
        Defines a new id for relation process-collect_task, check if exists
        """
        ipt = self.set_id(self.ipt)
        return ipt

    def set_ico(self):
        """
        Defines a new id for task related to collect data insice a worker, check if exists
        """
        return self.set_id(self.ico)

    def set_idm(self):
        """
        Defines a new id for relation incoming messages, check if exists
        """
        return self.set_id(self.idm)

    def load_stations(self):
        u = load_stations(self.server_name, self.datadb, log_path=self.log_path/"orm")  # ok
        for m in u:
            # print(m)
            keys = ['id', 'code', 'db', 'dblist', 'ECEF_X', 'ECEF_Y', 'protocol_host',
                    'ECEF_Z', 'port', 'protocol', 'host', 'dbname']
            try:
                station = dict(
                    id=m['id'],
                    code=m['st_code'],
                    name=m['st_name'],
                    ECEF_X=m['ecef_x'],
                    ECEF_Y=m['ecef_y'],
                    ECEF_Z=m['ecef_z'],
                    db=m['db_code'],
                    dblist=m['db_list'],
                    port=m['st_port'],
                    protocol=m['prt_name'],
                    protocol_host=m['protocol_host'],
                    host=m['st_host'],
                    on_db=True
                )
                (ids, sta) = self.add_station(**station)
                # print(station)
            except Exception as exc:
                raise exc

    def add_station(self, **sta):
        """
        Add station to list for data adquisition
        """
        try:
            keys = ['id',
                    'code',
                    'name',
                    'ECEF_X',
                    'ECEF_Y',
                    'ECEF_Z',
                    'host',
                    'port',
                    'interface_port',
                    'db',
                    'dblist',
                    'protocol',
                    'protocol_host',
                    'on_db',
                    'ipt']
            ids = self.set_ids()
            if ids in self.enqueued:
                self.enqueued.remove(ids)
            self.enqueued.append(ids)
            station = dict(ids=ids)

            for k in keys:
                if k in sta.keys():
                    if k == 'protocol':
                        station[k] = sta.get(k, 'None').upper()
                    else:
                        station[k] = sta.get(k, None)
                else:
                    if k == 'host':
                        station[k] = 'localhost'
                    elif k == 'port' or k == 'interface_port':
                        station[k] = 0
                    elif k == 'ECEF_X' or k == 'ECEF_Y' or k == 'ECEF_Z':
                        station[k] = 0
                    else:
                        station[k] = None
            self.stations.update({ids: station})
            self.status_sta.update({ids: False})
            self.first_time.update({ids: True})
            return (ids, sta)
        except Exception as ex:
            raise ex

    def get_stations_keys(self):
        return list(self.stations.keys())

    def load_databases(self):
        u = load_databases(self.datadb, log_path=self.log_path/"orm")  # ok
        for m in u:
            dbtype = m['type_name']
            kwargs = dict(
                id=m['id'],
                code=m['code'],
                path=m['path'],
                host=m['host'],
                port=m['port'],
                user=m['user'],
                passw=m['passw'],
                info=m['info'],
                type_name=m['type_name'],
                type_db=m['type_db'],
                url=m['url'],
                data_list=m['data_list'],
                dbname=m["dbname"].rstrip(),
                address=(m['host'], m['port']),
                log_path=self.log_path/"rdb",
                on_db=True)
            self.new_datadb(dbtype, **kwargs)

    def new_datadb(self, dbtype, **kwargs):
        """
        Here you give the argument for every type engine for store data colected
        and instantiate the db for enable query on that
        """
        # generate a idd= database instance identifier
        try:
            keys = [
                'id',
                'user',
                'passw',
                'code',
                'host',
                'port',
                'name',
                'path',
                'data_list',
                'type_name',
                'dbname',
                'type_db,'
                'url',
                'info',
                'address',
                'on_db',
                'log_path']
            uin = 4
            idd = self.set_idd()
            db_data = dict(idb=idd, name=dbtype, args={})
            for k in keys:
                if k in keys:
                    if k in kwargs.keys():
                        db_data['args'][k] = kwargs[k]
                    else:
                        if k == 'localhost':
                            db_data['args'][k] = 'localhost'
                        elif k == 'port':
                            db_data['args'][k] = 0
                        else:
                            db_data['args'][k] = ''
            self.db_data[idd] = db_data
            return idd, db_data
        except Exception as ex:
            raise ex

    def mod_station(self, ids, key, value):
        """
        Modify some value in station info

        """
        if key in self.stations.get(ids).keys():
            self.stations[ids][key] = value

    def del_station(self, ids):
        """
        Delete a station from list
        """
        del self.stations[ids]
        del self.status_sta[ids]
        del self.status_conn[ids]
        del self.instances[ids]
        k = self.ids.index(ids)
        del self.ids[k]

    def add_db_instance(self, ids, idd):
        """
        Create a new instance for ending database to save the raw data

        """
        try:
            if idd in self.db_data:
                self.db_data[idd]['args'].update(
                    {'address': self.rethinkdb_address,
                     'hostname': 'atlas'})
                name_db = self.db_data[idd]['name']
                object_db = self.database_objects[name_db]
                options = self.db_data[idd]['args']
                print("="*20)
                print(options)
                self.db_instances[idd] = object_db(**options)
                self.rethinkdb[ids] = False
                self.db_init[idd] = True
                self.db_connect[idd] = True
                if self.db_data[idd]['name'] == 'RethinkDB':
                    self.rethinkdb[ids] = True
                return self.db_instances[idd]
        except Exception as ex:
            print("Error creando instancia database %s" % format(self.db_data))
            raise ex

    def save_db(self, dbmanager, tname, args):
        """
        Save data to tname with args
        """
        # TODO: actualizar la lista de campos port table
        # TODO: añadir serverinstance
        input_args = dict(
            station=[
                'code',
                'name',
                'position_x',
                'position_y',
                'position_z',
                'host',
                'port',
                'interface_port',
                'db',
                'protocol'],
            dbdata=[
                'code',
                'path',
                'host',
                'port',
                'user',
                'passw',
                'info',
                'dbtype'],
            dbtype=['typedb', 'name', 'url', 'data_list'],
            protocol=['name', 'red_url', 'class_name', 'git_url']
        )
        name_args = input_args[tname]
        my_args = []
        id_instance = None
        if dbmanager == None:
            dbmanager = SessionCollector()
            instance = object
            if tname == 'station':
                instance = dbmanager.station(**args)
            elif tname == 'dbdata':
                instance = dbmanager.dbdata(**args)
            elif tname == 'dbtype':
                instance = dbmanager.dbtype(**args)
            elif tname == 'protocol':
                instance = dbmanager.protocol(**args)
            id_instance = instance.id
            return id_instance

    def save_station(self, ids):
        """
        Save station to database
        """
        # check if exists
        # if exist get data and compare
        # then update
        # if not, save
        pass

    def drop_station(self, ids):
        """
        Delete station from database
        """
        # get id from station ids
        # delete on database
        pass

    def del_db(self, varlist):
        """
        Delete element from database identified by idx in varlist
        """
        pass
###############

    def add_sta_instance(self, ids, loop):
        """
        Crear la instancia que accederá a los datos
        a través del socket
        """
        protocol = self.stations[ids]['protocol']
        kwargs = self.stations[ids]
        self.stations[ids].update({'on_collector': True})
        kwargs['code'] = self.stations[ids]['code']
        kwargs['host'] = self.stations[ids]['protocol_host']
        kwargs['port'] = self.stations[ids]['port']
        kwargs['sock'] = None
        kwargs['timeout'] = self.gsof_timeout
        kwargs["raise_timeout"] = False
        kwargs['loop'] = loop
        kwargs['log_path'] = self.log_path/"protocols"
        self.instances.update(
            {ids: self.collect_objects[protocol](**kwargs)})
        code = self.stations[ids]['code']
        code_db = self.stations[ids]['db']
        idd = self.get_id_by_code('DBDATA', code_db)
        args = []
        # activate engine to save date:
        if self.db_data[idd]['name'].upper() == 'TIMESERIE':
            # check if gsof
            folder = self.folder + "/" + idd
            args = [code, idd, folder, self.sep]

        self.db_instances_sta[ids] = idd
        self.first_time[ids] = True
        self.sta_init[ids] = True
        self.set_status_conn(ids, False)
        return self.instances[ids]

    def set_status_sta(self, ids, value):
        if isinstance(value, bool):
            self.status_sta[ids] = value
            # True: connect to sta
            # False: maintain status_conn01

    def set_status_conn(self, ids, value):
        if isinstance(value, bool):
            self.status_conn[ids] = value
            # True: connected
            # False: unconnected

    def del_sta(self, ids):
        del self.instances[ids]
        del self.status_sta[ids]
        del self.status_conn[ids]
        del self.first_time[ids]
        # del self.db_instances[ids]
        del self.ids

    def get_tname(self, varname):
        assert isinstance(varname, str)
        if varname == 'STA' or varname == 'STATION':
            return 'station'
        elif varname == 'DB' or varname == 'DBDATA':
            return 'database'
        elif varname == 'PROT' or varname == 'PROTOCOL':
            return 'protocol'
        elif varname == 'DBTYPE':
            return 'dbtype'
        else:
            return None

    def get_id_by_code(self, varname, code):
        if varname == 'STATIONS':
            this_var = self.stations
            for k in this_var.keys():
                if this_var[k]['code'] == code:
                    return k

        elif varname == 'DBDATA':
            this_var = self.db_data
            # variable in function dbtype
            for k in this_var.keys():
                # code_r=''
                try:
                    if this_var[k]['args']['code'] == code:
                        return k
                except Exception as ex:
                    raise ex

    def get_var(self, varname):
        varin = ''
        if varname == 'STA':
            varin = self.stations
        elif varname == 'DB':
            varin = self.db_data
        else:
            varin = None
        return varin

    async def connect(self, ids):
        if self.status_sta[ids]:
            await self.instances[ids].connect()
            self.set_status_conn(ids, True)
            self.set_status_sta(ids, False)
            self.first_time[ids] = False

    async def stop(self, ipt, ids):
        if self.status_sta[ids]:
            icos = [ico_dict for ipt, ico_dict in self.assigned_tasks.items()]
            ico_list = []
            for ico_dict in icos:
                ico_list += [ico for ico, _ids in ico_dict.items()
                             if _ids == ids]
            for ico in ico_list:
                self.unset_sta_assigned(ipt, ico, ids)
                instance_obj = self.instances.get(ids, Aux())
                await instance_obj.stop()
                self.set_status_conn(ids, False)
                self.set_status_sta(ids, False)

    async def reset_station_conn(self, sta_insta, ids, idc):
        self.set_status_sta(ids, False)
        self.set_status_conn(ids, False)
        self.first_time[ids] = True       
        v = 1
        if idc:
            await sta_insta.close(idc)
        await asyncio.sleep(10)
        return v

    def connect_to_sta(self, ids):
        return self.sta_init[ids] and not self.status_sta[ids] and not self.status_conn[ids] and self.first_time[ids]

    def is_connected(self, ids):
        return self.sta_init[ids] and self.status_sta[ids] and self.status_conn[ids] and not self.first_time[ids]        
    
    async def process_data(self, ipt, ids, *args, **kwargs):
        print(ipt,ids, args, kwargs)
        log = kwargs.get('log')
        v = int(args[0])
        data = args[1]
        sta_insta = data[0]
        db_insta = data[1]
        loop = asyncio.get_event_loop()
        code_db = self.stations.get(ids, {}).get('db')
        code = self.stations.get(ids, {}).get('code')
        idd = self.get_id_by_code('DBDATA', code_db)        
        code = None        
        #############
        # For some actions that modify status of
        # the variables on this coroutine
        self.free_ids[ids] = False
        while self.wait.get(ids, False):
            await asyncio.sleep(.01)
        if not self.status_sta[ids]:
            v = 1
        ##############
        """
        Si no se ha creado instancia de conexion a estación
        se crea

        sta_init un diccionario  {ids:bool}

        indice si la estación fue inicializada
        """        
        if not self.sta_init.get(ids):
            # step 0 initialize the objects, source and end
            try:
                gprint("Creando instancia collect para %s ids %s"%(code, ids))
                sta_insta = self.add_sta_instance(ids, loop)
                v += 1                
                log.info("Estación conectada->%s:%s" % (ids, code))
            except Exception as ex:
                log.exception(
                    "PD_00: Conexión de estación con falla ->%s:%s" % (ids, code))
                v = await self.reset_station_conn(sta_insta, ids, idc)
                kwargs["origin_exception"] = "PD_00 + %s" %code
                return [ipt, ids, v, (sta_insta, db_insta)], kwargs
        """
        Si no se ha creado la instanca de database:
        se crea la db instancia
        """
        """
        En caso que instancia de collect a estacion se haya iniciado
        1° conectar
        2° extraer datos
        """
        if self.connect_to_sta(ids):
            # step 1
            # si es primera vez de acceso
            # conectar al socket correspondiente
            # step 1.a connect and set flags to run data
            try:
                code = sta_insta.station                
                idc = None
                idc = await shield(sta_insta.connect())
                self.idc.update({ids: idc})
                self.set_status_sta(ids, True)
                self.set_status_conn(ids, True)
                self.first_time[ids] = False
            except asyncio.TimeoutError as e:
                log.exception("Tiempo fuera para conectar instancia de estación %s -> %s" %(code, db_insta))
                kwargs["origin_exception"] = "PD_T11_00 + %s" %code                                    
                v = await self.reset_station_conn(sta_insta, ids, idc)
                return [ipt, ids, v, (sta_insta, db_insta)], kwargs                                            
            except Exception as ex:
                rprint("Vuelta a reconectar")
                log.exception(
                    "PD_02: Error al conectar estación % s, ids %s, ipt  %s, %s" % (code, ids, ipt, ex))
                v = await self.reset_station_conn(sta_insta, ids, idc)
                kwargs["origin_exception"] = "PD_T12_00 + %s" %code                                                        
                return [ipt, ids, v, (sta_insta, db_insta)], kwargs                                           
            # si ya esta conectado :), obtener dato
        """
        Si ya está inicializado y conectad
        proceder a obtener datos
        """
        done = False
        msg_dict = {}
        sta_dict = {}
        if self.is_connected(ids):
            code = sta_insta.station
            idc = self.idc.get(ids)
            heartbeat = await sta_insta.heart_beat(idc)
            # just for checking
            if heartbeat:
                # step 1.b collect data and process to save the raw data
                try:
                    # set idc and header
                    set_header = wait_for(sta_insta.get_message_header(idc), timeout=self.timeout)
                    await shield(set_header)
                except asyncio.TimeoutError as e:
                    kwargs["origin_exception"] = "PD_T13_00 + %s" %code                                                            
                    log.exception("Tiempo fuera para setear header idc %s, estación %s , ids %s-> %s, error %s" %(idc, code, ids, sta_insta, e))
                    v = await self.reset_station_conn(sta_insta, ids, idc)
                    return [ipt, ids, v, (sta_insta, db_insta)], kwargs                                                                       
                except Exception as ex:
                    kwargs["origin_exception"] = "PD_T14_00 + %s" %code                                                            
                    log.exception(
                        "PD_03: Error al obtener mensaje de estación ids: %s, idc:  %s, code: %s, error %s" % (ids, idc, code, ex))
                    v = await self.reset_station_conn(sta_insta, ids, idc)
                    return [ipt, ids, v, (sta_insta, db_insta)], kwargs                                                                  
                # se inicia la lectura desde la fuente
                try:
                    get_records = wait_for(sta_insta.get_records(), timeout=self.timeout)
                    done, sta_dict = await shield(get_records)
                except asyncio.TimeoutError as e:
                    rprint("Error al obtener registros")
                    gprint("SE reinicia conexión a protocolo %s, %s, ids %s" %(sta_insta, sta_insta.class_name, ids))
                    kwargs["origin_exception"] = "PD_T15_00 + %s" %code                                                            
                    log.exception("Tiempo fuera, en get records idc %s, estación %s , ids %s-> %s, error %s" %(idc, code, ids, sta_insta, e))
                    v = await self.reset_station_conn(sta_insta, ids, idc)
                    return [ipt, ids, v, (sta_insta, db_insta)], kwargs                                                                       
                except Exception as ex:
                    kwargs["origin_exception"] = "PD_T16_00 + %s" %code                                                            
                    log.exception(
                        "PD_03: Error al obtener mensaje de estación, get records, ids: %s, idc:  %s, code: %s, error %s" % (ids, idc, code, ex))
                    v = await self.reset_station_conn(sta_insta, ids, idc)
                    return [ipt, ids, v, (sta_insta, db_insta)], kwargs                                                                  
                    
            else:
                rnow = now()
                kwargs["origin_exception"] = "PD99_00 + %s NO heartbeat" %code                                                        
                log.warning("PD_W00: IDS %s, Heart beat fails, %s at %s"%(ids, code, rnow))
                v = await self.reset_station_conn(sta_insta, ids, idc)                                                    
                data = [sta_insta, db_insta]
                return [ipt, ids, v, data], kwargs
                # rprint("Resultado de guardar ...%s" %result)
                    
        table_name = code_db
        if self.first_time[ids]:
            idd = self.db_instances_sta[ids]
            self.first_time[ids] = False
        else:
            idd = self.db_instances_sta[ids]
        """
        Procesar los datos
        """
        
        if done and sta_dict:
            # obtener idd de db, data ids
            dt0 = gps_time(sta_dict, sta_insta.tipo)
            dt_iso = rdb.iso8601(dt0.isoformat())
            rnow = now()
            recv_now = rdb.iso8601(rnow.isoformat())
            # print(rnow)
            delta = (rnow - dt0).total_seconds()
            sta_dict.update({
                'DT_GEN': dt_iso,
                'DT_RECV': recv_now,
                "DELTA_TIME": delta})
            # Control criteria
            if delta > self.dt_criteria:
                gprint("station %s :: Delta time %f, DT_GEN %s" %(code,delta, dt_iso))                                    
                rprint("station %s :: Delta time %f, DT_GEN %s" %(code,delta, dt_iso))                                    
                log.warning("Delta DT_RECV-DT_GEN>criterio(%f), DT_GEN %s, station %s"%(self.dt_criteria, dt_iso, code))

        """
        Crear instance de db
        """
        if not self.db_init.get(idd, False):
            db_insta = self.add_db_instance(ids, idd)
        """
        Conectar a database
        """
        if self.db_connect.get(idd):
            code = sta_insta.station            
            try:
                db_conn = wait_for(db_insta.async_connect(), timeout=10)
                conn = await shield(db_conn)
                log.info("Database conectada->%s:%s, idd:%s" % (
                    ids, code, idd))
                await db_insta.list_dbs()
                # create db if not exists
                print("Creando db on process data", db_insta.defaultdb)
                await db_insta.create_db(db_insta.defaultdb)
                # create table if not exists
                table_name = self.stations[ids]['db']
                result_create = await db_insta.create_table(table_name)
                await db_insta.create_index(table_name, index='DT_GEN')
                await db_insta.list_tables(db_insta.default_db)
                self.db_connect[idd] = False
            except asyncio.TimeoutError as e:
                log.exception("PD_TO1: Tiempo fuera para conectar db %s" %db_ins)
                db_insta.close()
                db_connect[idd]=True
                if self.raise_timeout:
                    raise e
                kwargs["origin_exception"] = "PD_TO1_00 + %s" %code                
                return [ipt, ids, v, (sta_insta, db_insta)], kwargs
               
            except Exception as ex:
                kwargs["origin_exception"] = "PD_TO2_00 + %s" %code
                db_insta.close()
                db_connect[idd]=True                        
                log.exception(
                    "PD_01: Excepción para conectar Rethinkdb, con falla -> %s: % s, did: % s" % (ids, code, idd))
                log.error("Falla del tipo %s"%ex)
                return [ipt, ids, v, (sta_insta, dn_insta)], kwargs
        """
        Guardar data en db
        """
        if done and self.db_init.get(idd) and not self.db_connect.get(idd):
           try:
               result = await db_insta.save_data(table_name, sta_dict)
           except Exception as ex:
               kwargs["origin_exception"] = "PD04_00 + %s" %code                                                                        
               log.exception(
                   "PD_04: Falla al guardar data...%s" % ex)
               # print("Databases %s tables %s" (
               #    await db_insta.list_dbs(),
               #    await db_insta.list_tables()))
               print("Error en levantar save_data rethink %s" % ex)
               db_ins.close()
               db_connect[idd]=True                        
               return [ipt, ids, v, (sta_insta, db_insta)], kwargs
        """
        Conclusión del cliclo
        esta tarea se termina. ... (por un momento)
        se preparan los parámetros de retorno

        Si todo va bien debería llegar hasta acá:
        """
        self.status_tasks[ids] = 'OFF'
        # [input, output] controls
        self.free_ids[ids] = True
        new_data = [sta_insta, db_insta]                        
        out = [ipt, ids, v, new_data]
        if not self.status_sta[ids]:
            v = 1
            out = [ipt, v, data]
        return out, kwargs

    async def status_proc_task(self, ipt, loop, ipt_result_dict):
        """
        Coroutine que chequea el status
        """
        log = self.log_manager[ipt]
        ids_list = self.proc_tasks[ipt]
        if len(ids_list) > 0:
            print("Recolectando %s" % format(ids_list))
        results_dict = {}
        for ids in ids_list:
            """
            Check stop queue
            """
            # print("Status to collect: %s "%self.status_task[ids])
            # bprint("Task %s in %s" % (format(self.stations[ids]), ipt))
            try:
                if ids not in ipt_result_dict.keys():
                    v = 1
                    args = [[ids, v], loop]
                    ipt_result_dict.update({ids: args})
                # args=[[ids,v],loop]
                args = ipt_result_dict[ids]
                result = await self.process_data(*args)
                self.tasks[ids] = result
                results_dict.update({ids: result})
            except Exception as ex:
                log.exception("Falla al registrar status, %s" % ex)
                raise ex
        # await asyncio.sleep(1)

        return [ipt, loop, results_dict]

    def check_iteration(self, maxv, task, coro):
        """
        Is a demo fn to create a hyperiteration and possible add new stations
        ->not impletented yet
        """
        result = task.result()
        value = result[0][1]
        if value <= maxv:
            renew(task, coro, simple_fargs_out)

    def set_init_args_kwargs(self, ipt):
        """
        This definition is for collector instance
        """
        log = FileLog("Engine@Collector", "CORE_%s" %
                      ipt, "localhost@pineiden", path=self.log_path/"engine")
        self.log_manager[ipt] = log
        return [ipt, 1, (None, None)], {"log": log}

    def set_pst(self, ids, args, kwargs):
        """
        This definition is for collector instance
        """
        return [args[0], ids, *args[1:]], kwargs

    def msg_network_task(self):
        # get from queue status
        # read_queue -> rq
        # process msg -> f(
        queue_list = [self.queue_n2t, self.queue_t2n]
        loop = asyncio.get_event_loop()
        try:
            args = [queue_list]
            kwargs = {}
            # Create instances
            task = loop.create_task(
                coromask(
                    self.check_status,
                    args, kwargs,
                    simple_fargs_out)
            )
            task.add_done_callback(
                functools.partial(
                    renew,
                    task,
                    self.check_status,
                    simple_fargs_out)
            )
            if not loop.is_running():
                loop.run_forever()
        except Exception as ex:
            print("Error o exception que se levanta con %s" %
                  format(queue_list))
            raise ex

    async def check_status(self, queue_list, *args, **kwargs):
        wq = queue_list[0]
        rq = queue_list[1]
        process = dict()
        idc = ""
        await asyncio.sleep(1)
        try:
            msg_from_source = []
            if not rq.empty():
                for i in range(rq.qsize()):
                    msg = rq.get()
                    # msg is a dict deserialized
                    msg_from_source.append(msg)
                    m = msg.get('dt', {})
                    idc = msg.get('idc', {})
                    if isinstance(msg, dict):
                        c_key = m.get('command').get('action')
                        if c_key in self.message_manager.commands.keys():
                            result = await self.message_manager.interpreter(m)
                            wq.put({'msg': result, 'idc': idc})
                        else:
                            wq.put({'msg': "Hemos recibido %s" % m, 'idc': idc})
                    else:
                        wq.put(
                            {'msg': "Es un mensaje que no es un comando de sistema %s" % msg,
                             'idc': idc})

            # bprint(self.instances.keys())
        except Exception as ex:
            raise ex
        return [queue_list, *args], kwargs
