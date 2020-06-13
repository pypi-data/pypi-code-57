#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import abc
import inspect
import json
import os
import shutil
import time
from collections import OrderedDict

from recordclass import recordclass
from enum import Enum

import wagascianpy.analysis.analysis
import wagascianpy.analysis.beam_summary_data
import wagascianpy.utils.environment
import wagascianpy.utils.utils

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class AnalyzerInputType(Enum):
    single_run = 1,
    multiple_runs = 2


class AnalyzerThreadingType(Enum):
    multi_threaded = 1,
    single_threaded = 2
    

class Analyzer(ABC):
    depends = None

    def __init__(self, analyzer_name, run_name, run_root_dir, output_dir,
                 run_number=None, default_args=None, **kwargs):
        self.name = analyzer_name
        self.run_name = run_name
        self.run_number = run_number
        self.run_root_dir = run_root_dir
        self.output_dir = output_dir
        self.wagasci_lib_ = None
        try:
            env = wagascianpy.utils.environment.WagasciEnvironment()
            self.wagasci_lib_ = env['WAGASCI_LIBDIR']
        except KeyError:
            raise KeyError("WAGASCI_LIBDIR variable not found in the shell environment")
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

    def get_topology(self, acq_config_xml):
        """
        Get the detector topology (DIF - CHIP - CHAN) from the XML configuration file
        :rtype: dict
        :param acq_config_xml: path to XML file containing the acquisition configuration
        :return: Detector topology dictionary
        """
        chain = wagascianpy.analysis.analysis.WagasciAnalysis(self.wagasci_lib_)
        topology_string, pointer = chain.get_dif_topology(acq_config_xml)
        chain.free_topology(pointer)
        return json.loads(topology_string.decode('utf-8'))

    def multiple_input_loop(self, input_files, chains):
        if chains:
            if len(chains) != len(input_files):
                raise ValueError("The number of chains ({}) must be the same as the number of "
                                 "input files ({})".format(len(chains), len(input_files)))
        for input_file in sorted(input_files):
            self._set_runtime_arguments(input_file)
            dif_id = int(wagascianpy.utils.utils.extract_dif_id(input_file))
            if not isinstance(chains, dict):
                raise TypeError("The chains dictionary must be initialized upstream")
            if dif_id not in chains:
                chain = recordclass('Chain', ['link', 'thread'])
                chain.link = wagascianpy.analysis.analysis.WagasciAnalysis(self.wagasci_lib_)
                chain.thread = chain.link.spawn(self.name, **self.args)
                chains[dif_id] = chain
                time.sleep(1)
            else:
                chains[dif_id].thread = chains[dif_id].link.spawn(self.name, **self.args)
            print("Spawn thread with DIF {} : LINK ID {} : THREAD ID {}".format(dif_id, id(chains[dif_id].link),
                                                                                id(chains[dif_id].thread)))

    def single_input_loop(self, chains):
        if chains and len(chains) > 1:
            raise IndexError("The method %s does not support more than one chain" %
                             inspect.currentframe().f_code.co_name)
        self._set_runtime_arguments(self.run_root_dir)
        dummy_id = 0
        if not isinstance(chains, dict):
            raise TypeError("The chains dictionary must be initialized upstream")
        if dummy_id not in chains:
            chain = recordclass('Chain', ['link', 'thread'])
            chain.link = wagascianpy.analysis.analysis.WagasciAnalysis(self.wagasci_lib_)
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


