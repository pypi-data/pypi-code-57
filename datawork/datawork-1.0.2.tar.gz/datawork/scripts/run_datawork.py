#!/usr/bin/env python

# standar library
import os
import sys
import subprocess
import socket
import shlex
import asyncio
import concurrent.futures
import time
import functools
import math
import argparse
from ctypes import c_bool
import multiprocessing as mp
from multiprocessing import Manager, Queue, Lock
from multiprocessing.managers import BaseManager, SyncManager
from pathlib import Path
# contrib
import ujson as json
import numpy as np
import uvloop
import click

# module tasktools
from tasktools.taskloop import coromask, renew, simple_fargs
from tasktools.assignator import TaskAssignator

# module networktools
from networktools.colorprint import gprint, bprint, rprint
from networktools.environment import get_env_variable
from networktools.ports import used_ports, get_port
from networktools.ssh import bridge, kill, clean_port
from networktools.library import pattern_value, \
    fill_pattern, context_split, \
    gns_loads, gns_dumps
from networktools.environment import get_env_variable

# module GNCSocket
# Implemente socket with this class better
# from gnsocket.server import GNSocketServer
from gnsocket.socket_server import GNCSocketServer
from gnsocket.socket_client import GNCSocketClient

# call scheduler engine datawork
from datawork import DragonGather
from datawork import DataManager
from datawork.scripts import EnvData
# leer archivo de configuración

def get_conf_data(conf):
    keys = ['DATAWORK_EST_X_PROC', 'DATAWORK_TSLEEP',
            'DATAWORK_WORKERS', 'DW_STATUS', 'DW_GROUP',
            'SELECT_GROUP', 'COLLECTOR_SOCKET_IP', 'COLLECTOR_SOCKET_PORT',
            'DATAWORK_SOCKET_IP', 'DATAWORK_SOCKET_PORT', 'RDB_SOURCE_HOST',
            'RDB_SOURCE_PORT', 'RDB_ENU_HOST', 'RDB_ENU_PORT', 'MQ_HOST',
            'MQ_NAME', 'MQ_PASS', 'MQ_VHOST', 'MQ_CODE', 'MQ_QUEUE_NAME']
    json_file = re.compile("\.json$")
    dbdata = {}
    if json_file.search(conf):
        file_path=Path(conf)
        if file_path.exists():
            with open(file_path,'r') as f:
                dbdata = json.load(f)
            if all(filter(lambda k: k in dbdata,keys)):
                return dbdata
            else:
                print("A tu archivo le falta una llave, revisa si tiene %s" %keys)
        else:
            print("Tu archivo json no existe en la ruta especificada: %s" %file_path)
            print("Debe ser así:")
            this_path = Path(__file__).parent
            example_path = this_path/"collector_example.json"
            if example_path.exists():
                with open(example_path,'r') as f:
                    print("{")
                    [print(k,":",v) for k,v in json.load(f).items()]
                    print("}")
            else:
                print("El archivo de ejemplo no existe, lo siento, escribe a dpineda@uchile.cl consultando")
    else:
        print("Tu archivo json debe tener una extensión json y una ruta correcta: pusiste  <%s>" %conf)
        print("Archivo json debe ser así:")
        this_path = Path(__file__).parent
        example_path = this_path/"datawork_example.json"
        if example_path.exists():
            with open(example_path,'r') as f:
                print("{")
                [print("    %s:\"%s\","%(k,v)) for k,v in json.load(f).items()]
                print("}")
        else:
            print("El archivo de ejemplo no existe, lo siento, escribe a dpineda@uchile.cl consultando")
    return dbdata

"""
fn to start datawork

"""

