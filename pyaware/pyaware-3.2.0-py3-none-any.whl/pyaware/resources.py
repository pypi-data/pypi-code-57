import datetime
import queue
import threading
import time
import logging
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, _base
from concurrent.futures.thread import _WorkItem

log = logging.getLogger(__name__)


class FutureThreadPoolExecutor(ThreadPoolExecutor):
    def submit(self, fn, *args, **kwargs):
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError('cannot schedule new futures after shutdown')
            try:
                f = kwargs.pop('_fut')
            except KeyError:
                f = _base.Future()
            w = _WorkItem(f, fn, args, kwargs)

            self._work_queue.put(w)
            self._adjust_thread_count()
            return f

    submit.__doc__ = _base.Executor.submit.__doc__


class PriorityExecutor:
    """
    The priority executor is a thread managing the items put into the thread executor based on how items are retrieved
    from the priority queue.
    """

    def __init__(self, max_workers=1):
        self.q = queue.PriorityQueue()
        self.executor = FutureThreadPoolExecutor(max_workers)
        self.t_manage = threading.Thread(target=self._worker, args=(self.q,))
        self.t_manage.daemon = True
        self.t_manage.start()

    def submit(self, priority: int, fn, fn_args: tuple = None, fn_kwargs: dict = None, cbf=None):
        """
        :param priority: Priority in which to call this task. 1 is highest priority. Larger is lower
        :param fn: Function to execute
        :param fn_args: positional arguments for the function
        :param fn_kwargs: keyword arguments for the function
        :param cbf: call back function that receives a future when the task is complete
        :return:
        """
        if priority <= 0:
            raise ValueError("Please select a priority over 0 as 0 is reserved for aborting the threads")
        log.debug("Queuing priority {priority} for {fn}({args}, {kwargs})".format(
            priority=priority, fn=fn, args=fn_args, kwargs=fn_kwargs))
        args = fn_args or tuple()
        kwargs = fn_kwargs or {}
        fut = _base.Future()
        kwargs["_fut"] = fut
        self.q.put((priority, datetime.datetime.now(), cbf, (fn, args, kwargs)))
        time.sleep(0.00000001)  # Ensures that the datetime increments between submission calls and keeps it in order
        return fut

    def _worker(self, q):
        # TODO instantiate the resource here so that the resource is local to the same thread it is executing
        try:
            while True:
                # As this executor is owned by this object, it should be an appropriate approximate representation
                # of currently running work items
                if self.executor._work_queue.qsize() != 0:
                    continue
                try:
                    item = q.get(timeout=0.2)
                except queue.Empty:
                    continue
                log.debug(item)
                if item == (0, None):
                    break

                priority, timestamp, cbf, (fn, args, kwargs) = item
                fut = self.executor.submit(fn, *args, **kwargs)
                if cbf is not None:
                    fut.add_done_callback(cbf)
        finally:
            self.executor.shutdown()

    def close(self):
        log.debug("Setting abort in priority queue")
        self.q.put((0, None))
        self.t_manage.join()
        log.debug("t_manage thread closed successfully")


class Resource:
    """
    Wraps a resource in the appropriate threading and messaging used by the ResourceManager
    """

    def __init__(self, resource, max_threads=1):
        self._resource = resource
        self._executor = PriorityExecutor(max_threads)

    def close(self):
        self._executor.close()
        self._resource.close()

    def _executor_call(self, handle_ref):
        """
        Wraps a call to the resource with a priority call to the executor
        :param handle:
        :return:
        """
        handle = getattr(self._resource, handle_ref)

        @wraps(handle)
        def _tmp(*args, priority=10, **kwargs):
            return self._executor.submit(priority, handle, fn_args=args, fn_kwargs=kwargs)

        _tmp.__doc__ = self._doc_update(_tmp)
        return _tmp

    def _doc_update(self, func):
        new_doc = []
        param_priority = ":param priority: Priority in which to call this task. 1 is highest priority. Larger is lower"
        return_string = ":return: A wrapped future promising the result {}"
        if func.__doc__ is not None:
            for line in func.__doc__.split('\n'):
                if ":return: " in line:
                    new_doc.append(line.split(':return:')[0] + param_priority)
                    new_doc.append(line.split(':return:')[0] + return_string + line.split(':return:')[-1].strip())
                else:
                    new_doc.append(line)
            return '\n'.join(new_doc)
        else:
            return param_priority + "\n" + return_string.format("")

    def __getattr__(self, item):
        return self._executor_call(item)


class ResourceManager:
    def __init__(self):
        self.resources = {}

    def add_resource(self, resource: object, resource_id: str, max_threads: int = 1):
        self.resources[resource_id] = Resource(resource, max_threads)

    def close(self):
        for resource in self.resources.values():
            resource.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __getitem__(self, item):
        return self.resources[item]


rm = ResourceManager()
if __name__ == "__main__":
    def debug_executor():
        def delay_print(seconds, msg):
            time.sleep(seconds)
            log.debug("Delayed {}s: {}".format(seconds, msg))
            return "RETURNED: " + msg

        def future_print(fut):
            print(fut.result())

        import random

        logging.basicConfig(level=logging.DEBUG)
        ex = PriorityExecutor(max_workers=3)
        time.sleep(2)
        ex.submit(2, delay_print, (1, "HI THERE"), cbf=future_print)
        ex.submit(2, delay_print, (2, "HI THERE"))
        for x in range(1, 50):
            ex.submit(x, delay_print, (0, "HI THERE {}".format(50 - x)), cbf=random.choice([None, future_print]))
        ex.submit(5, delay_print, (3, "HI THERE"))
        ex.submit(4, delay_print, (4, "HI THERE"))
        ex.submit(3, delay_print, (5, "HI THERE"))
        time.sleep(2.5)
        # time.sleep(20)
        ex.close()


    def debug_resource_manager():
        logging.basicConfig(level=logging.DEBUG)

        class FakeResource:
            def delay_print(self, seconds, msg):
                """
                The thing
                :param seconds:
                :param msg:
                :return: None
                """
                time.sleep(seconds)
                log.debug("Delayed {}s: {}".format(seconds, msg))
                return "RETURNED: " + msg

            def future_print(self, fut):
                print(fut.result())
                pass

            def close(self):
                log.debug("CLOSING RESOURCE {}".format(id(self)))

        with ResourceManager() as rm:
            my_resource = FakeResource()
            rm.add_resource(my_resource, "fake1")
            rm["fake1"].delay_print(1, "HI WORLD")
            time.sleep(2)


    debug_resource_manager()
