# -*- coding: utf-8 -*-
"""Microapp group module"""

from __future__ import print_function

import sys, abc

from multiprocessing import cpu_count, Pool
from microapp.base import MicroappObject, microapp_builtins
from microapp.error import TestError, UsageError, InternalError
from microapp.parse import GroupArgParser, ArgType
from microapp.framework import load_appclass
from microapp.utils import reduce_arg, assert_check, appdict, Logger, Logger
from microapp.parallel import EdgeMultiprocChildProxy as EdgeProxy

PY3 = sys.version_info >= (3, 0)


class Edge(object):

    _num_edge_instances = 0

    def __new__(cls, *vargs, **kwargs):

        obj = super(Edge, cls).__new__(cls)

        obj._eid = cls._num_edge_instances # edge id
        obj._bid = None # branch  id
        obj._tasks = []

        cls._num_edge_instances += 1

        return obj

    def append_task(self, task):
        self._tasks.append(task)

    def clone(self):
        edge = self.__class__()
        edge._tasks.extend(self._tasks)

        return edge


class Node(object):
    pass


class DynamicNode(Node):

    @abc.abstractmethod
    def transform(self):
        pass


class AppEdge(Edge):

    def append_app(self, app, args, subargs=None):

        self.append_task((app, args, subargs))

    def run(self, mgr, fwds=None):

        if not fwds:
            fwds = appdict()

        for appname, args, subargs in self._tasks:

            builtin_apps = mgr.get_builtin_apps()
            appcls, targs, sargs, objs = load_appclass(appname, args,
                    subargs, builtin_apps)
            app = appcls(mgr)

            # TODO: support ScriptGroup
            #if hasattr(app, "_dcasts"):
            #    app._dcasts.update(mgr.iter_downcast())

            fwds.update(objs)
            fwds["_bid_"] = self._bid

            ret, fwds = app.run(targs, sargs, fwds)

            if ret != 0:
                raise TestError("'%s' app returned %d." % (appname, ret))

        return 0, fwds


class DepartureNode(Node):

    def __new__(cls, *vargs, **kwargs):

        obj = super(DepartureNode, cls).__new__(cls)
        obj._nodefwd = appdict()
        obj._num_edges = 0
        obj._edges = []

        return obj

    def update_forward(self, edge, fwd):

        if edge in self._nodefwd:
            self._nodefwd[edge].update(fwd)

        else:
            self._nodefwd[edge] = appdict(fwd)

    def edge_forward(self, edge):
        return appdict(self._nodefwd[edge])

    def add_edge(self, edge, arrivalnode):

        edge._bid = self._num_edges
        self._num_edges += 1

        self._edges.append((edge, arrivalnode))

    def get_departure_paths(self):
        return list(self._edges)


class ArrivalNode(Node):

    def is_quorum(self, total_arrivals, present_arrivals):

        return set(total_arrivals) == set(a[0] for a in present_arrivals)

    def node_forward(self, arrived):

        fwds = appdict()

        for edge, ret, afwd in arrived:
            if ret == 0:
                for k, v in afwd.items():
                    if k in fwds:
                        if isinstance(fwds[k], list):
                            fwds[k].append(v)
                        else:
                            fwds[k] = [fwds[k], v]
                    else:
                        fwds[k] = v
            else:
                raise UsageError("Path '%s' finished with non-zero return "
                                "code at '%s' with forward of '%s'." % (
                                str(edge), str(self), str(afwd)))
        return fwds


class EntryNode(DepartureNode):
    pass


class ExitNode(ArrivalNode):
    pass


class Hub(DepartureNode, ArrivalNode):
    pass


class Group(MicroappObject, GroupArgParser, EntryNode, ExitNode):

    def __new__(cls, mgr, *vargs, **kwargs):

        kwargs["add_help"] = False

        obj = super(Group, cls).__new__(cls, *vargs, **kwargs)
        obj.manager = mgr

        #obj._departures = appdict()

        obj._entrynodes = appdict()
        obj._exitnodes = appdict()
        obj._arrivalnodes = appdict()

        obj._edgeproxy_ready = []
        obj._edgeproxy_active = []
        obj._procpool = None
        
