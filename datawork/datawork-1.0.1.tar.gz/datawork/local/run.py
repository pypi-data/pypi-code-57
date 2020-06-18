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
from multiprocessing import Manager, Queue, Lock
from multiprocessing.managers import BaseManager, SyncManager
# contrib
import ujson as json
import numpy as np

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

# call settings variables
from settings import GUI_STATIONS_BY_WORKER, GUI_WORKERS, GROUP, st_dict
from settings import host, gnsocket_port, user, nproc
from settings import (RDB_SOURCE_HOST, RDB_ENU_HOST)
from settings import (RDB_SOURCE_PORT, RDB_ENU_PORT)
from settings import (COLLECTOR_SOCKET_IP, COLLECTOR_SOCKET_PORT)
from settings import (DATAWORK_SOCKET_IP, DATAWORK_SOCKET_PORT)

# call scheduler engine datawork
from datawork import DragonGather
from datawork import DataManager


host_server = socket.gethostbyname(socket.gethostname())

AEventLoop = type(asyncio.get_event_loop())

parser = argparse.ArgumentParser(description="Obtener parámetros de operación")

parser.add_argument('--group',
                    help="Select the group of stations {0,1, 2, 3, ALL}",)
parser.add_argument('--workers',
                    type=int,
                    help="Select amount of workers to run with")
parser.add_argument('--eXw',
                    type=int,
                    help="Amount of stations by workers, to get data and process")

if __name__ == "__main__":
    args = parser.parse_args()
    workers = nproc
    if args.workers:
        workers = args.workers
    est_by_proc = GUI_STATIONS_BY_WORKER
    group = GROUP
    if args.group:
        if args.group.isdigit():
            group = int(args.group)
            if group in st_dict.keys():
                group = st_dict[group]
        else:
            if args.group in st_dict.keys():
                group = st_dict[args.group]
    if args.eXw:
        est_by_proc = args.eXw

    dt_status = "GROUP"
    dt_group = group

    # create a bridge to collector system, to connect GNCSocket
    dw_server_address = (DATAWORK_SOCKET_IP, DATAWORK_SOCKET_PORT)
    clean_port(DATAWORK_SOCKET_PORT)
    tsleep = 1
    # GNCSocket port
    port = gnsocket_port
    up = used_ports()
    [local_port, up] = get_port(up)
    collector_address = (COLLECTOR_SOCKET_IP, COLLECTOR_SOCKET_PORT)
    dt_status = "ALL"
    uin_p = 4
    nproc = nproc
    loop = asyncio.get_event_loop()
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

        # connect as client, available a server
        server_socket = GNCSocketServer(
           queue_n2t, queue_t2n, address=dw_server_address)
        print("Cliente ===================")
        print(collector_address)
        client_socket = GNCSocketClient(
           queue_client_n2t, queue_client_t2n, address=collector_address)
        enqueued = manager.list()

        kwargs.update({
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
            'rdb_address': (RDB_SOURCE_HOST, RDB_SOURCE_PORT),
            'rdb_enu_address': (RDB_ENU_HOST, RDB_SOURCE_PORT),
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

        mq_host = get_env_variable('MQ_HOST')
        mq_name = get_env_variable('MQ_NAME')
        mq_pass = get_env_variable('MQ_PASS')
        creds = (mq_name, mq_pass)
        mq_code = get_env_variable('MQ_CODE')
        mq_vhost = get_env_variable('MQ_VHOST')
        mq_queue_name = get_env_variable('MQ_QUEUE_NAME')

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
            'consumer_tag': 'enu_data'
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
            'consumer_tag': 'geojson'
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
            'consumer_tag': 'status_data'
        }

        amqp_options = manager.dict(
            data=amqp_data,
            status=amqp_status,
            earlybird=amqp_data_eb
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
