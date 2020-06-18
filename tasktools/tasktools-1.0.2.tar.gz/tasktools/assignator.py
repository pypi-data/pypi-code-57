import asyncio
import functools

from networktools.colorprint import gprint, bprint, rprint

from .taskloop import coromask, renew, simple_fargs, simple_fargs_out
from .scheduler import TaskScheduler


def get_free_ico(icos):
    ico_list = [
        key for key, v in icos.items() if not v]
    ico = None
    if ico_list:
        ico = ico_list.pop()
    return ico


class TaskAssignator:
    """
    Manage the tasks assigned to a TaskScheduler instance

    :param scheduler: A TaskScheduler instance
    :param queue_tasks: a queue
    :param sta_assigned: a dict managed for multiprocessing
    :param dt_status: a string that select the kind of group {GROUP, ALL}
    :param dt_group: a list of the group selected
    :param args: some extra args
    :param kwargs: some extra keyword args

    """

    def __init__(self,
                 scheduler,
                 queue_tasks,
                 queue_answer,
                 sta_assigned,
                 dt_status,
                 dt_group,
                 enqueued,
                 locker,
                 *args, **kwargs):
        self.scheduler = scheduler
        self.queue_tasks = queue_tasks
        self.queue_ans = queue_answer
        self.sta_assigned = sta_assigned
        self.dt_status = dt_status
        self.dt_group = dt_group
        self.enqueued = enqueued
        self.ts = 10
        self.locker = locker
        self.code_filter = kwargs.get('code_filter', 'code')
        self.counter = 0
        if 'ts' in kwargs:
            self.ts = kwargs.get('ts', 3)

    async def new_process(self, queue_tasks, * args, **kwargs):
        """
        This coroutine activate a process with new station task
        Check every \ts\ seconds the queue_tasks if there are new
        stations or tasksto add.

        Works on a async wheel

        :param queue_tasks: a queue to put task ids

        """
        await asyncio.sleep(self.ts)
        scheduler = self.scheduler
        sta_assigned = []
        for ipt, val in self.sta_assigned.items():
            for ico, ids in val.items():
                sta_assigned.append(ids)
        dt_status = self.dt_status
        dt_group = self.dt_group
        msg_in = []

        try:
            tasks = []
            W = 0
            if not queue_tasks.empty():
                for i in range(queue_tasks.qsize()):
                    ids = queue_tasks.get()
                    scheduler.status_tasks[ids] = True
                    scheduler.sta_init[ids] = True
                    if ids in self.enqueued:
                        q = 0
                        for ipt in scheduler.proc_tasks.keys():
                            print("IPT in scheduler", ipt,
                                  scheduler.proc_tasks)
                            q += 1
                            if len(scheduler.proc_tasks.get(ipt)) < \
                               scheduler.lnproc and \
                               ids not in sta_assigned:
                                respuesta = {'station': ids,
                                             'core': ipt, }
                                print("Respuest", respuesta, "DT status > %s <"
                                      % dt_status)
                                if dt_status == 'GROUP':
                                    if scheduler.stations.get(ids).get(self.code_filter) in dt_group:
                                        icos = scheduler.add_task(ids, ipt)
                                        scheduler.set_init(ids)
                                        ico = get_free_ico(icos)
                                        self.locker.acquire()
                                        self.scheduler.add_sta_assigned(
                                            ipt, ico, ids)
                                        self.locker.release()
                                        ans = "TASK %s ADDED TO %s" % (
                                            ids, ipt)
                                        respuesta.update({'added': True})
                                elif dt_status == 'ALL':
                                    icos = scheduler.add_task(ids, ipt)
                                    ico = get_free_ico(icos)
                                    scheduler.set_init(ids)
                                    qr = {ico: ids}
                                    self.counter +=1                                    
                                    ans = "TASK %s ADDED TO %s, de un total de:%d" % (ids, ipt, self.counter)
                                    sta_assigned.append(ids)
                                    self.locker.acquire()
                                    self.scheduler.add_sta_assigned(
                                        ipt, ico, ids)
                                    self.locker.release()
                                    respuesta.update({'added': True})
                                self.queue_ans.put(respuesta)
                    queue_tasks.task_done()
            else:
                pass
                # self.queue_ans.put({'added': False})
            return [queue_tasks, args], kwargs
        except Exception as ex:
            bprint("Error en asignación de tareas a procesador: %s" % ex)
            raise ex

    def new_process_task(self):
        """
        This function allows the system to call the coroutine that add
        a new_process in an asynchronous loop *the wheel*
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            args = [self.queue_tasks]
            # bprint("New process task")
            task = loop.create_task(
                coromask(
                    self.new_process,
                    args, {},
                    simple_fargs_out)
            )
            #
            task.add_done_callback(
                functools.partial(
                    renew,
                    task,
                    self.new_process,
                    simple_fargs_out)
            )
        except Exception as ex:
            rprint("Error en levantar corrutina %s" % ex)
            raise ex
        if not loop.is_running():
            loop.run_forever()
