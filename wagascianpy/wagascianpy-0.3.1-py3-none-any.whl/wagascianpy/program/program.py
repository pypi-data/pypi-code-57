#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import os
import re

from six import string_types

try:
    from multiprocessing import cpu_count
except ImportError as err:
    if "multiprocessing" in repr(err):
        from os import cpu_count
    else:
        raise

import wagascianpy.analysis.analysis
import wagascianpy.analysis.analyzer
from wagascianpy.analysis.analyzer import AnalyzerThreadingType, AnalyzerInputType
import wagascianpy.utils.environment
import wagascianpy.utils.utils

MAX_THREADS = 8


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
        self._multiple_run_analyzer_save_location = None
        self._analyzer_factories = []

        # Enable thread safety
        env = wagascianpy.utils.environment.WagasciEnvironment()
        wagasci_lib = env['WAGASCI_LIBDIR']
        wagascilib_call = wagascianpy.analysis.analysis.WagasciAnalysis(wagasci_lib)
        wagascilib_call.enable_thread_safety()
        nproc = cpu_count()
        if not nproc:
            MAX_THREADS = 1
        elif 1 <= nproc <= MAX_THREADS:
            MAX_THREADS = nproc

    def start(self):
        # setup first analyzer flags
        is_first_analyzer = {}
        for run_name in self._run_dict.keys():
            is_first_analyzer[run_name] = True
        # setup WagasciAnalysis thread chains
        chains_for_each_run = {}
        for run_name in self._run_dict.keys():
            chains_for_each_run[run_name] = {}
        # loop over the analyzers
        for analyzer_factory in self._analyzer_factories:
            if analyzer_factory.input_type == AnalyzerInputType.single_run:
                # loop over the single runs
                for run_name, run_root_dir in sorted(self._run_dict.items()):
                    try:
                        # setup the input directory and output directory for each analyzer
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
                        # get the run number from the run name
                        match = re.search(r'.*_([\d]+)$', run_name)
                        run_number = None if match is None else int(match.group(1))
                        # if single threaded wait for all the previous threads to complete
                        if analyzer_factory.threading_type == AnalyzerThreadingType.single_threaded and \
                                len(chains_for_each_run[run_name]) > 1:
                            wagascianpy.utils.utils.join_single_chain(chains_for_each_run[run_name])
                            chains_for_each_run[run_name] = {}
                        if analyzer_factory.threading_type == AnalyzerThreadingType.multi_threaded and \
                                len(chains_for_each_run[run_name]) == 1:
                            wagascianpy.utils.utils.join_single_chain(chains_for_each_run[run_name])
                            chains_for_each_run[run_name] = {}
                        # Get the analyzer from the factory
                        run_analyzer = analyzer_factory.get_analyzer(run_root_dir=run_root_dir, run_name=run_name,
                                                                     run_number=run_number, output_dir=output_dir)
                        # Spawn run analyzer
                        print("Applying %s analyzer on %s" % (run_analyzer.name, run_name))
                        run_analyzer.spawn(chains_for_each_run[run_name])
                        # Limit number of threads
                        wagascianpy.utils.utils.limit_chains(chains_for_each_run, MAX_THREADS)
                    except Exception as exception:
                        if self._stop_on_exception:
                            raise exception
                        else:
                            print("Run {} failed with exception : {}".format(run_name, str(exception)))
            elif analyzer_factory.input_type == AnalyzerInputType.multiple_runs:
                chain = {}
                # set the name for the multirun analyzer
                name = analyzer_factory.name
                run_numbers = []
                for run_name in self._run_dict:
                    match = re.search(r'.*_([\d]+)$', run_name)
                    run_number = None if match is None else int(match.group(1))
                    run_numbers.append(run_number)
                min_run_number = min(run_numbers)
                max_run_number = max(run_numbers)
                if min_run_number is not None and max_run_number is not None:
                    name = "{}_from_{}_to_{}".format(name, min_run_number, max_run_number)
                try:
                    # set input and output directories
                    if all(is_first_analyzer.values()) or not self._save_dict:
                        run_root_dir = sorted(list(self._run_dict.values()))
                    else:
                        run_root_dir = sorted(list(self._save_dict.values()))
                    if self._multiple_run_analyzer_save_location is None:
                        raise ValueError("To use a multiple run analyzer you must set its save location first")
                    output_dir = self._multiple_run_analyzer_save_location
                    # Get analyzer from factory
                    analyzer = analyzer_factory.get_analyzer(run_root_dir=run_root_dir,
                                                             run_name=name,
                                                             run_number=None,
                                                             output_dir=output_dir)
                    print("Applying %s analyzer on runs from %s to %s"
                          % (analyzer.name, min_run_number, max_run_number))
                    # Spawn all the threads and join them rightaway
                    analyzer.spawn(chain)
                    wagascianpy.utils.utils.join_single_chain(chain)
                except Exception as exception:
                    if self._stop_on_exception:
                        raise exception
                    else:
                        print("{} failed with exception : {}".format(name, str(exception)))
            else:
                raise NotImplementedError("Analyzer type not recognized %s" % analyzer_factory.input_type)

    @property
    def multiple_runs_analyzer_save_location(self):
        return self._multiple_run_analyzer_save_location

    @multiple_runs_analyzer_save_location.setter
    def multiple_runs_analyzer_save_location(self, location):
        if not isinstance(location, string_types):
            raise TypeError("multiple run analyzersave location must be a string path")
        if not os.path.exists(location):
            wagascianpy.utils.utils.mkdir_p(location)
        self._multiple_run_analyzer_save_location = location

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
        if factory.depends and factory.depends not in [f.name for f in self._analyzer_factories]:
            raise RuntimeError("{} depends on {} but not found".format(factory.name, factory.depends))
        return factory

    def add_step(self, name, **kwargs):
        analyzer_factory_producer = wagascianpy.analysis.analyzer.AnalyzerFactoryProducer()
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