def start_datawork(env, conf="collector_example.json"):
    new_loop =uvloop.new_event_loop()
    asyncio.set_event_loop(new_loop)
    mp.set_start_method('spawn')
    loop = asyncio.get_event_loop()    
    data = {}
    if env:
        env_data = EnvData()
        data = env_data.json
        clean_port(env_data.DATAWORK_SOCKET_PORT)
    else:
        data = get_conf_data(conf)
        clean_port(data.get("DATAWORK_SOCKET_PORT"))

    workers = int(data.get("DATAWORK_WORKERS"))
    est_by_proc = data.get("DATAWORK_EST_X_PROC")
    dt_status = data.get("DW_STATUS")
    dt_group = data.get("DW_GROUP")
    # create a bridge to collector system, to connect GNCSocket
    dw_server_address = tuple(
        map(
            lambda key:data.get(key),
            ("DATAWORK_SOCKET_IP", "DATAWORK_SOCKET_PORT")
        )
    )
    tsleep = 1
    collector_address =  tuple(
        map(
            lambda key:data.get(key),
            ("COLLECTOR_SOCKET_IP", "COLLECTOR_SOCKET_PORT")
        )
    )
    nproc = int(data.get("NPROC"))

    mq_host = data.get('MQ_HOST')
    mq_name = data.get('MQ_NAME')
    mq_pass = data.get('MQ_PASS')
    creds = (mq_name, mq_pass)
    mq_code = data.get('MQ_CODE')
    mq_vhost = data.get('MQ_VHOST')
    mq_queue_name = data.get('MQ_QUEUE_NAME')

    print("Cantidad workers :", workers, type(workers))
     
    with concurrent.futures.ProcessPoolExecutor(workers) as executor:
        manager = Manager()
        sta_assigned = manager.dict()
        ipt = manager.list()
        ico = manager.list()
        # SOCKET SERVER network->terminal
        queue_n2t = manager.Queue()
        queue_t2n = manager.Queue()
        # SOCKET CLIETN network->terminal
        queue_client_n2t = manager.Queue()
        queue_client_t2n = manager.Queue()
        queue2client = manager.Queue()
        #
        queue_list = [queue_n2t, queue_t2n]
        # terminal->network
        process_queue = manager.Queue()
        stations_queue = manager.Queue()
        dbus_geojson_queue = manager.Queue()
        tasks_queue = manager.Queue()
        ans_queue = manager.Queue()
        dbus_queue = manager.Queue()
        proc_tasks = manager.dict()
        assigned_tasks = manager.dict()
        stations = manager.dict()
        position = manager.dict()
        db_data = manager.dict()
        sta_init = manager.dict()
        gui_group = manager.dict()

        kwargs = dict()
        status_tasks = manager.dict()

        # list of process identificators
        proc_tasks = manager.dict()
        signals = manager.dict()

        # create gui queue
        gui_queue = manager.Queue()
        gui_set = manager.list()
        log_path = Path(data.get("LOG_PATH"),"~/datawork_log")

        # connect as client, available a server
        server_socket = GNCSocketServer(
            queue_n2t, queue_t2n, address=dw_server_address, log_path=str(log_path/"socket_server"))
        print("Cliente ===================")
        print(collector_address)
        client_socket = GNCSocketClient(
           queue_client_n2t, queue_client_t2n, address=collector_address, log_path=str(log_path/"socket_client"))
        enqueued = manager.list()
        kwargs.update({
            "log_path":data.get("LOG_PATH"),
            'enqueued': enqueued,
            'ipt': ipt,
            'ico': ico,
            'queue_client_n2t': queue_client_n2t,
            'queue_client_t2n': queue_client_t2n,
            'queue2client': queue2client,
            'stations': stations,
            'position': position,
            'db_data': db_data,
            'proc_tasks': proc_tasks,
            'nproc': nproc,
            'sta_init': sta_init,
            'bridge': bridge,
            'status_tasks': status_tasks,
            'assigned_tasks': assigned_tasks,
            'rdb_address': tuple(map(data.get,("RDB_SOURCE_HOST", "RDB_SOURCE_PORT"))),
            'rdb_enu_address': tuple(map(data.get,("RDB_ENU_HOST", "RDB_ENU_PORT"))),
            'rdb_dbname': 'collector',
            'chart': 'gnss_graph',
            'gui_set': gui_set,
            'gui_queue': gui_queue,
            'process_queue': process_queue,
            'signals': signals,
            'isg': manager.list(),
            'sigid': manager.list(),
            'group': dt_group,  # Specifi group
            'gui_group': gui_group,  # gui_group
            'dbus_queue': dbus_queue,
            'dbus_geojson_queue': dbus_geojson_queue,
            # if start collect data from rethindb is controled by gui
            'send_control': manager.Value(c_bool, True),
            'type_bus': 'session', })

        locker = manager.Lock()
        queue_ans_process = manager.Queue()
        # create new scheduler
        gather = DragonGather(queue_list, **kwargs)
        # assign scheduler yo assignator
        assignator = TaskAssignator(
            gather,
            process_queue,
            queue_ans_process,
            sta_assigned,
            dt_status,
            dt_group,
            enqueued,
            locker)

        """
        'code': 'gfast',
            'vhost': 'gfast',
            'host': mq_host,
            'credentials': creds,
            'qname': 'datawork2gfast',
        """
        amqp_data = {
            'amqp': True,
            'code': "enu_data",
            'vhost': mq_vhost,
            'host': mq_host,
            'credentials': creds,
            'queue_name': "geo_enu_data",
            'routing_key': 'data',
            'durable': False,
            'consumer_tag': 'enu_data',
            "log_path":str(log_path/"amqp_data")                        
        }
        amqp_data_eb = {
            'amqp': True,
            'code': "earlybird",
            'vhost': mq_vhost,
            'host': mq_host,
            'credentials': creds,
            'queue_name': "earlybird",
            'routing_key': 'earlybird',
            'exchange': 'earlybird',            
            'durable': False,
            'consumer_tag': 'geojson',
            "log_path":str(log_path/"amqp_earlybird")            
        }        
        amqp_status = {
            'amqp': True,
            'code': 'status',
            'vhost': mq_vhost,
            'host': mq_host,
            'credentials': creds,
            'queue_name': 'status_gnss',
            'routing_key': 'status',
            'exchange': 'status_exchange',
            'durable': True,
            'consumer_tag': 'status_data',
            "log_path":str(log_path/"amqp_status")                        
        }

        amqp_options = manager.dict(
            data=amqp_data,
            status=amqp_status,
            earlybird=amqp_data_eb,
        )

        signal_geojson = DataManager(dbus_geojson_queue, amqp_options)

        tasks_list = []

        # signal task

        # second process -> tasks asignment

        signal_geojsontask = loop.run_in_executor(
            executor,
            signal_geojson.task_cycle)

        tasks_list.append(signal_geojsontask)

        # second process -> tasks asignment

        # Task on gather to process messages RPC
        # Active client SOCKET connected with Collector

        networktask = loop.run_in_executor(
            executor,
            gather.msg_network_task
        )
        tasks_list.append(networktask)

        # Task to receive on socket messages from outside
        try:
            socket_client_task = loop.run_in_executor(
                executor,
                client_socket.socket_task
            )
            pass
        except Exception as e:
            print("Falla en cargar socket task CLIENT")
            raise e

        tasks_list.append(socket_client_task)

        try:
            socket_task = loop.run_in_executor(
                executor,
                server_socket.socket_task
            )
            pass
        except Exception as e:
            print("Falla en cargar socket task SERVER")
            raise e

        tasks_list.append(socket_task)

        """

        socket_task ---> networktask
        A ---> B
        A sends to B using queues a message

        """
        NIPT = workers-5  # Workers avalaible

        bprint("###"*20)
        bprint("#=#"*20)
        print("TOTAL NIPT %s / workers %s" % (NIPT, workers))
        bprint("#=#"*20)
        bprint("###"*20)

        for i in range(NIPT):
            # time.sleep(1)
            ipt = gather.set_ipt(4)
            gather.proc_tasks[ipt] = []
            # problem here for python v3.6>
            task_process = loop.run_in_executor(
                executor,
                functools.partial(
                    gather.manage_tasks,
                    ipt))
            tasks_list.append(task_process)

        tasks_list.append(assignator.new_process_task())
        bprint("Iniciando tareas")
        loop.run_until_complete(asyncio.gather(*tasks_list))




@click.command()
@click.option("--name", default="datawork", show_default=True, help="Nombre de la instancia datawork a crear")
@click.option("--env_vars/--no-env_vars", default=True, show_default=True,  type=bool, help="Para mostrar el nombre de las variables de ambiente" )
@click.option("--env/--no-env", default=True, show_default=True,  type=bool, required=True,help="Si obtener los datos de ambiente o cargarlos de un json o data entregada")
@click.option("--conf", default="JSON FILE",  show_default=True, help="Archivo json con los parámetros de configuración")
def run_datawork(name, env_vars, env, conf):
    print("Iniciando servicio COLLECTOR para %s" %name.upper())
    if env and env_vars:
        envvar = EnvData()
        envvar.show()
    start_datawork(env, conf)

if __name__ == "__main__":
    run_datawork()
