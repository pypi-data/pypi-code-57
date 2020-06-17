from tasktools.taskloop import coromask, renew, simple_fargs
from tasktools.assignator import TaskAssignator
from networktools.environment import get_env_variable

from multiprocessing import Manager, Queue
from multiprocessing.managers import BaseManager
from gnss_collector.engine.engine import Engine, deactive_server
from gnsocket.gn_socket import GNCSocket
from gnsocket.socket_server import GNCSocketServer
import asyncio
import uvloop
import concurrent.futures
import sys
import time
import functools
import math
import adjustments
from adjustments import (COLLECTOR_SOCKET_IP, COLLECTOR_SOCKET_PORT, LOG_PATH, DATDB)
# import socket
# socket communication engine to terminal (user)

from networktools.colorprint import gprint, bprint, rprint
from networktools.ssh import clean_port
from pathlib import Path
import socket
import multiprocessing as mp


def socket_exception(ex, gs, idc):
    bprint("Excepción en socket")
    bprint(gs)
    rprint("Id socket client -> %s" % idc)
    raise ex

new_loop =uvloop.new_event_loop()
print("UVLOOP", new_loop, type(new_loop))

asyncio.set_event_loop(new_loop)

if __name__ == "__main__":
    cll_status = adjustments.cll_status
    cll_group = adjustments.cll_group
    workers = adjustments.workers
    nproc = adjustments.nproc
    tsleep = adjustments.tsleep
    gsof_timeout = adjustments.GSOF_TIMEOUT
    mp.set_start_method('spawn')

    # RerhinkDB Settings
    rdb_address = (adjustments.RDB_HOST, adjustments.RDB_PORT)

    if workers > nproc:
        workers = nproc
    with concurrent.futures.ProcessPoolExecutor(workers) as executor:
        address = (COLLECTOR_SOCKET_IP, COLLECTOR_SOCKET_PORT)
        clean_port(COLLECTOR_SOCKET_PORT)
        est_by_proc = adjustments.est_by_proc
        loop = asyncio.get_event_loop()
        manager = Manager()
        # terminal->network
        queue_process = manager.Queue()
        # terminal->network
        queue_ans_process = manager.Queue()
        # terminal->network
        # Manager dict to share betwen process
        stations = manager.dict()
        wait = manager.dict()
        enqueued = manager.list()
        dbtype = manager.dict()
        protocol = manager.dict()
        protocols = manager.dict()
        dbtypes = manager.dict()
        status_sta = manager.dict()
        instances = manager.dict()
        db_instances_sta = manager.dict()
        status_conn = manager.dict()
        db_data = manager.dict()
        db_instances = manager.dict()
        dump_list = manager.dict()
        tasks = manager.dict()
        proc_tasks = manager.dict()
        sta_init = manager.dict()
        db_init = manager.dict()
        db_connect = manager.dict()                
        assigned_tasks = manager.dict()
        inc_msg = manager.dict()
        status_tasks = manager.dict()
        free_ids = manager.dict()
        stime = 1
        ids = manager.list()
        idd = manager.list()
        ipt = manager.list()
        idm = manager.list()
        ico = manager.list()
        idc = manager.dict()
        ##
        locker = manager.Lock()
        # create scheduler subclass
        queue_n2t = manager.Queue()
        # network->terminal
        queue_t2n = manager.Queue()
        server_name = get_env_variable('SERVER_NAME')
        kwargs = {
            'server': server_name,
            'log_path': LOG_PATH,
            'dt_criteria':10,
            "timeout":15,
            "raise_timeout":False,
            'datadb':DATADB
        }
        queue_list = [queue_n2t,
                      queue_t2n,
                      queue_process,
                      queue_ans_process, ]
        engine = Engine(
            queue_list,
            stime,
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
            rdb_address,
            8,
            **kwargs
        )
        NIPT = workers-3

        # activate new assignator
        sta_asssigned = []
        assignator = TaskAssignator(
            engine,
            queue_process,
            queue_ans_process,
            assigned_tasks,
            cll_status,
            cll_group,
            enqueued,
            locker)

        try:
            engine.load_stations()
            engine.load_databases()
        except Exception as e:
            print("Falla en cargar datos desde db %s" % e)
            raise e
        tasks = []

        #################
        #  Here there are in use 2 process
        ###################

        try:
            loop.run_in_executor(
                executor,
                engine.msg_network_task
            )
        except Exception as ex:
            print("Falla encargar networktask")
            raise ex
        opts = {
            "timeout":10,
            "raise_timeout":False, 
            'server': server_name,
            'log_path': Path(LOG_PATH)/"gnsocket_server",
        }
        server_socket = GNCSocketServer(
            queue_n2t, queue_t2n, address=address,
            callback_exception=socket_exception, **opts)
        try:
            loop.run_in_executor(
                executor,
                server_socket.socket_task
            )
        except Exception as ex:
            print("Falla en cargar socket task")
            raise ex

        ######

        ######

        SK = list(engine.stations.keys())
        tasks = []
        LSK = len(SK)
        for ids, sta in engine.stations.items():
            print("Station", sta.get('code'), ids)
            try:
                queue_process.put(ids)
            except Exception as exc:
                print("Error al cargar en cola %s " % exc)

        # Inicializa Assignator

        loop.run_in_executor(executor, assignator.new_process_task)

        ####
        # Here we use the another (the rest) of the processors
        ####
        for i in range(NIPT):
            try:
                # time.sleep(tsleep)
                ipt = engine.set_ipt()
                v = 1
                # se inicializa lista de proc_task
                engine.proc_tasks[ipt] = []
                try:
                    tipt = loop.run_in_executor(
                        executor,
                        functools.partial(
                            engine.manage_tasks,
                            ipt))
                    gprint("ID ipt->%s" % tipt)
                except Exception as exc:
                    print("Error al activar nueva cpu")
                    print(exc)
                    raise exc
            except Exception as exc:
                print("Error al cargar en executor %s erro: $s" % (ipt, exc))
                raise exc
        try:
            loop.run_forever()
        except Exception as exc:
            deactive_server(server_name)
            engine.exception("Detener log")
            print("Error al inicializar loop, error: $s" % (exc))
            raise exc

        print("Done")
