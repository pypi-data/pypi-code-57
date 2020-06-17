import threading
from cosu import utils
from csip import Client

import queue


class ServiceClient(threading.Thread):

    def __init__(self, url: str, i_particle: int, cost, x,
                 arg_params, step_param_names, step_objfunc, calib_params, files,
                 full_trace):
        threading.Thread.__init__(self)
        self.i_particle = i_particle
        self.url = url
        self.cost = cost
        self.x = x
        self.files = files
        self.arg_params = arg_params
        self.step_param_names = step_param_names
        self.objfunc = step_objfunc
        self.calib_params = calib_params
        self.full_trace = full_trace

    def run(self):
        c = Client()
        # static params (from args)
        for param in self.arg_params:
            c.add_data(param['name'], param['value'])

        # particle params  (generated from steps)
        for i, value in enumerate(self.x[self.i_particle, :]):
            c.add_data(self.step_param_names[i], value)

        # other, previously calibrated params (other steps)
        for name, value in self.calib_params.items():
            c.add_data(name, value)

        # objective function info
        for of in self.objfunc:
            c.add_data(of['name'], (of['data'][0], of['data'][1]))

        print('.', end='', flush=True)
        print(c)
        res = c.execute(self.url, files=self.files)
        print(res)
        print(u'\u2714', end='', flush=True)
        try:
            self.cost[self.i_particle] = self.get_of(res)
        except:
            print(res)

        if self.full_trace is not None:
            all_params = {}
            for i, value in enumerate(self.x[self.i_particle, :]):
                all_params[self.step_param_names[i]] = value
            for name, value in self.calib_params.items():
                all_params[name] = value
            self.full_trace.append((all_params, self.cost[self.i_particle]))

    def get_of(self, res):
        """Compute aggregated  objective function value."""

        cost = 0.0
        for of in self.objfunc:
            of_val = res.get_data_value(of['name'])
            cost += utils.NORM[of['name']](of_val) * of.get('weight', 1.0)
        return cost


def csip_worker(reqq: queue.Queue, thread_no: int, stop, full_trace,
                url, files, arg_params) -> None:
    while not stop():
        try:
            (i_particle, x, step_param_names, calib_params, objfunc, resq) = reqq.get(True, 0.5)
            # print(thread_no, i_particle)

            c = Client()
            # static params (from args)
            for param in arg_params:
                c.add_data(param['name'], param['value'])

            # particle params  (generated from steps)
            for i, value in enumerate(x[i_particle, :]):
                c.add_data(step_param_names[i], value)

            # other, previously calibrated params (other steps)
            for name, value in calib_params.items():
                c.add_data(name, value)

            # objective function info
            for of in objfunc:
                c.add_data(of['name'], (of['data'][0], of['data'][1]))

            print('.', end='', flush=True)

            try:
                # print(c)
                res = c.execute(url, files=files)
                # print(res)
                print(u'\u2714', end='', flush=True)
                cost = utils.get_cost(res, objfunc)

                if full_trace is not None:
                    all_params = {}
                    for i, value in enumerate(x[i_particle, :]):
                        all_params[step_param_names[i]] = value
                    for name, value in calib_params.items():
                        all_params[name] = value
                    full_trace.append((all_params, cost))

                resq.put((i_particle, cost))
            except:
                print(res)
            reqq.task_done()
        except queue.Empty:
            continue
