import asyncio
import logging
import aiojobs
import async_timeout
from functools import wraps

log = logging.getLogger(__name__)


def periodic(coro, period, timeout, loop, callback_handle=None, start_after=0, coro_kwargs=None):
    """
    :param coro: Coroutine to wrap in a periodic call
    :param period:
    :param timeout:
    :param loop:
    :param uncaught_exception_cnt:
    :return:
    """

    @wraps(coro)
    async def wrapped():
        try:
            if start_after:
                log.info("Waiting {} sec to start periodic task {}".format(start_after, coro))
                await asyncio.sleep(start_after)
        except asyncio.CancelledError:
            log.info("Cancelled before starting periodic task {}".format(coro))
            return
        while True:
            try:
                now = loop.time()
                try:
                    with async_timeout.timeout(timeout):
                        if coro_kwargs is not None:
                            res = await coro(**coro_kwargs)
                        else:
                            res = await coro()
                    if callback_handle:
                        callback_handle(res)
                except asyncio.TimeoutError:
                    log.info(
                        "Periodic task {} failed to completed in the specified timeout {}s".format(coro, timeout))
                sleep_time = now + period - loop.time()
                await asyncio.sleep(sleep_time)
            except asyncio.CancelledError:
                log.info("Cancelling {} as requested".format(coro))
                break

    return wrapped()


class TaskScheduler:
    """
    Base class to handle scheduling of reads and publishes
    Will also be responsible for error handling, timeouts and rescheduling broken tasks.
    """

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.scheduler = None
        self.critical_tasks = []
        self.non_critical_tasks = []
        self.loop.run_until_complete(self.init())
        self.closing = False

    async def init(self):
        self.scheduler = await aiojobs.create_scheduler(close_timeout=0.5)

    async def _run_until_critical_cancel(self):
        # Check if any jobs didn't initialise
        if any([task.closed for task in self.critical_tasks]):
            try:
                raise Exception("Critical Tasks could not initialise correctly. Aborting")
            except:
                log.exception("Tasks could not be initialised correctly. Check intialisation routines")
                raise
        for fs in asyncio.as_completed([func.wait() for func in self.critical_tasks]):
            try:
                await fs
            except:
                log.exception("Critical task {} is now inactive. Exiting to allow service to restart".format(fs))
                raise

    def run(self):
        try:
            if self.critical_tasks:
                self.loop.run_until_complete(self._run_until_critical_cancel())
            else:
                self.loop.run_forever()
        finally:
            self.close()
            log.warning("Sequencer finished running tasks")

    def create_periodic_task(self, coro, period, timeout=None, callback_handle=None, critical=True, start_after=0,
                             coro_kwargs=None):
        """
        Create a task to happen
        :param period:
        :param timeout:
        :return:
        """
        wrapped_coro = periodic(coro, period, timeout, self.loop, callback_handle, start_after, coro_kwargs=coro_kwargs)
        spawn = self.scheduler.spawn(wrapped_coro)
        log.info("Spawning: {}".format(wrapped_coro))
        job = self.loop.run_until_complete(spawn)
        log.info("Spawning Complete: {}-{}".format(wrapped_coro, job))
        if critical:
            self.critical_tasks.append(job)
        else:
            self.non_critical_tasks.append(job)

    def close(self):
        if self.closing:
            return
        self.closing = True
        log.info("Closing TaskScheduler")
        if self.loop is not None:
            if self.scheduler is not None:
                log.info("Scheduling close")
                fut = asyncio.ensure_future(self.scheduler.close())
                self.loop.run_until_complete(fut)
                self.scheduler = None
        log.info("Close complete")

    def _backup_close(self, loop):
        """
        Code is here for closing any tasks that are not controlled by the scheduler. Currently not used
        :param loop:
        :return:
        """

        def shutdown_exception_handler(loop, context):
            if "exception" not in context \
                    or not isinstance(context["exception"], asyncio.CancelledError):
                loop.default_exception_handler(context)

        loop.set_exception_handler(shutdown_exception_handler)
        log.warning("Backup Loop closer")
        # Handle shutdown gracefully by waiting for all tasks to be cancelled
        tasks = asyncio.gather(*asyncio.Task.all_tasks(loop=loop), loop=loop, return_exceptions=True)
        tasks.add_done_callback(lambda t: loop.stop())
        tasks.cancel()

        # Keep the event loop running until it is either destroyed or all
        # tasks have really terminated
        while not tasks.done() and not loop.is_closed():
            loop.run_forever()

    def create_task(self, coro, critical=True):
        spawn = self.scheduler.spawn(coro)
        log.debug("Spawning: {}".format(coro))
        job = self.loop.run_until_complete(spawn)
        if critical:
            self.critical_tasks.append(job)

    def __del__(self):
        self.close()


if __name__ == "__main__":
    sched = TaskScheduler()
    import time

    FORMAT = ('%(asctime)-15s %(threadName)-15s '
              '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
    logging.basicConfig(format=FORMAT, filename="tst.txt")
    log.setLevel(logging.DEBUG)
    import random


    async def print_thing():
        if random.random() > 0.9:
            raise Exception("RANDOM EXCEPTION")
        await asyncio.sleep(random.random() * 1.1)
        print(time.time())
        return "I AM A THING"
        # try:
        #     if random.random() > 0.9:
        #         raise Exception("RANDOM EXCEPTION")
        #     await asyncio.sleep(random.random() * 2)
        #     print(time.time())
        # except asyncio.CancelledError:
        #     log.warning("CANCELLED MY PRINT THING")
        #     # raise


    def callback_handle(res):
        print("I GOT THING: ", res)


    sched.create_periodic_task(print_thing, 1, 1)
    sched.create_periodic_task(print_thing, 1, 1, callback_handle=callback_handle)
    # sched.create_periodic_task(print_thing, 1, None)
    sched.run()
