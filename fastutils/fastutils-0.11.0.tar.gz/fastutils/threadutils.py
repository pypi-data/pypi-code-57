
import time
import threading
import logging

logger = logging.getLogger(__name__)


class ServiceCore(object):

    def __init__(self):
        # service inner setup
        self.setup()

    def setup(self):
        # service are alway work in new thread.
        # and there is only one work thread for a service.
        self.work_thread_starting_lock = threading.Lock()
        self.work_thread = None
        # service is always ready while not terminated.
        # so that before you terminate a service, you can start and stop the service many times.
        self.terminate_flag = False
        self.terminated_time = None
        self.stop_flag = False
        self.start_time = None
        self.stop_time = None
        self.stoped_time = None
        self.is_running = False

    def start(self):
        if not self.is_running:
            logger.debug("Service {0} starting...".format(self.name))
        else:
            logger.debug("Service {0} already started.".format(self.name))
        self.stop_flag = False
        self.start_time = time.time()
        self.stop_time = None
        self.stoped_time = None
        with self.work_thread_starting_lock:
            if self.work_thread is None:
                self.work_thread = threading.Thread(target=self.main)
                self.work_thread.setDaemon(True)
                self.work_thread.start()

    def stop(self, wait=True, wait_timeout=-1):
        if self.is_running:
            logger.debug("Service {0} stopping...".format(self.name))
        else:
            logger.debug("Service {0} already stoped.".format(self.name))
        self.stop_flag = True
        self.stop_time = time.time()
        if wait:
            stime = time.time()
            while self.is_running:
                if wait_timeout > 0 and time.time() - stime > wait_timeout:
                    break
                else:
                    time.sleep(1)

    def terminate(self, wait=True, wait_timeout=-1):
        logger.debug("Service {0} terminating...".format(self.name))
        self.terminate_flag = True
        self.stop(wait, wait_timeout)

    def main(self):
        while not self.terminate_flag:
            if self.stop_flag:
                time.sleep(1)
                continue
            try:
                self.is_running = True
                logger.debug("Service {0} started.".format(self.name))
                while not self.stop_flag:
                    try:
                        if getattr(self.service_loop, "__self__", None) == self:
                            self.service_loop(*self.args, **self.kwargs)
                        else:
                            self.service_loop(self, *self.args, **self.kwargs)
                    except Exception as error:
                        logger.exception("Service {} got error in service loop...".format(self.name))
                        if self.on_loop_error:
                            try:
                                if getattr(self.on_loop_error, "__self__", None) == self:
                                    self.on_loop_error(error)
                                else:
                                    self.on_loop_error(self, error)
                            except Exception as error:
                                logger.exception("Service {} got error in on_loop_error...".format(self.name))
                    finally:
                        if self.on_loop_finished:
                            try:
                                if getattr(self.on_loop_finished, "__self__", None) == self:
                                    self.on_loop_finished()
                                else:
                                    self.on_loop_finished(self)
                            except Exception as error:
                                logger.exception("Service {} got error in on_loop_finished...".format(self.name))
                    if self.loop_interval:
                        try:
                            time.sleep(self.loop_interval)
                        except InterruptedError:
                            self.terminate_flag = True
                            break
            finally:
                self.is_running = False
                self.stop_flag = True
                self.stoped_time = time.time()
                logger.debug("Service {0} stopped.".format(self.name))
        self.terminated_time = time.time()
        logger.debug("Service {0} terminated.".format(self.name))


class Service(ServiceCore):

    def __init__(self, service_loop, args=None, kwargs=None, name=None, on_loop_error=None, on_loop_finished=None, loop_interval=0):
        self.service_loop = service_loop
        self.args = args or []
        self.kwargs = kwargs or {}
        self.name = name or service_loop.__name__
        self.on_loop_error = on_loop_error
        self.on_loop_finished = on_loop_finished
        self.loop_interval = loop_interval
        super().__init__()

class ServiceBase(ServiceCore):
    name = None
    loop_interval = 0
  
    def __init__(self):
        self.args = ()
        self.kwargs = {}
        super().__init__()

    def on_loop_finished(self):
        pass

    def on_loop_error(self, error):
        pass

    def service_loop(self):
        raise NotImplementedError()
