import socket
from basic_queuetools.queue import read_queue_gen
from gnsocket.gn_socket import GNCSocket
# Standar lib
import asyncio
import functools
from multiprocessing import Manager, Queue, Lock

# contrib modules
import ujson as json

# Own module
from gnsocket.gn_socket import GNCSocket
from gnsocket.exceptions import clean_exception

# module tasktools
from tasktools.taskloop import coromask, renew, simple_fargs
from networktools.colorprint import gprint, bprint, rprint

from networktools.library import pattern_value, \
    fill_pattern, context_split, \
    gns_loads, gns_dumps
from networktools.library import my_random_string
from asyncio import shield

import ujson as json

tsleep = 2


class GNCSocketBase:

    def __init__(self, queue_n2t,
                 queue_t2n,
                 mode,
                 callback_exception=clean_exception,
                 *args,
                 **kwargs):
        self.qn2t = queue_n2t
        self.qt2n = queue_t2n
        self.address = kwargs.get('address', ('localhost', 6666))
        self.log_path = kwargs.get('log_path', '~/gnsocket_log')        
        self.mode = mode
        self.exception = callback_exception
        self.timeout = kwargs.get("timeout", 5)
        self.raise_timeout =  kwargs.get("raise_timeout", False)

    async def sock_write(self, gs, idc, *args, **kwargs):
        queue = self.qn2t
        await asyncio.sleep(.5)
        if idc in gs.clients:
            try:
                heartbeat = await gs.heart_beat(idc) 
                if heartbeat:
                    for msg in read_queue_gen(queue):
                        msg_send = json.dumps(msg)
                        idc_server = msg.get('idc_server')
                        send_msg = asyncio.wait_for(gs.send_msg(msg_send, idc), timeout=5)
                        await shield(send_msg)
                else:
                    print("Error en conexión socket sock_write")
                    print("heartbeat fail")
            except asyncio.TimeoutError as te:
                gs.logger.exception("Tiempo fuera en escritura %s, mode %s" %(
                    te, gs.mode))
                await asyncio.sleep(10)
            except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                gs.logger.exception("Excepción por desconexión %s, mode %s"%(
                    conn_error,gs.mode))
                await asyncio.sleep(10)
                gs.set_status(False)
                del gs.clients[idc]
                if self.exception:
                    self.exception(ex, gs, idc)                
            except Exception as ex:
                gs.logger.exception("Error con modulo cliente gnsocket coro write %s" %ex)
                print("Error con modulo de escritura del socket IDC %s" % idc)
        else:
            await asyncio.sleep(20)
        return [gs, idc, *args], kwargs
    # socket communication terminal to engine

    async def sock_read(self, gs, idc, *args, **kwargs):
        queue = self.qt2n
        msg_from_engine = []
        await asyncio.sleep(.5)
        if idc in gs.clients:
            try:
                heartbeat = await gs.heart_beat(idc)
                recv_msg = gs.recv_msg(idc)
                datagram = await shield(recv_msg)
                if datagram not in {'', "<END>", 'null', None}:
                    msg_dict = json.loads(datagram)
                    msg = {'dt': msg_dict, 'idc': idc}
                    queue.put(msg)
            except asyncio.TimeoutError as te:
                gs.logger.exception("Tiempo fuera en escritura %s, mode %s" %(
                    te, gs.mode))
                await asyncio.sleep(10)
            except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                gs.logger.exception("Excepción por desconexión %s, mode %s"%(
                    conn_error, gs.mode))
                await asyncio.sleep(10)
                gs.set_status(False)
                del gs.clients[idc]
                if self.exception:
                    self.exception(ex, gs, idc)                
            except Exception as ex:
                bprint("Excption on sock_read")
                rprint(ex)
                gs.logger.exception("Error con modulo cliente gnsocket coro read %s" %ex)           
                print("Some error %s en sock_read" % ex)
        else:
            await asyncio.sleep(20)
        return [gs, idc, args], kwargs

    def set_socket_task(self, callback_socket_task):
        self.socket_task = callback_socket_task