#        # add common arguments
#        # syntax --map 'f(x)[ -> y]'
#        obj.add_argument("--map", metavar="expr", delay=True,
#                action="append", help="map data from paths")
#        # syntax --filter 'x > 0[ -> y]'
#        obj.add_argument("--filter", metavar="expr", delay=True,
#                action="append", help="filter data from paths")
#        # syntax --reduce 'sum(x, y)[ -> y]'
#                #type=ArgType(None, True, None), action="append",
        obj.add_argument("--reduce", metavar="expr", delay=True,
                action="append", help="reduce data from paths")
        obj.add_argument("--clone", metavar="expr", type=int,
                help="dupulicate app")
        obj.add_argument("--assigned-input", metavar="data",
                help="assign input data to a specified edge")

        obj.add_argument("--assert-in", metavar="expr", action="append",
                type=bool, help="assertion test on input")
        obj.add_argument("--assert-out", metavar="expr", action="append",
                type=bool, delay=True, help="assertion test on output")
        #obj.add_argument('--version', action='version', version=(cls._name_
        #        + " " + cls._version_))

        #if sys.version_info >= (3, 0):
        obj.add_argument("--multiproc", help="# of processes")

        obj.logger = Logger(mgr, [obj._name_])

        return obj

    def connect_edge(self, departurenode, edge, arrivalnode):

        departurenode.add_edge(edge, arrivalnode)

        if arrivalnode in self._arrivalnodes:
            self._arrivalnodes[arrivalnode].append(edge)

        else:
            self._arrivalnodes[arrivalnode] = [edge]

        if isinstance(departurenode, EntryNode):
            self._entrynodes[departurenode] = None

        if isinstance(arrivalnode, ExitNode):
            self._exitnodes[arrivalnode] = None


    def is_finished(self, terms):

        if any((t not in terms) for t in self._exitnodes.keys()):
            return False

        return True

    @abc.abstractmethod
    def connect(self, args, subargs):
        pass

    def group_forward(self, args, data):

        grp_fwds = appdict()

        for v in data.values():
            grp_fwds.update(v)

        return grp_fwds


    def _init_multiproc(self, nprocs):


        nprocs = cpu_count() if nprocs=="*" else int(nprocs)
        self.logger.debug("nprocs = %d" % nprocs)

        for idx in range(nprocs):
            self._edgeproxy_ready.append(EdgeProxy(self.manager))

        # Pool([processes[, initializer[, initargs[, maxtasksperchild[, context]]]]])
        self._procpool = Pool(nprocs)

    def _multiproc(self, paths):

        async_res = None

        # check if available pipe
        if self._edgeproxy_ready and paths:
            proxy = self._edgeproxy_ready.pop()
            self._edgeproxy_active.append(proxy)

            dep, (edge, arr) = paths.pop()

            child_perform, args, kwargs = proxy.pack_launch(
                                            dep.edge_forward(edge), edge, arr)

            self.logger.debug("edge %d is launched" % edge._eid)

            # async launch process
            # TODO: evaluate using callbacks
            async_res = self._procpool.apply_async(child_perform, args, kwargs)

        return async_res

    def _fini_multiproc(self):

        if self._procpool:
            self._procpool.close()
            self._procpool.join()

    def run(self, args, sargs, fwds):
    
        self.logger.debug("Group '%s' runs: %s" % (self._name_, str(args)))

        # prepare env
        self._env.update(fwds)
        self._env.update(self.manager.iter_shared())
        self._env.update(self.manager.iter_downcast())

        # set program name and parse argument
        pos = sys.argv[0].rfind("-")
        if pos>=0:
            sys.argv[0] = sys.argv[0][:pos]+"-"+self._name_

        else:
            sys.argv[0] += "-"+self._name_

        self._arg_parser.prog = sys.argv[0]

        args, rargs = self.parse_known_args(args, self._env)

        if rargs and rargs[0].startswith("-"):
            raise UsageError("Unknown argument: %s" % " ".join(rargs))

        if args.assert_in:
            for ain in args.assert_in:
                if isinstance(ain, ArgType):
                    ain.env.update(self._env)
                    if not assert_check(ain):
                        raise TestError("Tested '%s' with '%s'" %
                            (str(ain.data), str(ain.env)))
                else:
                    raise InternalError("assert check argument is not ArgType")

        # build graph
        if rargs and sargs:
            sargs = rargs + ["--"] + sargs

        elif rargs:
            sargs = rargs

        elif not sargs:
            sargs = []

        ret = self.connect(args, sargs)

        # collect entry nodes
        #entrynodes = []
        #arrivalnodes = appdict()

        # build ready paths
        ready_paths = []

        if args.assigned_input:
            if args.assigned_input["_context_"]:
                assigned_input = (args.assigned_input["_context_"],
                                  args.assigned_input["_"])
            else:
                assigned_input = ("_", args.assigned_input["_"])

        else:
            assigned_input = tuple()

        for enode in self._entrynodes:
            # TODO: add --data argument
            for path in enode.get_departure_paths():
                edge = path[0]
                enode.update_forward(edge, fwds)

                if assigned_input:
                    if edge._bid < len(assigned_input[1]):
                        ainput = {assigned_input[0]: assigned_input[1][edge._bid]}
                        enode.update_forward(edge, ainput)

                ready_paths.append((enode, path))

        arrived = appdict()
        just_arrived = []
        terminated = appdict()

        if args.multiproc:
            if PY3:
                self._init_multiproc(args.multiproc["_"])

            else:
                pass
                # TODO: show info that py2 does not support multiproc

        while ready_paths or self._edgeproxy_active or just_arrived:

            #self.logger.debug("edgeproxy_active: %s" % str(self._edgeproxy_active))
            #self.logger.debug("just_arrived: %s" % str(just_arrived))

            # launch path if exists
            if ready_paths:
                if PY3 and args.multiproc:
                    self._multiproc(ready_paths)

                else:
                    # pop ready path
                    departure, (edge, arrival) = ready_paths.pop(0)

                    out, fwd = edge.run(self.manager, departure.edge_forward(edge))

                    just_arrived.append(arrival)

                    if arrival in arrived:
                        arrived[arrival].append((edge, out, fwd))

                    else:
                        arrived[arrival] = [(edge, out, fwd)]

            # handle paralle
            if PY3 and args.multiproc:

                processed = False

                # handle message from children
                for proxy in self._edgeproxy_active:
                    finished = proxy.process_child_message()

                    if finished:

                        arrival, edge, out, fwd = finished
                        self.logger.debug("finished edge: %d" % edge._eid)

                        just_arrived.append(arrival)

                        if arrival in arrived:
                            arrived[arrival].append((edge, out, fwd))

                        else:
                            arrived[arrival] = [(edge, out, fwd)]

                        self._edgeproxy_active.remove(proxy)
                        self._edgeproxy_ready.append(proxy)

                    processed = True

                if not processed:
                    for proxy in self._edgeproxy_active:
                        proxy.process_idletask()

            if just_arrived:

                arrival = just_arrived.pop(0)

                # check if quorum
                if arrival.is_quorum(self._arrivalnodes[arrival], arrived[arrival]):

                    # merge paths' output
                    node_fwds = arrival.node_forward(arrived[arrival])

                    # TODO: find good usage of dynamic node
                    if isinstance(arrival, DynamicNode):
                        arrival = arrival.transform()

                    if isinstance(arrival, ExitNode):
                        terminated[arrival] = node_fwds

                        # check if to exit
                        if self.is_finished(terminated):
                            break

                    elif isinstance(arrival, DepartureNode):

                        # add paths
                        for path in arrival.get_departure_paths():
                            arrival.update_forward(path[0], node_fwds)
                            ready_paths.append((arrival, path))

        if PY3 and args.multiproc:
            self._fini_multiproc()

        # merge terminals' output
        grp_fwds = self.group_forward(args, terminated)
        if not grp_fwds:
            grp_fwds = appdict()

        if args.reduce:
            for rdc in args.reduce:
                grp_fwds.update(reduce_arg(rdc, terminated))

