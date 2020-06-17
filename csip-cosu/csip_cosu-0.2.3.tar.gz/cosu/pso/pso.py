from ..utils import utils
from .csip_access import csip_worker
from pyswarms.single.global_best import GlobalBestPSO
from os import path
from threading import Thread
import numpy as np
import copy
import datetime
import queue


def eval_cost(x, step_param_names, step_objfunc, calib_params, req_queue,
              files, url, param):
    cost = np.ones(len(x[:, 0]))
    res_queue = queue.Queue()

    print('   ', end='', flush=True)

    # submit for processing
    for i_particle, v in enumerate(x[:, 0]):
        req_queue.put((i_particle, x, step_param_names, calib_params, step_objfunc, res_queue))

    # wait for the cost value to come back
    for i, v in enumerate(x[:, 0]):
        (i_particle, p_cost) = res_queue.get()
        cost[i_particle] = p_cost
        res_queue.task_done()

    res_queue.join()
    print(flush=True)
    return cost


def global_best(steps, rounds, args, n_particles, iters, options, n_threads=4, rtol=0.001, ftol=-np.inf,
                full_trace=None):
    """Performs a stepwise particle swarm optimization

        Parameters
        ----------
        steps : dict
            step definitions
        rounds : tuple
            round definition,  (min,max)
        args : dict
            static service args
        n_particles : int
            number of particles
        iters : int
            number of iterations
        options : dict
            PSO options (see pyswarms)
        n_threads : int
            size of thread pool (default: 4)
        rtol : float
            percentage of change of sum(best_cost) between rounds for
            convergence. Default is :code:`0.001` (0.1 percent)
        ftol : float
            PSO tolerance
        full_trace : Array
            trace of all runs list of tuples
            first is dictionary of parameter names to parameter values
            second is the cost value
        Returns
        -------
        tuple
            optimizer, best,  all PSO optimizer, the global best.
    """

    utils.check_url(args['url'])

    min_rounds = 1
    if type(rounds) == tuple:
        min_rounds = rounds[0]
        max_rounds = rounds[1]
    else:
        max_rounds = rounds

    if min_rounds < 1:
        raise Exception('min rounds >= 1 expected, was "{}"'.format(min_rounds))

    if max_rounds > 20:
        raise Exception('max rounds <= 20 expected, was "{}"'.format(max_rounds))

    best_cost = np.ones(len(steps))
    optimizer = np.empty(len(steps), dtype=object)

    # trace of steps info
    step_trace = {}
    # best round cost
    best_round_cost = 1000

    req_queue = queue.Queue()

    done = False
    thread_pool = []
    for thread_no in range(n_threads):
        worker = Thread(target=csip_worker, args=(req_queue, thread_no, lambda: done,
                                             full_trace, args['url'], args['files'], args['param']))
        thread_pool.append(worker)
        worker.start()

    start_time = datetime.datetime.now()
    for r in range(max_rounds):
        no_improvement = np.full(len(steps), True)
        for s, step in enumerate(steps):

            # check if forced exit.
            if path.exists("stop"):
                print('\n>>>>> stop file found, exit now.')
                break

            param_names, bounds, objfunc = utils.get_step_info(steps, s)
            # maybe clone args?
            args['step_param_names'] = param_names
            args['step_objfunc'] = objfunc
            # get calibrated parameter from all other steps
            args['calib_params'] = utils.get_calibrated_params(steps, s)

            args['req_queue'] = req_queue

            # create optimizer in the first round.
            if optimizer[s] is None:
                optimizer[s] = GlobalBestPSO(n_particles, len(param_names),
                                             options=options, bounds=bounds, ftol=ftol)
            print('\n>>>>> R{}/S{}  particle params: {}  calibrated params: {}\n'.format(r + 1, s + 1, param_names,
                                                                                         args['calib_params']))

            # perform optimization
            cost, pos = optimizer[s].optimize(eval_cost, iters=iters, **args)

            # capture the best cost
            # if cost < best_cost[s] and np.abs(cost - best_cost[s]) > rtol:
            if cost < best_cost[s]:
                best_cost[s] = cost
                no_improvement[s] = False
                utils.annotate_step(best_cost[s], pos, steps, s)

            print('\n     Step summary, best particle values: {} '.format(pos))

            key = "r{}s{}".format(r + 1, s + 1)
            step_trace[key] = copy.deepcopy(steps)

            # print(json.dumps(steps, sort_keys=False, indent=2))

        round_cost = np.sum(best_cost)
        # if no improvement in all steps, break out of rounds prematurely
        # but start checking only after min_rounds
        # if (r + 1 >= min_rounds) and all(no_improvement):
        rel_round_tol = 1 - round_cost / best_round_cost

        print('\n  Round summary - round_cost:{}, step_costs: {}, step improvement:{}'
              .format(round_cost, best_cost, np.invert(no_improvement)))
        print('\n  Progress -  best_round_cost:{}, rel_round_tol:{}, rtol:{}'
              .format(best_round_cost, rel_round_tol, rtol))

        if (r + 1 >= min_rounds) and 0 <= rel_round_tol < rtol:
            break

        if round_cost < best_round_cost:
            best_round_cost = round_cost

    end_time = datetime.datetime.now()
    elapsed = str(end_time - start_time)

    print('Done in {} after {} out of {} rounds'.format(elapsed, r + 1, max_rounds))

    done = True
    for worker in thread_pool:
        worker.join()

    step_trace['rounds'] = r + 1
    step_trace['steps'] = len(steps)
    step_trace['iters'] = iters
    step_trace['particles'] = n_particles
    step_trace['time'] = elapsed

    return optimizer, step_trace
