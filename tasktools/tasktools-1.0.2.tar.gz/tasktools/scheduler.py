# standar library
import asyncio
import functools
from asyncio import shield

# contrib
from networktools.library import my_random_string
from networktools.colorprint import gprint, bprint, rprint

# same module
from .taskloop import coromask, renew, simple_fargs, simple_fargs_out
from networktools.factory import FactoryClass


class TaskScheduler:
    """
    This class is a generic tasks scheduler that uses
    asyncio and multiprocessing
    For every new process activate M idle coro tasks
    until when are assigned by a function that send
    an id

    :param args: an unpacked list
    :param kwargs: an unpacked dictionary with at least {*ipt* dict, *ico* dict, *assigned_task* dict, *nproc* int, *sta_init* dict}, all in shared memory manager

    """

    def __init__(self, *args, **kwargs):
        """
        Is a generic init method, the inputs required are
        """
        self.ipt = kwargs.get('ipt', [])
        self.ico = kwargs.get('ico', [])
        self.assigned_tasks = kwargs.get('assigned_tasks', {})
        self.lnproc = kwargs.get('nproc', 3)
        self.sta_init = kwargs.get("sta_init", {})
        self.enqueued = kwargs.get('enqueued', list())

    def set_ipt(self, uin=4):
        """
        Defines a new id for relation process-collect_task, check if exists

        :param uin: is an optional int to define the length of the keys for ipt dict

        :returns: a new key from ipt
        """
        ipt = my_random_string(uin)
        while True:
            if ipt not in self.ipt:
                self.ipt.append(ipt)
                break
            else:
                ipt = my_random_string(uin)
        return ipt

    def set_ico(self, uin=4):
        """
        Defines a new id for task related to collect data
        inside a worker, check if exists

        :param uin: is an optional int to define the length of the keys for ico dict

        :returns: a new key from ico
        """
        ico = my_random_string(uin)
        while True:
            if ico not in self.ico:
                self.ico.append(ico)
                break
            else:
                ico = my_random_string(uin)
        return ico

    async def run_task(self, *args):
        """
        A default coroutine that await .1 secs every time

        :param args: a unpacked list

        :returns: the same list
        """
        await asyncio.sleep(.1)
        return args

    def set_new_run_task(self, **coros_callback):
        """
        Is a function that you have to call to define the corutines which you need
        to execute on the wheel (gear)

        Is recomended the use at the end of the __init__ method on your new class.

        :param coros_callback: is a dictionary with the corutines, that depends of what you need:

        - A unidirectional machine: you have to set only the *run_task* key
        - A bidirectional machine: you ahve to set also *net2service* and *service2net* keys
        """
        run_task = coros_callback.get('run_task', None)
        net2service_task = coros_callback.get('net2service', {})
        service2net_task = coros_callback.get('service2net', {})
        self.n2s = None
        self.s2n = None
        self.run_task = None

        if asyncio.iscoroutinefunction(run_task):
            self.run_task = run_task
        else:
            print("The callback run_task is not a coroutine")

        if asyncio.iscoroutinefunction(net2service_task.get('coro')):
            self.n2s = net2service_task
        else:
            print("The callback net2service is not a coroutine")

        if asyncio.iscoroutinefunction(service2net_task.get('coro')):
            self.s2n = service2net_task
        else:
            print("The callback service2net is not a coroutine")

    async def process_sta_task(self, ipt, ico, *args, **kwargs):
        """
        Process gather data for ids station

        This coroutine is executed for both cases: unidirectional and bidirectional

        :param ipt: is an ipt value to work with the *ipt* process
        :param ico: is an ico value to work with the *ico* object
        :param args: an unpacked list to execute the *run_task*

        :returns: the first two inputs and the unpacked result
        """
        assigned_task = self.assigned_tasks.get(ipt, {}).get(ico, None)
        result_args, result_kwargs = [], {}
        log = kwargs.get('log')
        try:
            if assigned_task:
                if not self.sta_init.get(assigned_task):
                    args, kwargs = self.set_pst(assigned_task, args, kwargs)
                result_args, result_kwargs = await shield(self.run_task(*args, **kwargs))
            else:
                result_args, result_kwargs = args, kwargs
            return [ipt, ico, *result_args], result_kwargs                
        except Exception as e:
            if log:
                log.exception("STA_TASK: Falla en inicializar la corutina loop, %s %s" %(args, kwargs))
            raise e            

    async def process_sta_task_n2s(self, ipt, ico, *args, **kwargs):
        """
        Process channel network to service data for ids station

        This coroutine is executed for bidirectional case, on network to service direction

        :param ipt: is an ipt value to work with the *ipt* process
        :param ico: is an ico value to work with the *ico* object
        :param args: an unpacked list to execute the *run_task*

        :returns: the first two inputs and the unpacked result
        """

        assigned_task = self.assigned_tasks.get(ipt, {}).get(ico, None)
        result_args, result_kwargs = [], {}
        log = kwargs.get('log')
        try:
            if assigned_task:
                if not self.sta_init.get(assigned_task):
                    args, kwargs = self.set_pst_n2s(assigned_task, args, kwargs)
                result_args, result_kwargs = await shield(self.n2s_coro(*args, **kwargs))
            else:
                result_args, result_kwargs = args, kwargs
            return [ipt, ico, *result_args], result_kwargs                
        except Exception as e:
            if log:
                log.exception("N2S: Falla en inicializar la corutina loop, %s %s" %(args, kwargs))
            raise e            

    async def process_sta_task_s2n(self, ipt, ico, *args, **kwargs):
        """
        Process channel service 2 network for ids station

        This coroutine is executed for bidirectional case, on service to network direction

        :param ipt: is an ipt value to work with the *ipt* process
        :param ico: is an ico value to work with the *ico* object
        :param args: an unpacked list to execute the *run_task*

        :returns: the first two inputs and the unpacked result
        """
        assigned_task = self.assigned_tasks.get(ipt, {}).get(ico, None)
        result_args, result_kwargs = [], {}
        log = kwargs.get('log')        
        try:
            if assigned_task:
                if not self.sta_init[assigned_task]:
                    args, kwargs = self.set_pst_s2n(assigned_task, args, kwargs)
                result_args, result_kwargs = await shield(self.s2n_coro(*args, **kwargs))
            else:
                result_args, result_kwargs = args, kwargs
            return [ipt, ico, *result_args], result_kwargs                
        except Exception as e:
            if log:
                log.exception("S2N: Falla en inicializar la corutina loop, %s %s" %(args, kwargs))
            raise e            

    def get_ipt(self, ids):
        for ipt, ico_set in self.assigned_tasks.items():
            icos = [ico for ico in ico_set if ico_set[ico] == ids]
            rprint(icos)
            if icos:
                return ipt
        return None

    async def process_sta_manager(self, ipt):
        """
        Manage asignation of station to task inside ipt process

        :param ipt: the key of the process

        :returns: a list object with ipt value
        """
        #
        ids_list = self.proc_tasks[ipt]
        for ids in ids_list:
            if ids not in self.assigned_tasks[ipt].values():
                for ico, value in self.assigned_tasks[ipt].items():
                    if value is None:
                        self.assigned_tasks[ipt].update({ico: ids})
                        break
        await asyncio.sleep(1)
        return [ipt], {}

    def set_pst(self, ids, args, kwargs):
        """
        Set the factory for the wheel's array

        In your class you have to rewrite this.

        :param ids: key of the source
        :param args: list of arguments

        :returns: a different list of future arguments
        """
        return [ids, args[1], args[2]], kwargs

    def set_init(self, ids):
        """
        Is a flag for every station, the ids is related with the id
        assigned to the station

        """
        self.sta_init.update({ids: False})

    def set_init_args_kwargs(self, ipt):
        """
        Set the initial list of arguments

        In your class you have to rewrite this.

        :returns: a list of initial arguments
        """
        return [None, None, None, None], {}

    def add_sta_assigned(self, ipt, ico, ids):
        ico_d = self.assigned_tasks[ipt]
        ico_d[ico] = ids
        self.assigned_tasks[ipt] = ico_d

    def unset_sta_assigned(self, ipt, ico, ids):
        ico_d = self.assigned_tasks[ipt]
        ico_d[ico] = None
        self.assigned_tasks[ipt] = ico_d

    def add_task(self, ids, ipt):
        """
        Add an *ids* task to some *ipt* process

        :param ids: the key of a source
        :param ipt: the key or identifier of a process
        """
        self.proc_tasks[ipt] += [ids]
        icos = self.assigned_tasks[ipt]
        return icos

    def manage_tasks(self, ipt):
        """
        A method to manage the tasks assigned to *ipt* process

        Initialize an event loop, and assign idle tasks for this process

        Create the tasks for every source assigned to this process.
        Check the cases unidirectional and bidirectional.

        :param ipt: the key or identifier of a process
        """
        # loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        v = 1
        tasks = []
        self.assigned_tasks[ipt] = {}
        new_dict = {}
        for i in range(self.lnproc):
            ico = self.set_ico()
            nd = {ico:  None}
            new_dict.update(nd)
        self.assigned_tasks[ipt] = new_dict
        tasks_on_this_ipt = self.assigned_tasks.get(ipt)
        stax, sta_kwargs = self.set_init_args_kwargs(ipt)
        for ico in tasks_on_this_ipt.keys():
            if self.run_task:
                try:
                    args = [ipt, ico, *stax]
                    task = loop.create_task(
                        coromask(
                            self.process_sta_task,
                            args, sta_kwargs,
                            simple_fargs_out)
                    )
                    task.add_done_callback(
                        functools.partial(renew,
                                          task,
                                          self.process_sta_task,
                                          simple_fargs_out)
                    )
                    tasks.append(task)
                except Exception as ex:
                    print(
                        "Error en collect_task, gather stations, process_sta(task) %s, error %s"
                        % (ipt, ex))
                    print(ex)
                    raise ex

            # add if exists the other tasks
            try:
                if self.n2s:
                    self.n2s_coro = self.n2s.get('coro')
                    n2s_args = self.n2s.get('args')
                    n2s_args.insert(0, ipt)
                    args = [ipt, ico, *n2s_args]
                    task = loop.create_task(
                        coromask(
                            self.process_sta_task_n2s,
                            args,
                            simple_fargs_out)
                    )
                    task.add_done_callback(
                        functools.partial(renew,
                                          task,
                                          self.process_sta_task_n2s,
                                          simple_fargs_out)
                    )
                    tasks.append(task)
            except Exception as ex:
                print(
                    "Error en collect_task, gather stations, net2service(task) %s, error %s"
                    % (ipt, ex))
                print(ex)
                raise ex

            try:
                if self.s2n:
                    self.s2n_coro = self.s2n.get('coro')
                    s2n_args = self.s2n.get('args')
                    s2n_args.insert(0, ipt)
                    args = [ipt, ico, *s2n_args]
                    task = loop.create_task(
                        coromask(
                            self.process_sta_task_s2n,
                            args,
                            simple_fargs_out)
                    )
                    task.add_done_callback(
                        functools.partial(renew,
                                          task,
                                          self.process_sta_task_s2n,
                                          simple_fargs_out)
                    )
                    tasks.append(task)
            except Exception as exec:
                print(
                    "Error en collect_task, gather stations, service2net(task) %s, error %s"
                    % (ipt, exec))
                print(exec)
                raise exec
        try:
            args = [ipt]
            kwargs = {}
            task = loop.create_task(
                coromask(
                    self.process_sta_manager,
                    args, kwargs,
                    simple_fargs_out)
            )
            task.add_done_callback(
                functools.partial(renew,
                                  task,
                                  self.process_sta_manager,
                                  simple_fargs_out)
            )
            tasks.append(task)
        except Exception as exec:
            print("Error en collect_task, manager %s, error %s" % (ipt, exec))
            print(exec)
            raise exec
        bprint("Loop is running yet? IPT->%s" % ipt)
        rprint(loop.is_running())
        if not loop.is_running():
            loop.run_forever()
