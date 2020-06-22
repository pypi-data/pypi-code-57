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
from gnsocket.socket_base import GNCSocketBase

# module tasktools
from tasktools.taskloop import coromask, renew, simple_fargs_out
from networktools.colorprint import gprint, bprint, rprint

from networktools.library import pattern_value, \
    fill_pattern, context_split, \
    gns_loads, gns_dumps
from networktools.library import my_random_string
from asyncio import shield, wait_for, wait

import ujson as json

tsleep = 2


class GNCSocketClient(GNCSocketBase):

    def __init__(self, queue_n2t, queue_t2n, *args, **kwargs):
        super().__init__(queue_n2t, queue_t2n, 'client', *args, **kwargs)
        self.set_socket_task(self.socket_task)

    def socket_task(self):
        # client socket
        loop = asyncio.get_event_loop()
        self.connected = False
        with GNCSocket(mode='client', timeout=self.timeout,
                       raise_timeout=self.raise_timeout,
                       log_path=self.log_path) as gs:
            try:
                self.loop = loop
                gs.set_address(self.address)
                gs.set_loop(loop)

                async def socket_io():
                    idc = await gs.create_client()
                    try:
                        args = [gs, idc]
                        task_1 = loop.create_task(
                            coromask(
                                self.sock_read,
                                args, {},
                                simple_fargs_out)
                        )
                        task_1.add_done_callback(
                            functools.partial(
                                renew,
                                task_1,
                                self.sock_read,
                                simple_fargs_out)
                        )
                        args = [gs, idc]
                        # task write
                        task_2 = loop.create_task(
                            coromask(
                                self.sock_write,
                                args, {},
                                simple_fargs_out)
                        )
                        task_2.add_done_callback(
                            functools.partial(
                                renew,
                                task_2,
                                self.sock_write,
                                simple_fargs_out)
                        )
                    except Exception as ex:
                        gs.abort(idc)
                        task_1.cancel()
                        task_2.cancel()
                        raise ex
            except Exception as ex:
                gs.logger.exception("Error con modulo cliente gnsocket %s" %ex)                
                print("Eception as %s" %ex)
                raise ex

                ########
                # Insert a coroutine with reader and writer tasks

            async def activate_sock():
                try:
                    await shield(wait_for(socket_io(), timeout=10))
                    return "socket loaded"
                except asyncio.TimeoutError as te:
                    gs.logger.exception("Tiempo fuera en escritura %s, mode %s" %(
                        te, gs.mode))
                    await asyncio.sleep(10)
                except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                    gs.logger.exception("Excepción por desconexión %s, mode %s"%(
                        conn_error,gs.mode))
                    await asyncio.sleep(10)                                                           
            future1 = loop.create_task(activate_sock())
            if not loop.is_running():
                loop.run_forever()


if __name__ == "__main__":
    address = (socket.gethostbyname(socket.gethostname()), 5500)
    client = GNCSocketClient(address=address)
    client.socket_task()
