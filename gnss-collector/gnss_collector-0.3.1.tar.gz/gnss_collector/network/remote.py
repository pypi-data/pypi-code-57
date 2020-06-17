from tasktools.taskloop import coromask, renew, simple_fargs
from multiprocessing import Manager
from collector.engine import Engine
from gnsocket.gn_socket import GNCSocket
from gnc.client_manager import GNCManager
import asyncio
import asyncssh
import functools
import concurrent.futures
import sys
import time
# import socket
# socket communication engine to terminal (user)

from termcolor import colored, cprint

def gprint(text):
    msg = colored(text, 'green', attrs=['reverse', 'blink'])
    print(msg)

def bprint(text):
    msg = colored(text, 'blue', attrs=['reverse', 'blink'])
    print(msg)

def rprint(text):
    msg = colored(text, 'red', attrs=['reverse', 'blink'])
    print(msg)


if __name__ == "__main__":
    executor=concurrent.futures.ProcessPoolExecutor()
    est_by_proc=2
    loop=asyncio.get_event_loop()
    manager=Manager()
    queue_n2t=manager.Queue()#network->terminal
    queue_t2n=manager.Queue()#terminal->network
    queue_process=manager.Queue()#terminal->network
    queue_ans_process=manager.Queue()#terminal->network
    #Manager dict to share betwen process
    stations=manager.dict()
    status_sta=manager.dict()
    instances=manager.dict()
    db_instances_sta=manager.dict()
    status_conn=manager.dict()
    db_data=manager.dict()
    db_instances=manager.dict()
    dump_list=manager.dict()
    tasks=manager.dict()
    proc_tasks=manager.dict()
    status_task=manager.dict()
    inc_msg=manager.dict()
    stime=1
    ids=manager.list()
    idd=manager.list()
    ipt=manager.list()
    idm=manager.list()
    engine=Engine(
        [queue_n2t, queue_t2n, queue_process, queue_ans_process],
        stime,
        loop,
        est_by_proc,
        stations,
        status_sta,
        db_instances_sta,
        status_conn,
        db_data,
        dump_list,
        proc_tasks,
        status_task,
        inc_msg,
        ids,
        idd,
        ipt,
        idm
    )
    NIPT=engine.nproc-2
    engine.load_stations()
    engine.load_databases()
    tasks=[]
    gs = GNCSocket(mode='server')
    tsleep=3
    async def sock_write(queue_t2n):
        queue=queue_t2n
        await asyncio.sleep(tsleep)
        try:
            print(queue.empty())
            if not queue.empty():
                for i in range(queue.qsize()):
                    msg_in = queue.get()
                    await gs.send_msg(msg_in)
                await gs.send_msg("<END>")
            else:
                pass
        except Exception as exec:
            raise exec

    # socket communication terminal to engine
    async def sock_read(queue_n2t):
        queue=queue_n2t
        msg_from_engine=[]
        await asyncio.sleep(tsleep)
        try:
            # read queue is answer from msg sended
            datagram = await gs.recv_msg()
            bprint(datagram)
            if not datagram == '' and \
               datagram != "<END>":
                queue.put(datagram)
        except Exception as exec:
            raise exec

    def socket_task():
        loop=asyncio.get_event_loop()
        gs.set_loop(loop)
        async def socket_io(reader, writer):
            queue_read=queue_n2t
            queue_write=queue_t2n
            await gs.set_reader_writer(reader, writer)
            #First time welcome
            welcome="Welcome to socket"
            rprint(welcome)
            await gs.send_msg(welcome)
            await gs.send_msg("<END>")
            #task reader
            try:
                args=[queue_read]
                task=loop.create_task(
                    coromask(
                        sock_read,
                        args,
                        simple_fargs)
                )
                task.add_done_callback(
                    functools.partial(
                        renew,
                        task,
                        sock_read,
                        simple_fargs)
                )
                args=[queue_write]
                #task write
                task=loop.create_task(
                    coromask(
                        sock_write,
                        args,
                        simple_fargs)
                )
                task.add_done_callback(
                    functools.partial(
                        renew,
                        task,
                        sock_write,
                        simple_fargs)
                )
            except Exception as exec:
                raise exec

        ########
        future=loop.create_task(gs.create_server(socket_io))
        if not loop.is_running():
            loop.run_forever()

    async def new_process(queue, queue_ans):
        loop=asyncio.get_event_loop()
        await asyncio.sleep(4)
        #read queue:
        msg_in=[]
        try:
            tasks=[]
            if not queue.empty():
                bprint("Nuevo proceso")
                bprint(engine.stations.keys())

                for i in range(queue.qsize()):
                    ids=queue.get()
                    bprint(ids)
                    engine.status_task[ids]='ON'
                    v=1
                    rprint("Is ids in list")
                    rprint(engine.stations.keys())
                    rprint(ids in engine.stations.keys())
                    if ids in engine.stations.keys():
                        #Si está vacio proc_task, crear nueva
                        gprint("Creando nuevo proceso")
                        #Si no está vacío hacer una lectura de disponibilidad
                        q=0
                        for ipt in engine.proc_tasks.keys():
                            bprint(engine.proc_tasks[ipt])
                            q+=1
                            bprint("Revisando tareas en procesador %s" % ipt)
                            if len(engine.proc_tasks[ipt])<engine.lnproc:
                                print("Añadiendo a procesador %s" % ipt)
                                engine.proc_tasks[ipt]+=[ids]
                                ans="TASK %s ADDED TO %s" % (ids, ipt)
                                break
                            else:
                                bprint("Procesadores trabajando a FULL")
                        bprint("Nuevo ipt: %s" % ipt)
                        queue_ans.put(ipt)
                queue.task_done()
                result=await asyncio.gather(*tasks)
                gprint(result)
                rprint("Procesadores-tareas")
                rprint(engine.proc_tasks.keys())
        except Exception as exec:
            gprint(exec)
            raise exec

    def new_process_task(queue,queue_ans):
        #task reader
        try:
            args=[queue, queue_ans]
            task=loop.create_task(
                coromask(
                    new_process,
                    args,
                    simple_fargs)
            )
            task.add_done_callback(
                functools.partial(
                    renew,
                    task,
                    new_process,
                    simple_fargs)
            )
        except Exception as exec:
            raise exec


    #new_process_task(queue_process)
    #loop.run_in_executor(
    #        executor,
    #        functools.partial(new_process_task,queue_process))
    # Generate communication socket tasks
    # Generate receptor task from communitacion
    # generate msg network receptor:
    loop.run_in_executor(
            executor,
            functools.partial(
                engine.msg_network_task,
                [queue_n2t,queue_t2n])
        )

    loop.run_in_executor(
            executor,
            socket_task
        )
    SK=list(engine.stations.keys())
    print(SK)
    tasks=[]
    LSK=len(SK)
    for ids in engine.stations.keys():
        gprint(ids)
        queue_process.put(ids)

    for i in range(NIPT):
        ipt=engine.set_ipt(3)
        v=1
        engine.proc_tasks[ipt]=[]
        loop.run_in_executor(
            executor,
            functools.partial(
                engine.collect_task,
                ipt,
                v
                )
            )
    
    print("Loop")
    bprint(engine.stations)
    bprint(engine.db_data)
    new_process_task(queue_process, queue_ans_process)    
    loop.run_forever()
    print("Done")

