# Standar lib
import asyncio
import functools
from multiprocessing import Manager, Queue, Lock

# contrib modules
import ujson as json

# Own module
from gnsocket.gn_socket import GNCSocket

# module tasktools
from tasktools.taskloop import coromask, renew, simple_fargs
from networktools.colorprint import gprint, bprint, rprint

from networktools.library import pattern_value, \
    fill_pattern, context_split, \
    gns_loads, gns_dumps

from networktools.queue import send_queue, read_queue_gen

tsleep = 2


class GNCSocketServer:

    def __init__(self, queue_t2n, queue_n2t, *args, **kwargs):
        self.address = kwargs.get('address', ('localhost', 6666))
        # This queue list is fixed and allow us to control
        # the scheduler system with more or less instances
        # not to send msg to every instace
        self.common_queues = kwargs.get('common_queues', {})
        self.gs = GNCSocket(mode='server')
        self.gs.set_address(self.address)
        self.qt2n = queue_t2n
        self.qn2t = queue_n2t

    async def read_queue(self, queue):
        for i in range(queue.qsize()):
            msg_in = queue.get()
            msg = msg_in['msg']
            idc = msg_in['idc']
            await self.gs.send_msg(json.dumps(msg), idc)

    async def sock_write(self, gs, idc):
        # Receive from sources and send data to clients
        queue_in = self.qt2n
        await asyncio.sleep(tsleep)
        try:
            rprint("Sock write check queque<")
            bprint(queue_in.empty())
            bprint(self.qt2n.empty())
            bprint(self.qn2t.empty())
            rprint(">Sock write check queque")
            for msg_ans in read_queue_gen(queue_in):
                bprint("Recibiendo msg calculado")
                bprint(msg_ans)
                rprint("Listo para enviar a socket")
                msg_send = json.dumps(msg_ans)
                await gs.send_msg(msg_send, idc)
        except Exception as exec:
            print("Error con modulo de escritura del socket")
            raise exec

    # socket communication terminal to engine
    async def sock_read(self, gs, idc):
        # read from client and send to the manager
        # the datagrams must bring the source id: ids
        loop = asyncio.get_event_loop()
        queue_out = self.qn2t
        msg_from_engine = []
        await asyncio.sleep(tsleep)
        try:
            datagram = await gs.recv_msg(idc)
            if datagram not in {'', "<END>", 'null', None}:
                msg_dict = json.loads(datagram)
                bprint("Enviando a calculo->%s" % msg_dict)
                queue_out.put(msg_dict)
        except Exception as exec:
            print("Error con modulo escritura socket", exec)
            raise exec

    def socket_task(self):
        #print("XDX socket loop inside", flush=True)
        with GNCSocket(mode='server') as gs:
            #gs = GNCSocket(mode='server')
            loop = asyncio.get_event_loop()
            self.loop = loop
            gs.set_address(self.address)
            gs.set_loop(loop)
            try:
                async def socket_io(reader, writer):
                    print("Entrando a socket -io")
                    idc = await gs.set_reader_writer(reader, writer)
                    # First time welcome
                    welcome = json.dumps({"msg": "Welcome to socket"})
                    print("Enviando msg welcome--%s" % welcome)
                    await gs.send_msg(welcome, idc)
                    await asyncio.sleep(0.1)
                    # task reader
                    try:
                        args = [gs, idc]
                        task_1 = loop.create_task(
                            coromask(
                                self.sock_read,
                                args,
                                simple_fargs)
                        )
                        task_1.add_done_callback(
                            functools.partial(
                                renew,
                                task_1,
                                self.sock_read,
                                simple_fargs)
                        )
                        args = [gs, idc]
                        # task write
                        task_2 = loop.create_task(
                            coromask(
                                self.sock_write,
                                args,
                                simple_fargs)
                        )
                        task_1.add_done_callback(
                            functools.partial(
                                renew,
                                task_1,
                                self.sock_write,
                                simple_fargs)
                        )
                    except Exception as exe:
                        gs.close()
                        if not self.conn:
                            self.conn.close()
                        raise exec
                gprint("=")
                gprint("loop"+str(loop))
                rprint("Loop is runnign?<"+str(loop.is_running())+">")
                print("Creating socket server future")
                future = loop.create_task(
                    gs.create_server(socket_io, loop))
                rprint(loop.is_running())
                gprint("=")
                print("Future de server socket->")
                print(future)
                print(loop.is_running())
                if not loop.is_running():
                    loop.run_forever()
                else:
                    loop.run_until_complete(future)
            except KeyboardInterrupt:
                gs.close()
                loop.run_until_complete(gs.wait_closed())
            except Exception as ex:
                print("Otra exception", ex)
            finally:
                print("Clossing loop on server")
                # loop.close()

        def close(self):
            self.gs.close()
