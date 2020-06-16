from gnsocket.socket_server import GNCSocketServer
import concurrent.futures
import socket
from multiprocessing import Manager, Queue
from networktools.ssh import clean_port
import asyncio
from collector.local import COLLECTOR_SOCKET_IP
from collector.local import COLLECTOR_SOCKET_PORT


def socket_exception(ex, gs, idc):
    bprint("Excepción en socket")
    bprint(gs)
    rprint("Id socket client -> %s" % idc)
    raise ex


if __name__ == "__main__":
    workers = 2
    with concurrent.futures.ProcessPoolExecutor(workers) as executor:
        address = (COLLECTOR_SOCKET_IP, COLLECTOR_SOCKET_PORT)
        clean_port(COLLECTOR_SOCKET_PORT)
        loop = asyncio.get_event_loop()
        manager = Manager()
        queue_n2t = manager.Queue()
        # network->terminal
        queue_t2n = manager.Queue()

        server_socket = GNCSocketServer(
            queue_n2t, queue_t2n, address=address,
            callback_exception=socket_exception)
        try:
            loop.run_in_executor(
                executor,
                server_socket.socket_task
            )
        except Exception as ex:
            print("Falla en cargar socket task")
            raise ex
