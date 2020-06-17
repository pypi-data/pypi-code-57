import asyncio
from gnsocket.gn_socket import GNCSocket
from gnsocket.conf.socket_conf import TEST_TEXT
from tasktools.taskloop import coromask, renew, simple_fargs
import functools
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

    mode = 'server'
    print(mode)
    gs = GNCSocket(mode=mode)
    print(gs.address)
    msg = TEST_TEXT
    idc = "X"
    # Testing message generator
    print("Status %s" % gs.status)
    for m in gs.generate_msg(msg):
        print(m.decode('utf-8'))
    # gs.send_msg(msg)
    # gs.send_msg(msg)
    # print(gs.conn)
    # Testing communicate
    print(gs)
    print("Entrando a loop")
    loop = asyncio.get_event_loop()
    gs.set_loop(loop)
    tsleep = 1  # 1 second sleep by some coroutines
    # Create coroutines

    async def sock_read(queue, idc):
        bprint("Sock read")
        try:
            datagram = await gs.recv_msg(idc)
            bprint("msg recibido")
            if not datagram == '' and \
               datagram != "<END>":
                bprint("Recibido en server")
                bprint(datagram)
                await queue.put(datagram)
            await asyncio.sleep(tsleep)
            # print(msg_tot)
        except Exception as exec:
            gs.set_status('OFF')
            raise exec

    async def sock_write(queue, idc):
        rprint("Sock write")
        # read async queue
        try:
            if not queue.empty():
                for q in range(queue.qsize()):
                    msg = await queue.get()
                    await gs.send_msg(msg, idc)
                await gs.send_msg("<END>", idc)
                rprint("Msg enviado")
            await asyncio.sleep(tsleep)
        except Exception as exec:
            gs.set_status('OFF')
            raise exec

    async def socket_io(reader, writer):
        queue = asyncio.Queue()
        idc = await gs.set_reader_writer(reader, writer)
        # First time welcome
        welcome = "Welcome to socket"
        rprint(welcome)
        await gs.send_msg(welcome, idc)
        await gs.send_msg("<END>", idc)
        # task reader
        try:
            args = [queue, idc]
            task = loop.create_task(
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
            # task write
            task = loop.create_task(
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
    try:
        future = loop.create_task(gs.create_server(socket_io, loop))
        loop.run_forever()
    except Exception as e:
        raise e
    loop.close()
    gs.close()