class Decoder(Analyzer):
    name = "decoder"
    depends = None
    input_type = AnalyzerInputType.single_run
    threading_type = AnalyzerThreadingType.multi_threaded

    _default_args = wagascianpy.utils.utils.get_arguments_ordered_dict(
        wagascianpy.analysis.analysis.WagasciAnalysis.decoder)
    _default_args.update({'calibration_dir': "",
                          'overwrite_flag': False,
                          'compatibility_mode': False,
                          'enable_tdc_variables': False})

    def __init__(self, **kwargs):
        super(Decoder, self).__init__(analyzer_name=self.name, default_args=self._default_args, **kwargs)

        self.acq_config_xml = wagascianpy.utils.utils.acqconfigxml_file_finder(self.run_root_dir, self.run_name)
        if not os.path.exists(self.acq_config_xml):
            raise OSError("Acquisition configuration XML file not found : %s"
                          % self.acq_config_xml)
        self._topology = self.get_topology(self.acq_config_xml)
        wagascianpy.utils.utils.renametree(run_root_dir=self.run_root_dir, run_name=self.run_name,
                                           dif_topology=self._topology)

    def _set_runtime_arguments(self, input_file):
        self.args["input_file"] = input_file
        self.args["output_dir"] = self.output_dir
        dif_id = int(wagascianpy.utils.utils.extract_dif_id(input_file))
        self.args["dif"] = dif_id
        self.args["n_chips"] = len(self._topology[str(dif_id)])

    def spawn(self, chains):
        if os.path.isfile(self.run_root_dir) and self.run_root_dir.endswith('.raw'):
            input_files = [self.run_root_dir]
        else:
            input_files = wagascianpy.utils.utils.find_files_with_ext(self.run_root_dir, 'raw')
        if not os.path.exists(self.output_dir):
            wagascianpy.utils.utils.mkdir_p(self.output_dir)
        for xml_file in wagascianpy.utils.utils.find_files_with_ext(self.run_root_dir, 'xml'):
            try:
                shutil.copy2(src=xml_file, dst=os.path.join(self.output_dir, os.path.basename(xml_file)))
            except shutil.SameFileError:
                pass
        for log_file in wagascianpy.utils.utils.find_files_with_ext(self.run_root_dir, 'log'):
            try:
                shutil.copy2(src=log_file, dst=os.path.join(self.output_dir, os.path.basename(log_file)))
            except shutil.SameFileError:
                pass
        self.multiple_input_loop(input_files, chains)


class SpillNumberFixer(Analyzer):
    name = "spill_number_fixer"
    depends = "decoder"
    input_type = AnalyzerInputType.single_run
    threading_type = AnalyzerThreadingType.single_threaded

    _zed_board_bug_runs = range(58, 79)

    _default_args = wagascianpy.utils.utils.get_arguments_ordered_dict(
        wagascianpy.analysis.analysis.WagasciAnalysis.spill_number_fixer)
    _default_args.update({'output_filename': "", 'passes': "", 'offset': 0,
                          'enable_graphics': False})

    def _set_runtime_arguments(self, _):
        self.args["output_filename"] = self.run_name
        if self.run_number in self._zed_board_bug_runs:
            self.args["passes"] = "FirsPassOnSteroids,SecondPassOnSteroids,FirstPassRegular," \
                                  "SecondPassRegular,ThirdPassRegular,FourthPassRegular"

    def __init__(self, **kwargs):
        super(SpillNumberFixer, self).__init__(analyzer_name=self.name, default_args=self._default_args, **kwargs)
        self.args["input_dir"] = self.run_root_dir
        self.args["output_dir"] = self.output_dir

    def spawn(self, chains):
        if not os.path.exists(self.output_dir):
            wagascianpy.utils.utils.mkdir_p(self.output_dir)
        self.single_input_loop(chains)


class BeamSummaryData(Analyzer):
    name = "beam_summary_data"
    depends = "spill_number_fixer"
    input_type = AnalyzerInputType.single_run
    threading_type = AnalyzerThreadingType.single_threaded

    _default_args = wagascianpy.utils.utils.get_arguments_ordered_dict(
        wagascianpy.analysis.beam_summary_data.beam_summary_data)
    _default_args.update({'t2krun': 10,
                          'recursive': True})

    def __init__(self, **kwargs):
        super(BeamSummaryData, self).__init__(analyzer_name=self.name, default_args=self._default_args, **kwargs)

    def _set_runtime_arguments(self, input_path):
        self.args["input_path"] = input_path
        if os.path.isdir(input_path):
            self.args["recursive"] = True
        else:
            self.args["recursive"] = False

    def spawn(self, chains):
        self.single_input_loop(chains)


class Temperature(Analyzer):
    name = "temperature"
    depends = "beam_summary_data"
    input_type = AnalyzerInputType.single_run
    threading_type = AnalyzerThreadingType.multi_threaded

    _default_args = wagascianpy.utils.utils.get_arguments_ordered_dict(
        wagascianpy.analysis.analysis.WagasciAnalysis.temperature)
    _default_args.update({'sqlite_database': "/hsm/nu/wagasci/data/temphum/mh_temperature_sensors_t2krun10.sqlite3"})

    def __init__(self, **kwargs):
        super(Temperature, self).__init__(analyzer_name=self.name, default_args=self._default_args, **kwargs)

    def _set_runtime_arguments(self, input_file):
        self.args["input_file"] = input_file

    def spawn(self, chains):
        if os.path.isfile(self.run_root_dir) and self.run_root_dir.endswith('.root'):
            input_files = [self.run_root_dir]
        else:
            input_files = [filename for filename
                           in wagascianpy.utils.utils.find_files_with_ext(self.run_root_dir, 'root')
                           if wagascianpy.utils.utils.extract_dif_id(filename) is not None]
        self.multiple_input_loop(input_files, chains)


