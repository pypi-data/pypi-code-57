#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import abc
import inspect
import json
import os
import time
from collections import OrderedDict
from typing import Dict

from recordclass import recordclass

import wagascianpy.analysis
import wagascianpy.beam_summary_data
import wagascianpy.environment
import wagascianpy.utils

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})

ENV = wagascianpy.environment.WagasciEnvironment()
ENV["WAGASCI_LIB"] = ENV['WAGASCI_MAINDIR'] + "/lib"


class Analyzer(ABC):
    depends = None

    def __init__(self, name, run_name, run_root_dir, output_dir, default_args=None,
                 **kwargs):
        self.name = name
        self.run_name = run_name
        self.run_root_dir = run_root_dir
        self.output_dir = output_dir
        if default_args:
            self.args = default_args
        else:
            self.args = OrderedDict()
        self.set_init_arguments(**kwargs)

    @abc.abstractmethod
    def _set_runtime_arguments(self, input_file):
        pass

    @abc.abstractmethod
    def spawn(self, chains):
        pass

    @staticmethod
    def get_topology(acq_config_xml):
        """
        Get the detector topology (DIF - CHIP - CHAN) from the XML configuration file
        :rtype: dict
        :param acq_config_xml: path to XML file containing the acquisition configuration
        :return: Detector topology dictionary
        """
        chain = wagascianpy.analysis.WagasciAnalysis(ENV["WAGASCI_LIB"])
        topology_string = chain.get_dif_topology(acq_config_xml).decode('utf-8')
        return json.loads(topology_string)

    def multiple_file_loop(self, input_files, chains):
        for input_file in sorted(input_files):
            self._set_runtime_arguments(input_file)
            dif_id = int(wagascianpy.utils.extract_dif_id(input_file))
            if not isinstance(chains, Dict):
                raise TypeError("The chains dictionary must be initialized upstream")
            if dif_id not in chains:
                chain = recordclass('Chain', ['link', 'thread'])
                chain.link = wagascianpy.analysis.WagasciAnalysis(ENV["WAGASCI_LIB"])
                chain.thread = chain.link.spawn(self.name, **self.args)
                chains[dif_id] = chain
                time.sleep(1)
            else:
                chains[dif_id].thread = chains[dif_id].link.spawn(self.name, **self.args)
            print("Spawn thread with DIF {} : LINK ID {} : THREAD ID {}".format(dif_id, id(chains[dif_id].link),
                                                                                id(chains[dif_id].thread)))

    def single_file_loop(self, chains):
        if chains and len(chains) > 1:
            raise IndexError("The method %s does not support more than one chain" %
                             inspect.currentframe().f_code.co_name)
        self._set_runtime_arguments(self.run_root_dir)
        dummy_id = 0
        if not isinstance(chains, Dict):
            raise TypeError("The chains dictionary must be initialized upstream")
        if dummy_id not in chains:
            chain = recordclass('Chain', ['link', 'thread'])
            chain.link = wagascianpy.analysis.WagasciAnalysis(ENV["WAGASCI_LIB"])
            chain.thread = chain.link.spawn(self.name, **self.args)
            chains[dummy_id] = chain
        else:
            chains[dummy_id].thread = chains[dummy_id].link.spawn(self.name, **self.args)
        print("Spawn thread with DIF {} : LINK ID {} : THREAD ID {}".format(dummy_id, id(chains[dummy_id].link),
                                                                            id(chains[dummy_id].thread)))

    def set_init_arguments(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.args:
                raise KeyError("Analyzer %s does not accept argument %s" % (self.name, key))
            self.args[key] = value


class Decoder(Analyzer, ABC):
    name = "decoder"
    depends = None

    _default_args = wagascianpy.utils.get_arguments_ordered_dict(wagascianpy.analysis.WagasciAnalysis.decoder)
    _default_args.update({'calibration_dir': "",
                          'overwrite_flag': False,
                          'compatibility_mode': False,
                          'enable_calib_mapping_variables': False})

    def __init__(self, **kwargs):
        super(Decoder, self).__init__(name=self.name, default_args=self._default_args, **kwargs)

        self.acq_config_xml = wagascianpy.utils.acqconfigxml_file_finder(self.run_root_dir, self.run_name)
        if not os.path.exists(self.acq_config_xml):
            raise OSError("Acquisition configuration XML file not found : %s"
                          % self.acq_config_xml)
        self._topology = self.get_topology(self.acq_config_xml)
        wagascianpy.utils.renametree(run_root_dir=self.run_root_dir, run_name=self.run_name,
                                     dif_topology=self._topology)

    def _set_runtime_arguments(self, input_file):
        self.args["input_file"] = input_file
        self.args["output_dir"] = self.output_dir
        dif_id = int(wagascianpy.utils.extract_dif_id(input_file))
        self.args["dif"] = dif_id
        self.args["n_chips"] = len(self._topology[str(dif_id)])

    def spawn(self, chains):
        if os.path.isfile(self.run_root_dir) and self.run_root_dir.endswith('.raw'):
            input_files = [self.run_root_dir]
        else:
            input_files = wagascianpy.utils.find_files_with_ext(self.run_root_dir, 'raw')
        if chains:
            if len(chains) != len(input_files):
                raise ValueError("The number of chains ({}) must be the same as the number of "
                                 "input files ({})".format(len(chains), len(input_files)))
        self.multiple_file_loop(input_files, chains)


class SpillNumberFixer(Analyzer, ABC):
    name = "spill_number_fixer"
    depends = "decoder"

    _default_args = wagascianpy.utils.get_arguments_ordered_dict(
        wagascianpy.analysis.WagasciAnalysis.spill_number_fixer)
    _default_args.update({'flipped_bits': "", 'offset': 0, 'enable_graphics': False})

    def _set_runtime_arguments(self, _):
        pass

    def __init__(self, **kwargs):
        super(SpillNumberFixer, self).__init__(name=self.name, default_args=self._default_args, **kwargs)
        self.args["input_dir"] = self.run_root_dir
        self.args["output_dir"] = self.output_dir

    def spawn(self, chains):
        self.single_file_loop(chains)


class BeamSummaryData(Analyzer, ABC):
    name = "beam_summary_data"
    depends = "spill_number_fixer"

    _default_args = wagascianpy.utils.get_arguments_ordered_dict(wagascianpy.beam_summary_data.beam_summary_data)
    _default_args.update({'t2krun': 10,
                          'recursive': True})

    def __init__(self, **kwargs):
        super(BeamSummaryData, self).__init__(name=self.name, default_args=self._default_args, **kwargs)

    def _set_runtime_arguments(self, input_path):
        self.args["input_path"] = input_path
        if os.path.isdir(input_path):
            self.args["recursive"] = True
        else:
            self.args["recursive"] = False

    def spawn(self, chains):
        self.single_file_loop(chains)


class AnalyzerFactory(ABC):
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    @abc.abstractmethod
    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        self._kwargs.update(kwargs)


class DecoderFactory(AnalyzerFactory):
    depends = Decoder.depends
    name = Decoder.name

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        super(DecoderFactory, self).get_analyzer(run_root_dir, output_dir, **kwargs)
        return Decoder(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class SpillNumberFixerFactory(AnalyzerFactory):
    depends = SpillNumberFixer.depends
    name = SpillNumberFixer.name

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        super(SpillNumberFixerFactory, self).get_analyzer(run_root_dir, output_dir, **kwargs)
        return SpillNumberFixer(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class BeamSummaryDataFactory(AnalyzerFactory):
    depends = BeamSummaryData.depends
    name = BeamSummaryData.name

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        super(BeamSummaryDataFactory, self).get_analyzer(run_root_dir, output_dir, **kwargs)
        return BeamSummaryData(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class AnalyzerFactoryProducer:
    def __init__(self):
        pass

    @staticmethod
    def get_factory(type_of_factory, **kwargs):
        if type_of_factory == "decoder":
            return DecoderFactory(**kwargs)
        if type_of_factory == "spill_number_fixer":
            return SpillNumberFixerFactory(**kwargs)
        if type_of_factory == "beam_summary_data":
            return BeamSummaryDataFactory(**kwargs)
