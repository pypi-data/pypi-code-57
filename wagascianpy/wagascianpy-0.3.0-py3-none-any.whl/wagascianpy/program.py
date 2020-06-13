#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

try:
    from multiprocessing import cpu_count
except ImportError as err:
    if "multiprocessing" in repr(err):
        from os import cpu_count
    else:
        raise

import wagascianpy.analysis
import wagascianpy.analyzer
import wagascianpy.environment
import wagascianpy.utils

MAX_THREADS = 8

ENV = wagascianpy.environment.WagasciEnvironment()
ENV["WAGASCI_LIB"] = ENV['WAGASCI_MAINDIR'] + "/lib"


class Program(object):
    """
    Class to decode a list of runs as an uninterrupted job. The usage scenario is when
    you need to decode multiple runs in one batch and do not want to monitor the chain
    continuously. The decoding should go on even in case of error and print a report at the
    end.
    """

    def __init__(self):
        global MAX_THREADS
        self._stop_on_exception = True
        self._enforce_dependencies = True
        self._run_dict = {}
        self._output_dir_same_as_input = True
        self._save_dict = {}
        self._analyzer_factories = []

        # Enable thread safety
        wagascilib_call = wagascianpy.analysis.WagasciAnalysis(ENV["WAGASCI_LIB"])
        wagascilib_call.enable_thread_safety()
        nproc = cpu_count()
        if not nproc:
            MAX_THREADS = 1
        elif 1 <= nproc <= MAX_THREADS:
            MAX_THREADS = nproc

    def start(self):
        is_first_analyzer = {}
        for run_name in self._run_dict.keys():
            is_first_analyzer[run_name] = True
        for analyzer_factory in self._analyzer_factories:
            chains_for_each_run = {}
            for run_name, run_root_dir in sorted(self._run_dict.items()):
                try:
                    if is_first_analyzer[run_name]:
                        if self._output_dir_same_as_input:
                            output_dir = run_root_dir
                        else:
                            output_dir = self._save_dict[run_name]
                    else:
                        if self._output_dir_same_as_input:
                            output_dir = run_root_dir
                        else:
                            output_dir = self._save_dict[run_name]
                            run_root_dir = self._save_dict[run_name]
                    is_first_analyzer[run_name] = False

                    run_analyzer = analyzer_factory.get_analyzer(run_root_dir=run_root_dir, run_name=run_name,
                                                                 output_dir=output_dir)
                    print("Applying %s analyzer on %s" % (run_analyzer.name, run_name))

                    chains_for_each_run[run_name] = {}
                    run_analyzer.spawn(chains_for_each_run[run_name])
                    wagascianpy.utils.limit_chains(chains_for_each_run, MAX_THREADS)
                except Exception as exception:
                    if self._stop_on_exception:
                        raise exception
                    else:
                        print("Run {} failed with exception : {}".format(run_name, str(exception)))

            wagascianpy.utils.join_chains(chains_for_each_run)

    def set_run_location(self, run_dict):
        self._run_dict = run_dict

    def get_run_location(self):
        return self._run_dict

    def get_save_location(self):
        return self._save_dict

    def set_save_location(self, save_dict):
        """
        Set a custom location where to store each run decoded data.
        :param save_dict: Dictionary where the key is the run name and the value is
                          the path of the folder where the decoded data is to be stored
        :rtype: None
        """
        self._save_dict = save_dict
        for run_name in self._run_dict:
            if run_name not in save_dict:
                raise KeyError("The save location dictionary does not contain the run named '%s'" % run_name)
        self._output_dir_same_as_input = False

    def output_dir_same_as_input(self):
        self._save_dict.clear()
        self._output_dir_same_as_input = True

    def _check_dependencies(self, factory):
        if (factory.depends is not None and
                factory.depends not in [factory.name for factory in self._analyzer_factories]):
            raise RuntimeError("{} depends on {} but not found".format(factory.name, factory.depends))
        return factory

    def add_step(self, name, **kwargs):
        analyzer_factory_producer = wagascianpy.analyzer.AnalyzerFactoryProducer()
        factory = analyzer_factory_producer.get_factory(name, **kwargs)
        if self._enforce_dependencies:
            analyzer_factory = self._check_dependencies(factory)
        else:
            analyzer_factory = factory
        self._analyzer_factories.append(analyzer_factory)

    def do_not_stop_on_exception(self):
        self._stop_on_exception = False
        
    def stop_on_exception(self):
        self._stop_on_exception = True
        
    def enforce_dependencies(self):
        self._enforce_dependencies = True
        
    def do_not_enforce_dependencies(self):
        self._enforce_dependencies = False
