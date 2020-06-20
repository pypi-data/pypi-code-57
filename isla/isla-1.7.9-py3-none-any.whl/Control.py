import os
import itertools
import copy
import warnings
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from matplotlib.patches import Patch

from .LoadFollow import LoadFollow
from .NullComp import NullComp
from .Component import Component
from .LoadComponent import LoadComponent
from .IntermittentComponent import IntermittentComponent
from .StorageComponent import StorageComponent
from .DispatchableComponent import DispatchableComponent
from .SinkComponent import SinkComponent
from .GridComponent import GridComponent
from .SupplementaryComponent import SupplementaryComponent
from .Connector import Connector
from .LoadConnector import LoadConnector
from .IntermittentConnector import IntermittentConnector
from .StorageConnector import StorageConnector
from .DispatchableConnector import DispatchableConnector
from .SinkConnector import SinkConnector
from .GridConnector import GridConnector
from .SupplementaryConnector import SupplementaryConnector

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class Control(object):
    """Power system controller module.

    Parameters
    ----------
    comp_list : list
        List of initialized component objects.
    dt : float, optional
        Size of one timestep [h] (default: 1)
    t_span : float, optional
        Duration of the simulation [h] (default: 8760)

    """

    def __init__(self, comp_list, dt=1, t_span=8760):
        """Initializes the base class."""

        # store parameters
        self.comp_list = comp_list  # list of components
        self.dt = dt  # length of timestep [h]
        self.t_span = t_span  # length of simulation [h]

        # calculate number of simulation points
        self.nt = int(np.ceil(t_span/dt))

        # initialize data storage
        self.size = {}  # dict of component sizes
        self.algo = None  # dispatch algorithm
        self.disc = 0
        self.yr_proj = 0
        self.proj_capex = 0
        self.proj_caprt = 0
        self.proj_opex = 0
        self.time_ser = dict(  # time series data for power
            (i, np.zeros(self.nt)) for i in comp_list
        )
        self.time_sersoc = dict(  # time series data for SOC
            (i, np.ones(self.nt)) for i in comp_list
            if isinstance(i, StorageComponent)
        )

        # initialize metrics arrays
        self.npc = np.array([])  # NPC
        self.lcoe = np.array([])  # LCOE
        self.lcow = np.array([])  # LCOW
        self.re_frac = np.array([])  # RE-share
        self.lolp = np.array([])  # LOLP

        # initialize advanced economics metrics
        self.is_econ = False  # if advanced econ has been initialized
        self.cost_elec = 0
        self.cost_sub = 0
        self.tax_rate = 0
        self.salv_rate = 0
        self.depr = False
        self.cf_dict = {}
        self.irr = 0
        self.npv = 0
        self.ucme = 0
        self.cost_elec = 0
        self.cost_ctot = 0
        self.cost_otot = 0
        self.cost_rtot = 0
        self.cost_ftot = 0
        self.rev_tot = 0

        # initialize capacity factor
        self.capfac = {}

        # initialize maintenance feasibility
        self.sched_feas = None

    def simu(
        self, size, spin_res=0.1, yr_proj=20.0, disc=0.1,
        proj_capex=0.0, proj_caprt=0.0, proj_opex=0.0,
        algo=LoadFollow, **kwargs
    ):
        """Simulates a scenario given a set of sizes and calculates the LCOE.

        Parameters
        ----------
        size : dict
            Sizes [kW] or [kWh] of the components. Use component objects as
            keys and sizes as values.
        spin_res : float
            Spinning reserve.
        yr_proj : float
            Project lifetime [yr].
        disc : float
            Discount rate.
        proj_capex : float
            Capital expenses [USD] of the project.
        proj_caprt : float
            Capital expenses of project as ratio of component CapEx.
        proj_opex : float
            Fixed yearly operating expenses [USD/yr] of the project.
        algo : Dispatch
            The dispatch algorithm to be used.

        Other Parameters
        ----------------
        do_inval : bool
            True if invalid cases should have nan LCOE and RE-share.
        print_prog : bool
            True if calculation progress should be printed.
        print_out : bool
            True if results should be printed. Invokes res_print().

        Notes
        -----
        Sets LCOE to nan when the size combination is infeasible.

        """
        # get keyword arguments
        do_inval = kwargs.pop('do_inval', True)
        print_prog = kwargs.pop('print_prog', True)
        print_out = kwargs.pop('print_out', True)
        self.size = size
        self.disc = disc
        self.yr_proj = yr_proj
        self.proj_capex = proj_capex
        self.proj_caprt = proj_caprt
        self.proj_opex = proj_opex

        # initialize for console output
        t0 = time.time()  # time
        mark = np.arange(0, self.nt, self.nt//10)

        # initialize dispatch algorithm
        al = algo(self.comp_list, self.dt, self.t_span, size, spin_res)

        # perform simulation
        for n in range(self.nt):
            al._step()  # increment simulation
            for cp in self.comp_list:
                self.time_ser[cp][n] = cp.pow  # record power at timestep
                if isinstance(cp, StorageComponent):
                    self.time_sersoc[cp][n] = cp.soc  # record SOC at timestep
            if print_prog and n in mark:  # display progress
                print(
                    'Simulation Progress: {:.0f}%'.format((n+1)*100/self.nt),
                    flush=True
                )

        # store completed dispatch algorithm object
        self.algo = al

        # calculate metrics
        self.npc = Control._npc(
            al, yr_proj, disc, proj_capex, proj_caprt, proj_opex
        )[0]
        self.lcoe = Control._lcoe(
            al, yr_proj, disc, proj_capex, proj_caprt, proj_opex
        )[0]
        self.lcow = Control._lcow(
            al, yr_proj, disc, proj_capex, proj_caprt, proj_opex
        )[0]

        # calculate RE-share
        pow_ldts = np.zeros(self.nt)  # time-series data of total load
        enr_tot = np.zeros(self.nt)  # total energy
        enr_re = np.zeros(self.nt)  # total renewable energy
        for cp in self.comp_list:
            if isinstance(cp, LoadComponent):
                pow_ldts += self.time_ser[cp]  # time series data of total load
        for cp in self.comp_list:
            if not isinstance(cp, LoadComponent) and cp.is_re is not None:
                ld_def = np.maximum(pow_ldts-enr_tot, 0)  # load deficit
                enr_tot += np.minimum(  # add to energy
                    self.time_ser[cp], ld_def  # do not go over load
                )*self.dt
                if cp.is_re:  # add to RE energy
                    enr_re += np.minimum(  # add to energy
                        self.time_ser[cp], ld_def  # do not go over load
                    )*self.dt
        self.re_frac = np.sum(enr_re)/np.sum(enr_tot)

        # check if invalid
        if do_inval and not al.feas:
            self.lcoe = np.nan
            self.re_frac = np.nan

        # print results
        if print_prog:
            t1 = time.time()
            print('Simulation completed in {:.4f} s.'.format(t1-t0))
        if print_out:
            self.res_print()

    def opt(
        self, spin_res=0.1, yr_proj=20.0, disc=0.1,
        proj_capex=0.0, proj_caprt=0.0, proj_opex=0.0, size_max=None,
        size_min=None, iter_simu=10, iter_npv=3, algo=LoadFollow, **kwargs
    ):
        """Set component sizes such that NPC is optimized.

        Parameters
        ----------
        spin_res : float
            Spinning reserve.
        yr_proj : float
            Project lifetime [yr].
        disc : float
            Discount rate.
        proj_capex : float
            Capital expenses [USD] of the project.
        proj_caprt : float
            Project capital expenses as a fraction of the component CapEx.
        proj_opex : float
            Fixed yearly operating expenses [USD/yr] of the project.
        size_max : dict
            Maximum size constraint. Use the component object as keys and the
            size constraint as values.
        size_min : dict
            Minimum size constraint. Use the component object as keys and the
            size constraint as values.
        iter_simu : int
            Number of cases to simulate simultaneously.
        iter_npv : int
            Number of iterations to find the NPC.

        Other Parameters
        ----------------
        im_range : tuple of float or str
            Boundaries of the search space for the sizes of intermittent power
            components. Input as (min, max). Set to 'auto' to automatically
            find the search space.
        st_range : tuple of float or str
            Boundaries of the search space for the sizes of energy storage
            components. Input as (min, max). Set to 'auto' to automatically
            find the search space.
        dp_range : tuple of float or str
            Boundaries of the search space for the sizes of dispatchable power
            components. Input as (min, max). Set to 'auto' to automatically
            find the search space.
        sk_range : tuple of float or str
            Boundaries of the search space for the sizes of sink power
            components. Input as (min, max). Set to 'auto' to automatically
            find the search space.
        gd_range : tuple of float or str
            Boundaries of the search space for the size of the grid. Input as
            (min, max). Set to 'auto' to automatically find the search space.
        su_range : tuple of float or str
            Boundaries of the search space for the sizes of supplementary power
            components. Input as (min, max). Set to 'auto' to automatically
            find the search space.
        size_fix : dict
            Specify fixed sizes of components.
        batch_size : int
            Number of simulations to be carried out simultaneously. Prevents
            the program from consuming too much memory.
        print_npv : bool
            True if opimization progress should be printed.
        print_simu : bool
            True if simulation progress should be printed.
        print_res : bool
            True if results should be printed.

        """
        # get keyword arguments
        im_range = kwargs.pop('im_range', 'auto')
        st_range = kwargs.pop('st_range', 'auto')
        dp_range = kwargs.pop('dp_range', 'auto')
        sk_range = kwargs.pop('sk_range', 'auto')
        gd_range = kwargs.pop('gd_range', 'auto')
        su_range = kwargs.pop('su_range', 'auto')
        size_fix = kwargs.pop('size_fix', {})
        batch_size = kwargs.pop('batch_size', 10000)
        print_prog = kwargs.pop('print_prog', True)
        print_out = kwargs.pop('print_out', True)
        self.proj_capex = proj_capex
        self.proj_caprt = proj_caprt
        self.proj_opex = proj_opex
        self.disc = disc
        self.yr_proj = yr_proj

        # initialize for console output
        t0 = time.time()  # time

        # replace constraints with empty dict if there are none
        if size_max is None:
            size_max = {}
        if size_min is None:
            size_min = {}

        # check if adj or grid components are present
        has_dp = any(
            isinstance(i, DispatchableComponent) for i in self.comp_list
        )
        has_gd = any(isinstance(i, GridComponent) for i in self.comp_list)
        if has_dp or has_gd:  # no adjustable or grid components
            small_size = True  # use smaller search space
        else:
            small_size = False  # use larger search space

        # use smaller search space if adj or grid is present
        if small_size:  # based on peak
            approx_powmax = sum(  # sum of peak loads
                i.approx_powmax for i in self.comp_list
                if isinstance(i, LoadComponent)
            )
            auto_range = (0, approx_powmax*3.5)
        else:  # based on daily consumption
            approx_enrtot = sum(  # total annual load
                i.approx_enrtot for i in self.comp_list
                if isinstance(i, LoadComponent)
            )
            auto_range = (0, approx_enrtot*2/365)

        # determine number of components to be sized:
        num_comp = sum(  # load is not counted
            1 for i in self.comp_list if not isinstance(i, LoadComponent)
        )-len(size_fix)  # subtract fixed sizes

        # initialize
        rng_list = [im_range, st_range, dp_range, sk_range, gd_range, su_range]
        rng_dict = {}  # dict with ranges
        cls_list = [  # list of component classes
            IntermittentComponent, StorageComponent, DispatchableComponent,
            SinkComponent, GridComponent, SupplementaryComponent
        ]

        # assign auto search spaces
        for i in range(6):
            if rng_list[i] == 'auto':  # replace auto ranges
                rng_list[i] = auto_range

        # create dict of ranges
        for cp in self.comp_list:
            for i in range(6):
                if isinstance(cp, cls_list[i]):  # sort by component type
                    rng_dict[cp] = rng_list[i]  # copy the range

        # make a copy of the original ranges
        orig_dict = copy.deepcopy(rng_dict)

        # calculate batch size
        num_case_all = iter_simu**num_comp  # total number of cases
        num_batch, num_rem = divmod(num_case_all, batch_size)

        # initialize for subset iteration
        size_dict = {}  # dict with sizes
        sub_dict = {}  # dict with subset of sizes
        opt_dict = {}  # dict with optimum sizes
        opt_npv = np.inf  # optimum NPC

        # begin iteration
        for i in range(0, iter_npv):  # number of optimization loops

            # convert ranges into sizes
            for cp in rng_dict:

                # determine if size is fixed
                if cp in list(size_fix.keys()):
                    size_dict[cp] = np.array([size_fix[cp]])

                    continue

                # determine upper bound of component
                if cp in list(size_max.keys()):
                    ub = np.min([rng_dict[cp][1], size_max[cp]])
                else:
                    ub = rng_dict[cp][1]

                # determine lower bound of component
                if cp in list(size_min.keys()):
                    lb = np.max([rng_dict[cp][0], size_min[cp]])
                else:
                    lb = rng_dict[cp][0]

                # create range
                size_dict[cp] = np.linspace(lb, ub, num=iter_simu)

            # create generator object that dispenses size combinations
            gen = (itertools.product(*list(size_dict.values())))

            # begin iteration per batch
            for j in range(num_batch+1):

                # subset initial list of sizes
                if j == num_batch:  # last batch
                    if num_rem == 0:  # no remaining cases
                        break
                    sub_arr = np.array(list(
                        next(gen) for i in range(0, num_rem)
                    ))  # extracts combinations
                else:
                    sub_arr = np.array(list(
                        next(gen) for i in range(0, batch_size)
                    ))  # extracts combinations

                # assign sizes to subset array
                comp = 0
                for cp in size_dict:
                    sub_dict[cp] = sub_arr[:, comp]
                    comp += 1

                # initialize dispatch algorithm
                # note: this modifies sub_dict by ading NullComps
                al = algo(
                    self.comp_list, self.dt, self.t_span, sub_dict, spin_res
                )

                # perform simulation
                for hr in range(0, self.nt):
                    al._step()

                # calculate NPC
                npc = Control._npc(
                    al, yr_proj, disc, proj_capex, proj_caprt, proj_opex
                )

                # determine invalid cases
                inval = np.logical_not(al.feas)

                # continue with next loop if all invalid
                if np.all(inval):
                    continue

                # find array index of lowest valid NPC
                npc[inval] = np.nan
                opt_ind = np.nanargmin(npc)

                # remove NullComp from sub_dict
                sub_dict = dict(
                    (i, j) for i, j in zip(sub_dict.keys(), sub_dict.values())
                    if not isinstance(i, NullComp)
                )

                # check if NPC of this subset is lower than before
                if npc[opt_ind] < opt_npv:
                    opt_npv = npc[opt_ind]  # set optimum NPC
                    for cp in sub_dict:  # set optimum sizes
                        opt_dict[cp] = sub_dict[cp][opt_ind]

            # prepare new list
            for cp in rng_dict:
                if cp not in size_fix:
                    sep = size_dict[cp][1]-size_dict[cp][0]
                    lb = np.maximum(opt_dict[cp]-sep, 0)  # new lower bound
                    ub = np.maximum(opt_dict[cp]+sep, 0)  # new upper bound
                    rng_dict[cp] = (lb, ub)

            # output progress
            if print_prog:
                prog = (i+1)*100/iter_npv
                out = 'Optimization progress: {:.2f}%'.format(prog)
                print(out, flush=True)

        # set components to optimum
        self.simu(
            opt_dict, spin_res, yr_proj, disc,
            proj_capex, proj_caprt, proj_opex, algo,
            print_prog=False, print_out=False
        )

        # print results
        if print_prog:
            t1 = time.time()
            out = 'Optimization completed in {:.4f} min.'.format((t1-t0)/60)
            print(out, flush=True)
        if print_out:
            self.res_print()

    def sched(self, sched_dict, algo=LoadFollow, **kwargs):
        """Checks if a proposed maintenance schedule is feasible.

        Parameters
        ----------
        sched_dict : dict
            A dict with the components as keys and the schedule as an ndarray
            as values. The ndarray should have 0 values when maintenance is
            done and 1 elsewhere.
        algo : Dispatch
            The dispatch algorithm to be used.

        Other Parameters
        ----------------
        print_prog : bool
            True if calculation progress should be printed.
        print_out : bool
            True if results should be printed.

        Notes
        -----
        This calculation assumes hourly timesteps for one representative year.
        """
        # get keyword arguments
        print_prog = kwargs.pop('print_prog', True)
        print_out = kwargs.pop('print_out', True)

        # get relevant data from last algorithm
        dt = self.algo.dt
        t_span = self.algo.t_span
        size = self.algo.size

        # initialize for console output
        t0 = time.time()  # time
        mark = np.arange(0, self.nt, self.nt//10)

        # initialize dispatch algorithm
        al = algo(self.comp_list, dt, t_span, size, 0)

        # initialize
        sched_comp = list(sched_dict.keys())

        # perform simulation
        for n in range(self.nt):

            # turn on or off component
            for cp in sched_comp:
                cp.dist_var = sched_dict[cp][n]

            # increment simulation
            al._step()

            # record data
            for cp in self.comp_list:
                self.time_ser[cp][n] = cp.pow  # record power at timestep
                if isinstance(cp, StorageComponent):
                    self.time_sersoc[cp][n] = cp.soc  # record SOC at timestep

            # display progress
            if print_prog and n in mark:
                print(
                    'Simulation Progress: {:.0f}%'.format((n+1)*100/self.nt),
                    flush=True
                )

        # store schedule feasibility
        self.sched_feas = al.feas

        # print results
        if print_prog:
            t1 = time.time()
            print('Simulation completed in {:.4f} s.'.format(t1-t0))
        if print_out:
            if al.feas:
                print('Maintenance schedule is feasible')
            else:
                print('Maintenance schedule is not feasible')

    def rel(
        self, size, num_pts=10000, spin_res=0.1,
        algo=LoadFollow, **kwargs
    ):
        """Simulates a scenario given a set of sizes and calculates the LCOE.

        Parameters
        ----------
        size : dict
            Sizes [kW] or [kWh] of the components. Use component objects as
            keys and sizes as values.
        num_pts : int
            Number of points to use for Monte Carlo.
        spin_res : float
            Spinning reserve.
        algo : Dispatch
            The dispatch algorithm to be used.

        Other Parameters
        ----------------
        batch_max : int
            Maximum number of simulations to be carried out simultaneously.
            Prevents the program from consuming too much memory.
        do_inval : bool
            True if invalid cases should have nan LCOE and RE-share.
        print_prog : bool
            True if calculation progress should be printed.
        print_out : bool
            True if results should be printed. Invokes res_print().
        tol : float
            Tolerance when checking if power meets the load.

        """
        # get keyword arguments
        max_size = kwargs.pop('batch_max', 10000)
        print_prog = kwargs.pop('print_prog', True)
        print_out = kwargs.pop('print_out', True)
        tol = kwargs.pop('tol', 1e-2)
        self.disc = disc
        self.yr_proj = yr_proj

        # initialize for console output
        t0 = time.time()  # time
        mark = np.arange(0, self.nt, self.nt//10)

        # modify size array
        size_dict = {}
        for cp in size:
            size_dict[cp] = size[cp]*np.ones(num_pts)

        # initialize dispatch algorithm
        al = algo(self.comp_list, self.dt, self.t_span, size, spin_res)

        # begin simulations
        lolp = np.zeros(num_pts)
        for hr in range(self.nt):

            # perform step
            al._step()

            # display progress
            if print_prog and hr in mark:
                print(
                    'Calculation Progress: {:.0f}%'.format((n+1)*100/self.nt),
                    flush=True
                )

        # divide by hours per year
        self.lolp = np.average(al.num_def)/sel.nt

        # print results
        if print_prog:
            t1 = time.time()
            print('Simulation completed in {:.4f} s.'.format(t1-t0))
        if print_out:
            self.res_print()

    def powflow_plot(
        self, time_range=(0, 168), fig_size=(12, 5),
        pow_lim='auto'
    ):
        """Generates a power flow of the system.

        Parameters
        ----------
        time_range : tuple, optional
            Range of times to plot [h]. (default: (0, 168))
        fig_size : tuple, optional
            Size of plot. (default: (12, 5))
        pow_lim : ndarray or 'auto'
            Limits for power axis. (default: 'auto')

        """
        # initialize dicts
        name_solid = {}  # dict of components and names
        color_solid = {}  # dict of components and colors
        pow_solid = {}  # dict of components and powers
        name_line = {}  # dict of components and names
        color_line = {}  # dict of components and colors
        pow_line = {}  # dict of components and powers
        soc_line = {}  # dict of components and SOC

        # get indeces of time range
        lb = int(np.floor(time_range[0]/self.dt))
        ub = int(np.ceil(time_range[1]/self.dt))

        # get names, colors, and value of each component
        for cp in self.comp_list:
            if cp.color_solid is not None:  # stacked graph for power sources
                name_solid[cp] = cp.name_solid
                color_solid[cp] = cp.color_solid
                pow_solid[cp] = self.time_ser[cp][lb:ub]
            if cp.color_line is not None:  # line graph for load and SOC
                if isinstance(cp, StorageComponent):  # storage has SOC
                    name_line[cp] = cp.name_line
                    color_line[cp] = cp.color_line
                    soc_line[cp] = self.time_sersoc[cp][lb:ub]
                if isinstance(cp, LoadComponent):  # load
                    name_line[cp] = cp.name_line
                    color_line[cp] = cp.color_line
                    pow_line[cp] = self.time_ser[cp][lb:ub]

        # generate x-axis (list of times)
        t_axis = np.linspace(lb*self.dt, ub*self.dt, num=ub-lb, endpoint=False)

        # create left axis for power
        fig, pow_axis = plt.subplots(figsize=fig_size)
        if pow_lim != 'auto':
            plt.ylim(pow_lim)

        # axes labels
        pow_axis.set_xlabel('Time [h]')
        pow_axis.set_ylabel('Power [kW]')

        # initialize
        plot_list = []  # list of plot objects
        name_list = []  # list of corresponding names

        # plot power sources (solid graphs)
        pow_stack = 0  # total power below the graph
        for cp in name_solid:

            # add to list of plots
            plot_list.append(
                pow_axis.fill_between(
                    t_axis, pow_stack,
                    pow_stack+pow_solid[cp],
                    color=color_solid[cp]
                )
            )

            # add to list of names
            name_list.append(name_solid[cp])

            # increase pow stack
            pow_stack = pow_stack+pow_solid[cp]

        # plot power sources (line graphs)
        for cp in pow_line:

            # add to list of plots
            line_plot = pow_axis.plot(
                t_axis, pow_line[cp], color=color_line[cp]
            )
            plot_list.append(line_plot[0])

            # add to list of names
            name_list.append(name_line[cp])

        # plot soc on right axis
        soc_axis = pow_axis.twinx()  # make right y-axis
        soc_axis.set_ylabel('SOC')
        soc_axis.set_ylim(0, 1.1)

        # plot lines that represent SOC's
        for cp in soc_line.keys():

            # add to list of plots
            line_plot = soc_axis.plot(
                t_axis, soc_line[cp], color=color_line[cp]
            )
            plot_list.append(line_plot[0])

            # add to list of names
            name_list.append(name_line[cp])

        # generate plot
        plt.legend(tuple(plot_list), tuple(name_list))
        plt.show()

    def powflow_csv(self, file):
        """Generates a .csv file with the power flow.

        Parameters
        ----------
        file : str
            Filename for output file.

        """
        # initialize array with powers
        pow_out = np.linspace(
            0, self.nt*self.dt, num=self.nt, endpoint=False
        ).reshape((self.nt, 1))

        # initialize headers
        pow_head = ['Time [h]']

        # get the names and values of each component
        for cp in self.comp_list:
            if cp.name_solid is not None:
                pow_head.append(cp.name_solid)  # append component
                pow_out = np.append(
                    pow_out, self.time_ser[cp].reshape((self.nt, 1)), axis=1
                )
            if cp.name_line is not None:
                if isinstance(cp, StorageComponent):  # storage has SOC
                    pow_head.append(cp.name_line)  # append battery SOC
                    pow_out = np.append(
                        pow_out, self.time_sersoc[cp].reshape((self.nt, 1)),
                        axis=1
                    )
                if isinstance(cp, LoadComponent):
                    pow_head.append(cp.name_line)  # append load
                    pow_out = np.append(
                        pow_out, self.time_ser[cp].reshape((self.nt, 1)),
                        axis=1
                    )

        pd.DataFrame(pow_out).to_csv(file, index=False, header=pow_head)

    def summary_csv(self, file):
        """Generates a .csv file with the sizes.

        Parameters
        ----------
        file : str
            Filename for output file.

        """
        # initialize file
        file_out = open(file, mode='w')

        # get the sizes of each component
        for cp in self.comp_list:
            if not isinstance(cp, LoadComponent):
                file_out.writelines(
                    '{},{}\n'.format(cp.name_solid, cp.size[0])
                )

        # basic parameters
        if self.npc.size != 0 and not np.isnan(self.npc):
            file_out.writelines('NPC [10^6 USD],{}\n'.format(self.npc/1e6))
        if self.lcoe.size != 0 and not np.isnan(self.lcoe):
            file_out.writelines('LCOE [USD/kWh],{}\n'.format(self.lcoe))
        if self.lcow.size != 0 and not np.isnan(self.lcow):
            file_out.writelines('LCOW [USD/m3],{}\n'.format(self.lcow))
        if self.re_frac.size != 0 and not np.isnan(self.re_frac):
            file_out.writelines('RE-Share,{}\n'.format(self.re_frac))
        if self.lolp.size != 0 and not np.isnan(self.lolp):
            file_out.writelines('LOLP,{}\n'.format(self.lolp))

        # other parameters
        if self.is_econ:
            if self.cost_ctot.size != 0 and not np.isnan(self.cost_ctot):
                file_out.writelines(
                    'CapEx [10^6 $],{}\n'.format(self.cost_ctot/1e6)
                )
            if self.cost_otot.size != 0 and not np.isnan(self.cost_otot):
                file_out.writelines(
                    'OpEx [10^6 $],{}\n'.format(self.cost_otot/1e6)
                )
            if self.cost_rtot.size != 0 and not np.isnan(self.cost_rtot):
                file_out.writelines(
                    'RepEx [10^6 $],{}\n'.format(self.cost_rtot/1e6)
                )
            if self.cost_ftot.size != 0 and not np.isnan(self.cost_ftot):
                file_out.writelines(
                    'FuelEx [10^6 $],{}\n'.format(self.cost_ftot/1e6)
                )
            if self.rev_tot.size != 0 and not np.isnan(self.rev_tot):
                file_out.writelines(
                    'Revenue [10^6 $],{}\n'.format(self.rev_tot/1e6)
                )
            if self.npv.size != 0 and not np.isnan(self.npv):
                file_out.writelines('NPV [10^6 $],{}\n'.format(self.npv/1e6))
            if self.irr.size != 0 and not np.isnan(self.irr):
                file_out.writelines('IRR,{}\n'.format(self.irr[0]))
            if self.ucme.size != 0 and not np.isnan(self.ucme):
                file_out.writelines('UCME,{}\n'.format(self.ucme[0]/1e6))

    def res_print(self):
        """Prints the sizes and calculated parameters in the console."""

        # print results
        print('SYSTEM SUMMARY')

        # sizes
        print('Sizes [kW] or [kWh]:')
        for cp in self.comp_list:
            if not isinstance(cp, LoadComponent):
                if np.atleast_1d(cp.size).size == 1:  # one scenario only
                    print(
                        '    {:15}: {:>12.4f}'
                        .format(cp.name_solid, cp.size[0])
                    )
                else:  # multiple scenarios simulated
                    print('    {:15}: '.format(cp.name_solid)+str(cp.size[0]))

        # other parameters
        print('Parameters:')
        if self.npc.size != 0 and not np.isnan(self.npc):
            print('    NPC [10^6 USD] : {:>12.4f}'.format(self.npc/1e6))
        if self.lcoe.size != 0 and not np.isnan(self.lcoe):
            print('    LCOE [USD/kWh] : {:>12.4f}'.format(self.lcoe))
        if self.lcow.size != 0 and not np.isnan(self.lcow):
            print('    LCOW [USD/m3]  : {:>12.4f}'.format(self.lcow))
        if self.re_frac.size != 0 and not np.isnan(self.re_frac):
            print('    RE-Share       : {:>12.4f}'.format(self.re_frac))
        if self.lolp.size != 0 and not np.isnan(self.lolp):
            print('    LOLP           : {:>12.4f}'.format(self.lolp))

    def econ_calc(
        self, cost_elec='lcoe', cost_sub=0, tax_rate=0,
        salv_rate=0, depr=False, print_out=True, **kwargs
    ):
        """Performs rigorous economic calculations.

        Parameters
        ----------
        cost_elec : float or str
            Electricity rate [$/kWh] for IRR calculations. Set to 'lcoe' to
            set electricity rate to LCOE (IRR = discount rate).
        cost_sub : float
            Subsidized electricity cost [$/kWh].
        tax_rate : float
            Tax on income.
        salv_rate : float
            Salvage value as percentage of capital cost.
        depr : bool
            If True, then depreciation will be calculated.
        print_out : bool
            True if results should be printed. Invokes res_print().

        """
        # get electricity rate
        if cost_elec == 'lcoe':
            cost_elec = self.lcoe

        # store variables
        self.cost_elec = cost_elec
        self.cost_sub = cost_sub
        self.tax_rate = tax_rate
        self.salv_rate = salv_rate
        self.depr = depr

        # reset cashflow variables
        self.cost_ctot = 0
        self.cost_otot = 0
        self.cost_rtot = 0
        self.cost_ftot = 0
        cost_cf = 0

        # iterate for every component and get cashflows
        for cp in self.comp_list:
            if not isinstance(cp, (LoadComponent, NullComp)):

                # get capex, opex, repex
                capex_cf = cp.cost_c.flatten()
                opex_cf = (cp.cost_of+cp.cost_ov+cp.cost_ou).flatten()
                repex_cf = cp.cost_r.flatten()

                # check if fuel is present
                if isinstance(cp.cost_f, np.ndarray):
                    fuel_cf = cp.cost_f.flatten()
                else:
                    fuel_cf = np.zeros(int(self.yr_proj)+1)

                # add to total costs
                self.cost_ctot += np.sum(capex_cf)
                self.cost_otot += np.sum(opex_cf)
                self.cost_rtot += np.sum(repex_cf)
                self.cost_ftot += np.sum(fuel_cf)
                cost_cf += capex_cf+opex_cf+repex_cf+fuel_cf

                # create subdict
                self.cf_dict[cp] = {
                    'CapEx': capex_cf, 'OpEx': opex_cf,
                    'RepEx': repex_cf, 'FuelEx': fuel_cf
                }

        # get project capex
        proj_cap_tot = self.proj_capex+self.proj_caprt*self.cost_ctot
        proj_cap_cf = np.append([proj_cap_tot], np.zeros(int(self.yr_proj)))
        self.cost_ctot += proj_cap_tot

        # get project opex
        proj_opex_cf = self.proj_opex/(
            (1+self.disc)**np.arange(self.yr_proj+1)
        )
        proj_opex_cf[0] = 0
        self.cost_otot += np.sum(proj_opex_cf)

        # get revenue
        rev_cf = self.algo.ld.enr_tot*cost_elec*(1-tax_rate)/(
            (1+self.disc)**np.arange(self.yr_proj+1)
        )
        rev_cf[0] = 0
        self.rev_tot = np.sum(rev_cf)

        # get depreciation
        depr_val = (1-salv_rate)*self.cost_ctot/self.yr_proj
        depr_cf = depr*tax_rate*depr_val/(
            (1+self.disc)**np.arange(self.yr_proj+1)
        )
        depr_cf[0] = 0

        # get salvage value
        salv_cf = np.zeros(int(self.yr_proj)+1)
        salv_cf[-1] = salv_rate*self.cost_ctot/((1+self.disc)**(self.yr_proj))

        # get NPV
        self.npv = self.rev_tot+np.sum(depr_cf+salv_cf)-self.npc

        # store cash flows
        self.cf_dict['Project'] = {'CapEx': proj_cap_cf, 'OpEx': proj_opex_cf}
        self.cf_dict['Revenue'] = rev_cf
        self.cf_dict['Depreciation'] = depr_cf
        self.cf_dict['Salvage'] = salv_cf
        cost_cf += proj_cap_cf+proj_opex_cf

        # get IRR
        if cost_elec >= self.lcoe:
            ann_inv = (1+self.disc)**np.arange(0, self.yr_proj+1)
            nomcf_tot = (rev_cf+depr_cf+salv_cf-cost_cf)*ann_inv

            def to_zero(disc):
                ann = 1/(1+disc)**np.arange(0, self.yr_proj+1)
                return np.sum(nomcf_tot*ann)

            self.irr = fsolve(to_zero, self.disc)
        else:
            self.irr = np.array([])

        # get UCME
        self.ucme = (cost_elec-cost_sub)*self.algo.ld.enr_tot

        # print output
        print('Parameters:')
        print('    CapEx [10^6$]  : {:>12.4f}'.format(self.cost_ctot/1e6))
        print('    OpEx [10^6$]   : {:>12.4f}'.format(self.cost_otot/1e6))
        print('    RepEx [10^6$]  : {:>12.4f}'.format(self.cost_rtot/1e6))
        print('    FuelEx [10^6$] : {:>12.4f}'.format(self.cost_ftot/1e6))
        print('    Revenue [10^6$]: {:>12.4f}'.format(self.rev_tot/1e6))
        print('    NPV [10^6$]    : {:>12.4f}'.format(self.npv/1e6))
        if self.irr.size != 0:
            print('    IRR            : {:>12.4f}'.format(self.irr[0]))
        print('    UCME [10^6$]   : {:>12.4f}'.format(self.ucme[0]/1e6))

        # econ calculations performed
        self.is_econ = True

    def capfac_calc(self):
        """Calculates capacity factors."""

        # print output
        print('Capacity Factor:')
        dis = self.algo
        for cp in dis.comp_list:
            if isinstance(cp, (IntermittentComponent, DispatchableComponent)):
                capfac = cp.enr_tot/(cp.size*dis.dt*dis.nt)
                print(
                    '    {:15}: {:>12.4f}'
                    .format(cp.name_solid+' CF', capfac[0])
                )
                self.capfac[cp] = capfac

    def cashflow_plot(
        self, cost_elec='lcoe', cost_sub=0, tax_rate=0,
        salv_rate=0, depr=False, fig_size=(12, 5)
    ):
        """Displays the cashflow diagram.

        Parameters
        ----------
        cost_elec : float or str
            Electricity rate [$/kWh] for IRR calculations. Set to 'lcoe' to
            set electricity rate to LCOE (IRR = discount rate).
        cost_sub : float
            Subsidized electricity cost [$/kWh].
        tax_rate : float
            Tax on income.
        salv_rate : float
            Salvage value as percentage of capital cost.
        depr : bool
            If True, then depreciation will be calculated.
        fig_size : tuple
            Size of plot. (default: (12, 5))

        """

        def col_light(col_base, bright):
            """Lightens a base color."""

            # get RGB components
            val_r = int(col_base[1:3], 16)
            val_g = int(col_base[3:5], 16)
            val_b = int(col_base[5:7], 16)

            # adjust RGB components
            adj_r = int(val_r+bright*(255-val_r))
            adj_g = int(val_g+bright*(255-val_g))
            adj_b = int(val_b+bright*(255-val_b))

            # convert to output color
            col_adj = '#{}{}{}'.format(
                hex(adj_r)[2:],
                hex(adj_g)[2:],
                hex(adj_b)[2:]
            )

            return col_adj

        # run econ_calc if not yet run
        if not self.is_econ:
            self.econ_calc(
                cost_elec, cost_sub, tax_rate,
                salv_rate, depr, False
            )

        # initialize plot
        plt.figure(figsize=fig_size)
        col_c = Patch(color='#000000', label='Cap/Rep')
        col_o = Patch(color=col_light('#000000', 0.3), label='OpEx')
        col_f = Patch(color=col_light('#000000', 0.6), label='FuelEx')
        cost_leg = plt.legend(handles=[col_c, col_o, col_f], loc=1)
        ax = plt.gca().add_artist(cost_leg)

        # initialize variables
        cumcost = 0
        cumrev = 0
        t = np.arange(0, self.yr_proj+1)

        # iterate per component
        for cp, sub in zip(self.cf_dict, self.cf_dict.values()):

            # plot depending on type
            if cp == 'Revenue':

                # plot revenue
                plt.bar(
                    t, sub, bottom=cumrev, color='#33CC33', label='Revenue'
                )
                cumrev += sub

            elif cp == 'Depreciation':

                plt.bar(
                    t, sub, bottom=cumrev, color='#990099',
                    label='Depreciation'
                )
                cumrev += sub

            elif cp == 'Salvage':

                plt.bar(
                    t, sub, bottom=cumrev, color='#FF6600',
                    label='Salvage'
                )
                cumrev += sub

            elif cp == 'Project':

                # plot capex
                plt.bar(
                    t, -sub['CapEx'], bottom=-cumcost,
                    color='#990000', label='Project'
                )
                cumcost += sub['CapEx']

                # plot opex
                plt.bar(
                    t, -sub['OpEx'], bottom=-cumcost,
                    color=col_light('#990000', 0.3)
                )
                cumcost += sub['OpEx']

            else:

                # plot capex
                plt.bar(
                    t, -sub['CapEx'], bottom=-cumcost,
                    color=cp.color_solid, label=cp.name_solid
                )
                cumcost += sub['CapEx']

                # plot repex
                plt.bar(
                    t, -sub['RepEx'], bottom=-cumcost,
                    color=cp.color_solid
                )
                cumcost += sub['RepEx']

                # plot opex
                plt.bar(
                    t, -sub['OpEx'], bottom=-cumcost,
                    color=col_light(cp.color_solid, 0.3)
                )
                cumcost += sub['OpEx']

                # plot fuel
                plt.bar(
                    t, -sub['FuelEx'], bottom=-cumcost,
                    color=col_light(cp.color_solid, 0.6)
                )
                cumcost += sub['FuelEx']

        # plot
        plt.xticks(np.arange(0, self.yr_proj+1))
        plt.plot([-1, self.yr_proj+1], [0, 0], color='#000000')
        plt.xlabel('Year')
        plt.ylabel('Cost [$]')
        plt.legend(loc=4)
        plt.show()

    def cashflow_csv(
        self, file, cost_elec='lcoe', cost_sub=0, tax_rate=0,
        salv_rate=0, depr=False
    ):
        """Creates a csv with the powerflow

        Parameters
        ----------
        file : str
            Filename for output file.
        cost_elec : float or str
            Electricity rate [$/kWh] for IRR calculations. Set to 'lcoe' to
            set electricity rate to LCOE (IRR = discount rate).
        cost_sub : float
            Subsidized electricity cost [$/kWh].
        tax_rate : float
            Tax on income.
        salv_rate : float
            Salvage value as percentage of capital cost.
        depr : bool
            If True, then depreciation will be calculated.

        """
        # run econ_calc if not yet run
        if not self.is_econ:
            self.econ_calc(
                cost_elec, cost_sub, tax_rate,
                salv_rate, depr, False
            )

        # initialize
        cost_arr = np.zeros((int(self.yr_proj)+1, 1))
        cost_arr[:, 0] = np.arange(0, self.yr_proj+1)
        header = ['Year']

        # iterate per component
        for cp, sub in zip(self.cf_dict, self.cf_dict.values()):

            if cp == 'Revenue':

                # append to header
                header += ['Revenue']

                # append to cost array
                cost_arr = np.append(cost_arr, np.atleast_2d(sub).T, axis=1)

            elif cp == 'Depreciation':

                # append to header
                header += ['Depreciation']

                # append to cost array
                cost_arr = np.append(cost_arr, np.atleast_2d(sub).T, axis=1)

            elif cp == 'Salvage':

                # append to header
                header += ['Salvage']

                # append to cost array
                cost_arr = np.append(cost_arr, np.atleast_2d(sub).T, axis=1)

            elif cp == 'Project':

                # append to header
                header += ['Project CapEx', 'Project OpEx']

                # append to cost array
                for cf in [sub['CapEx'], sub['OpEx']]:
                    cost_arr = np.append(cost_arr, np.atleast_2d(cf).T, axis=1)

            else:

                # append to header
                header += [
                    cp.name_solid+' CapEx', cp.name_solid+' OpEx',
                    cp.name_solid+' RepEx', cp.name_solid+' FuelEx'
                ]

                # append to cost array
                for cf in [
                    sub['CapEx'], sub['OpEx'], sub['RepEx'], sub['FuelEx']
                ]:
                    cost_arr = np.append(cost_arr, np.atleast_2d(cf).T, axis=1)

        # make csv file
        pd.DataFrame(cost_arr).to_csv(file, header=header, index=None)

    @staticmethod
    def _npc(dis, yr_proj, disc, proj_capex, proj_caprt, proj_opex):
        """Calculates the net present value (NPC).

        Parameters
        ----------
        dis : Dispatch
            A Dispatch object from which to calculate the LCOE.
        yr_proj : float
            Project lifetime [yr].
        disc : float
            Discount rate.
        proj_capex : float
            Capital expenses [USD] of the project.
        proj_caprt : float
            Project capital expenses as a fraction of the component CapEx.
        proj_opex : float
            Fixed yearly operating expenses [USD/yr] of the project.

        Returns
        -------
        npc : ndarray
            The NPC of each scenario. Returns nan if scenario is invalid.

        """
        # start cost calculation in each module
        dis.ld._cost_calc(yr_proj, disc)
        dis.im._cost_calc(yr_proj, disc)
        dis.st._cost_calc(yr_proj, disc)
        dis.dp._cost_calc(yr_proj, disc)
        dis.sk._cost_calc(yr_proj, disc)
        dis.gd._cost_calc(yr_proj, disc)
        dis.su._cost_calc(yr_proj, disc)

        # get total capex
        proj_capex_tot = proj_capex+proj_caprt*np.sum(
            dis.ld.cost_c+dis.im.cost_c+dis.st.cost_c +
            dis.dp.cost_c+dis.sk.cost_c+dis.gd.cost_c +
            dis.su.cost_c
        )

        # get total opex
        proj_opex_tot = proj_opex*np.sum(
            1/(1+disc)**np.arange(1, 1+yr_proj)
        )

        # calculate total cost
        npc = proj_capex_tot+proj_opex_tot+np.sum(
            dis.ld.cost+dis.im.cost+dis.st.cost +
            dis.dp.cost+dis.sk.cost+dis.gd.cost +
            dis.su.cost, axis=0
        )

        return npc

    @staticmethod
    def _lcoe(dis, yr_proj, disc, proj_capex, proj_caprt, proj_opex):
        """Calculates the LCOE.

        Parameters
        ----------
        dis : Dispatch
            A Dispatch object from which to calculate the LCOE.
        yr_proj : float
            Project lifetime [yr].
        disc : float
            Discount rate.
        proj_capex : float
            Capital expenses [USD] of the project.
        proj_caprt : float
            Project capital expenses as a fraction of the component CapEx.
        proj_opex : float
            Fixed yearly operating expenses [USD/yr] of the project.

        Returns
        -------
        lcoe : ndarray
            The LCOE of each scenario. Returns nan if scenario is invalid.

        """
        # start cost calculation in each module
        dis.ld._cost_calc(yr_proj, disc)
        dis.im._cost_calc(yr_proj, disc)
        dis.st._cost_calc(yr_proj, disc)
        dis.dp._cost_calc(yr_proj, disc)
        dis.sk._cost_calc(yr_proj, disc)
        dis.gd._cost_calc(yr_proj, disc)
        dis.su._cost_calc(yr_proj, disc)

        # get cost of electrical components only
        cost = 0
        for cp in dis.comp_list:
            if cp.is_elec:
                cost += cp.cost
        cost = np.sum(cost, axis=0)

        # add total capex
        cost += proj_capex+proj_caprt*np.sum(
            dis.ld.cost_c+dis.im.cost_c+dis.st.cost_c +
            dis.dp.cost_c+dis.sk.cost_c+dis.gd.cost_c +
            dis.su.cost_c
        )

        # add total opex
        cost += proj_opex*np.sum(
            1/(1+disc)**np.arange(1, 1+yr_proj)
        )

        # get total electrical load
        ld_elec = 0
        for cp in dis.comp_list:
            if isinstance(cp, LoadComponent) and cp.is_elec:
                ld_elec += cp.enr_tot

        # calculate LCOE
        yr_sc = 8760/(dis.nt*dis.dt)
        crf = disc*(1+disc)**yr_proj/((1+disc)**yr_proj-1)
        lcoe = crf*cost/(ld_elec*yr_sc)

        return lcoe

    @staticmethod
    def _lcow(dis, yr_proj, disc, proj_capex, proj_caprt, proj_opex):
        """Calculates the LCOW.

        Parameters
        ----------
        dis : Dispatch
            A Dispatch object from which to calculate the LCOE.
        yr_proj : float
            Project lifetime [yr].
        disc : float
            Discount rate.
        proj_capex : float
            Capital expenses [USD] of the project.
        proj_caprt : float
            Project capital expenses as a fraction of the component CapEx.
        proj_opex : float
            Fixed yearly operating expenses [USD/yr] of the project.

        Returns
        -------
        lcoe : ndarray
            The LCOE of each scenario. Returns nan if scenario is invalid.

        """
        # start cost calculation in each module
        dis.ld._cost_calc(yr_proj, disc)
        dis.im._cost_calc(yr_proj, disc)
        dis.st._cost_calc(yr_proj, disc)
        dis.dp._cost_calc(yr_proj, disc)
        dis.sk._cost_calc(yr_proj, disc)
        dis.gd._cost_calc(yr_proj, disc)
        dis.su._cost_calc(yr_proj, disc)

        # get statistics from water components
        enr_ld = 0  # energy from water load
        enr_sk = 0  # energy into water sink
        wat_cost = 0  # cost of water components
        vol_tot = 0  # water generated
        for cp in dis.comp_list:
            if cp.is_water:
                wat_cost += np.sum(cp.cost, axis=0)
                if isinstance(cp, LoadComponent):
                    enr_ld += cp.enr_tot
                    vol_tot += np.sum(cp.water)*dis.dt
                if isinstance(cp, SinkComponent):
                    enr_sk += cp.enr_tot
        enr_gen = enr_ld-enr_sk

        # get CRF and LCOE
        yr_sc = 8760/(dis.nt*dis.dt)
        crf = disc*(1+disc)**yr_proj/((1+disc)**yr_proj-1)
        lcoe = Control._lcoe(
            dis, yr_proj, disc, proj_capex, proj_caprt, proj_opex
        )

        # get LCOW
        lcow = (lcoe*enr_gen*yr_sc+crf*wat_cost)/(vol_tot*yr_sc)

        return lcow
