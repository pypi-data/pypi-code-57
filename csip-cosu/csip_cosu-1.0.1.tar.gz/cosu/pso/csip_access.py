from cosu import utils
from csip import Client
import queue


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
            # for i, value in enumerate(x):
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
                cost = utils.calc_cost(res, objfunc)

                if full_trace is not None:
                    all_params = {}
                    # for i, value in enumerate(x):
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
