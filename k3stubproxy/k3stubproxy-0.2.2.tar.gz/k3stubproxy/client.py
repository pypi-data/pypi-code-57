"""
client side api and implementation
"""

import logging
import json
from threading import Thread
from k3process import rpc
from k3process.scheduler import Scheduler
import threading
import time

logger = logging.getLogger(__name__)
stubLogger = logging.getLogger("stub_call_logger")
# logger = None
# moduleNm = __name__

class _Traget():
    
    def __init__(self):
        self.targetTarget = None
    
    def _retister_target(self, targetTarget):
        self.targetTarget = targetTarget
    
    def call_on_client_stub(self, functionName, kwargs):
        logger.info("Client side call_on_client_stub received: {} {}".format(functionName, kwargs))
        if self.targetTarget:
            return self.targetTarget(functionName, kwargs)
        else:
            logger.warning("Recveid msg on stub side, but not target has been registered. Raising error for callee")
            raise RuntimeError("No c callback set to forward client call to")
            

class ProxyClient:
    
    def __init__(self, config):
        self.proxyRunningEvent = threading.Event()
        self.config = config
        with open(self.config["stub_function_definition"]) as fh:
            self.stubFuncDef = json.load(fh)
        
        self.stubCallLogHandle = None
        if config["stub_call_log_path"]:
            fmtStr = "%(asctime)s: %(message)s"
            fh = logging.FileHandler(config["stub_call_log_path"])
            fh.setFormatter(logging.Formatter(fmtStr))
            stubLogger.addHandler(fh)
            
        self.recvThread = Thread(target=self._run, name="stub_client_proxy_recv")
        self.target = _Traget()
        self.remoteTarget = None
        logging.debug("ProxyClient init complete")
        self.callCount = 0
            
    def get_function_parameters(self, functionName):
        try:
            methodArgs = self.stubFuncDef[functionName]["parameters"]
            for arg in methodArgs:
                _a1, _a2, _a3 = arg
        except Exception:
            logger.warning(f"Function definition for function {functionName} in the wrong format")
            raise
        return methodArgs
    
    def register_server_to_client_target_func(self, aCallable):
        self.target._retister_target(aCallable)
    
    def _run(self):
        s = Scheduler(200)
        Thread(target=s.runScheduler, name="prx_recv_scheduler").start()
        logger.debug("Scheduler started")
        try:
            logger.debug("Connecting to server")
            with rpc.K3RPCClient("stub_client", self.config["host"], self.config["port"], self.config["auth_key"].encode('utf-8'), scheduler=s) as rpcClientSession:
                logger.info("Connecting to server successful")
                rpcClientSession.set_target(self.target)
                rpcClientSession.wait_remote_target_set()
                self.remoteTarget = rpcClientSession.get_remote_target_proxy()
                self.proxyRunningEvent.set()
                rpcClientSession.wait_remote_close()
                logger.info("Server terminated client server connection")
        except Exception as e:
            logger.error("Proxy client receive thread raised an exception", exc_info=True)
        finally:
            logger.info("Proxy client receive thread done")
            s.stop()
            
    def forward_proxy_stub_call(self, functionName, kwargs):
        #logger.debug(f"{functionName} called. Args: {kwargs}")
        
        if self.remoteTarget == None:
            logger.error("Cannot forward stub call as proxy is not running")
            raise RuntimeError("Cannot forward stub call as proxy is not running") 
        
        self.callCount += 1
#         if self.callCount % 100 == 0:
#             print(self.callCount)
    
        ret = self.remoteTarget.proxy_stub_call(functionName, kwargs)
        stubLogger.debug("{:40} {:44} -> {}".format(functionName, str(kwargs), str(ret)))
        return ret
    
    def start_proxy_async(self):
        self.recvThread.start()
        self.proxyRunningEvent.wait(2)
        
def init_proxy_client(stubConfig) -> ProxyClient:
    global logger
    try:
        with open(stubConfig) as fh:
            config = json.load(fh)
        logging.basicConfig(level=config["log_level"].upper(), format="%(asctime)s %(levelname)s: %(message)s")
    #     logger = logging.getLogger(moduleNm)
        prx =  ProxyClient(config)
        logger.info("Proxy connection/recv thread started")
        prx.start_proxy_async()
    except:
        logger.exception("Error in k3stubproxy.init_proxy_client")
    else:
        logger.info("init_proxy_client complete")
    return prx
        