#        if args.filter:
#            for flt in args.filter:
#                grp_fwds.update(filter_arg(flt, exit_fwds))
#
#        if args.map:
#            for mp in args.map:
#                grp_fwds.update(map_arg(mp, exit_fwds))

        if args.assert_out:
            for aout in args.assert_out:
                if isinstance(aout, ArgType):
                    aout.env.update(grp_fwds)
                    if not assert_check(aout):
                        raise TestError("Tested '%s' with '%s'" %
                            (str(aout.data), str(aout.env)))
                else:
                    raise InternalError("assert check argument is not ArgType")

        self.logger.debug("Group '%s' finished." % self._name_)

        return 0, grp_fwds


class GroupCmd(Group):

    _name_ = "group"
    _version_ = "0.1.1"

    def __init__(self, mgr):

        self.add_argument("--forwarding", type=str, default="overwrite",
                help="group forward method(pass, block, overwrite:default, accumulate)")

    def connect(self, args, subargs):

        edge = AppEdge()

        items = []
        for s in subargs:
            if s == "--":
                if items and not items[0].startswith("-"):
                    edge.append_app(items[0], items[1:])
                items = []
            else:
                items.append(s)

        if items and not items[0].startswith("-"):
            edge.append_app(items[0], items[1:])

        if args.clone:
            for idx in range(int(args.clone["_"])):
                self.connect_edge(self, edge.clone(), self)
        else:
            self.connect_edge(self, edge, self)

    def group_forward(self, args, data):

        fwdtype = args.forwarding["_"]
        grp_fwds = appdict()

        if fwdtype == "block":
            pass

        elif fwdtype == "pass":
            grp_fwds.update(data)

        elif fwdtype == "overwrite":
            # discard arrival node info
            for v in data.values():
                grp_fwds.update(v)

        elif fwdtype == "accumulate":
            for k, v in data.items():
                if k in grp_fwds:
                    grp_fwds.append(v)

                else:
                    grp_fwds[k] = [v]
        else:
            raise UsageError("Unknown group forward type: %s" % fwdtype)

        return grp_fwds
