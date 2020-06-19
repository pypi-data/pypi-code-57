import time
import threading
import traceback
import argparse
import logging

from . import appserver, controlserver

parser = argparse.ArgumentParser(description="Run a Vibrance relay server "
                                 "(command server and client WebSocket "
                                 "servers).")

parser.add_argument("--psk", help="Optional password for the command server.")

parser.add_argument("--cert", help="SSL certificate for securing the "
                    "WebSockets and the command server.")

parser.add_argument("--key", help="SSL private key for securing the WebSockets"
                    " and the command server.")

log_levels = {"DEBUG": logging.DEBUG, "INFO": logging.INFO,
              "WARNING": logging.WARNING, "ERROR": logging.ERROR,
              "CRITICAL": logging.CRITICAL}

parser.add_argument("--debug", help=f"Debug level {log_levels.keys()}",
                    default="CRITICAL", choices=log_levels.keys())

args = parser.parse_args()

logging.basicConfig(level=log_levels[args.debug])

def wrapLoop(loopfunc):
    """Wraps a thread in a wrapper function to restart it if it exits."""
    def wrapped():
        while True:
            try:
                loopfunc()
            except BaseException:
                print(f"Exception in thread {loopfunc},"
                      " restarting in 10s...")
                traceback.print_exc()
            else:
                print(f"Thread {loopfunc} exited, restarting in 10s...")
            time.sleep(10)
    return wrapped

appServer = appserver.AppServer(args.cert, args.key)
controlServer = controlserver.ControlServer(appServer, args.psk,
                                            args.cert, args.key)

appServerThread = threading.Thread(target=wrapLoop(appServer.run))
controlServerThread = threading.Thread(target=wrapLoop(controlServer.run))
appCheckAliveThread = threading.Thread(
    target=wrapLoop(appServer.handleCheckAlive))

appServerThread.start()
controlServerThread.start()
appCheckAliveThread.start()

while True:
    time.sleep(1)