class DataQuality(Analyzer):
    name = "data_quality"
    depends = "temperature"
    input_type = AnalyzerInputType.multiple_runs
    threading_type = AnalyzerThreadingType.multi_threaded

    _default_args = wagascianpy.utils.utils.get_arguments_ordered_dict(
        wagascianpy.analysis.analysis.WagasciAnalysis.data_quality)
    _default_args.update({'passes': 3, 'enable_plotting': False})

    def __init__(self, **kwargs):
        super(DataQuality, self).__init__(analyzer_name=self.name, default_args=self._default_args, **kwargs)
        self.data_quality_filename = self.run_name
        self.args["data_quality_dir"] = self.output_dir
        if self.run_number is not None:
            self.data_quality_filename = "{}_{}".format(self.data_quality_filename, self.run_number)

    def _set_runtime_arguments(self, input_file):
        self.args["tree_files"] = input_file
        dif_id = int(wagascianpy.utils.utils.extract_dif_id(input_file))
        self.args["data_quality_file"] = "{}_ecal_dif_{}.root".format(self.data_quality_filename, dif_id)
        self.args["dif_id"] = dif_id

    def spawn(self, chains):
        if not isinstance(self.run_root_dir, list):
            self.run_root_dir = [self.run_root_dir]
        input_files_dict = {}
        topology_source = self.args["topology_source"]
        if not topology_source:
            topology_source = wagascianpy.utils.utils.acqconfigxml_file_finder(self.run_root_dir[0],
                                                                               os.path.basename(self.run_root_dir[0]))
        self.args["topology_source"] = topology_source
        topology = self.get_topology(topology_source)
        for dif_id in topology:
            input_files_dict[dif_id] = []
            for run_dir in self.run_root_dir:
                for root_file in wagascianpy.utils.utils.find_files_with_ext(run_dir, 'root'):
                    if str(dif_id) == str(wagascianpy.utils.utils.extract_dif_id(root_file)):
                        input_files_dict[dif_id].append(root_file)
        input_files = sorted(input_files_dict.values())
        self.multiple_input_loop(input_files, chains)


class AnalyzerFactory(ABC):

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    @abc.abstractmethod
    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        self._kwargs.update(kwargs)


class DecoderFactory(AnalyzerFactory):
    depends = Decoder.depends
    name = Decoder.name
    input_type = Decoder.input_type
    threading_type = Decoder.threading_type

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        super(DecoderFactory, self).get_analyzer(run_root_dir=run_root_dir, output_dir=output_dir, **kwargs)
        return Decoder(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class SpillNumberFixerFactory(AnalyzerFactory):
    depends = SpillNumberFixer.depends
    name = SpillNumberFixer.name
    input_type = SpillNumberFixer.input_type
    threading_type = SpillNumberFixer.threading_type

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        super(SpillNumberFixerFactory, self).get_analyzer(run_root_dir=run_root_dir, output_dir=output_dir, **kwargs)
        return SpillNumberFixer(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class BeamSummaryDataFactory(AnalyzerFactory):
    depends = BeamSummaryData.depends
    name = BeamSummaryData.name
    input_type = BeamSummaryData.input_type
    threading_type = BeamSummaryData.threading_type

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        super(BeamSummaryDataFactory, self).get_analyzer(run_root_dir=run_root_dir, output_dir=output_dir, **kwargs)
        return BeamSummaryData(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class TemperatureFactory(AnalyzerFactory):
    depends = Temperature.depends
    name = Temperature.name
    input_type = Temperature.input_type
    threading_type = Temperature.threading_type

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        super(TemperatureFactory, self).get_analyzer(run_root_dir=run_root_dir, output_dir=output_dir, **kwargs)
        return Temperature(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


class DataQualityFactory(AnalyzerFactory):
    depends = DataQuality.depends
    name = DataQuality.name
    input_type = DataQuality.input_type
    threading_type = DataQuality.threading_type

    def get_analyzer(self, run_root_dir, output_dir, **kwargs):
        super(DataQualityFactory, self).get_analyzer(run_root_dir=run_root_dir, output_dir=output_dir, **kwargs)
        return DataQuality(run_root_dir=run_root_dir, output_dir=output_dir, **self._kwargs)


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
        if type_of_factory == "temperature":
            return TemperatureFactory(**kwargs)
        if type_of_factory == "data_quality":
            return DataQualityFactory(**kwargs)
        raise NotImplementedError("Factory %s not implemented or not recognized" % type_of_factory)
