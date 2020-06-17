import abc
import inspect
import time
import numpy as np
import h5py
from datetime import datetime
from lasso.dyna.Binout import Binout

from ..utils.constants import StandardFunctionsDefinition, JsonConstants, ObjectConstantsForData, LoggerERROR
from ..calc.standard_functions import StandardFunction
from ..utils.constants import LOGConstants, PluginsParamDictDef
from ..utils.logger import ConsoleLogger
from ..data.dynasaur_definitions import DynasaurDefinitions
from ..data.DataContainer import DataContainer
from ..data.vps import VPSData
from ..data.madymo import MadymoData

class Plugin(object):
    def __init__(self, path_to_def_file, path_def_file_id, data_source, name, user_function_object=None, volume_path=None, code_type="LS-DYNA"):
        '''
        Initialization class constructor

        :param: calculation_procedure_def_file
        :param: object_def_file
        :param: data_source(binout path)
        :param: name
        :param: logger
        :param: dynasaur definition

        :return:
        '''
        self._logger = ConsoleLogger()
        self._dynasaur_definitions = DynasaurDefinitions(self._logger)
        self._dynasaur_definitions.read_def(path_to_def_file)
        self._dynasaur_definitions.read_def(path_def_file_id)
        self._user_function = user_function_object
        #self._code_type = self._dynasaur_definitions.get_code()

        if code_type == "LS-DYNA":
            binout = Binout(data_source)
            DataContainer.init_all_data_sources(binout, self._logger, self._dynasaur_definitions, volume_path=volume_path)
        elif code_type == "VPS":
            vps_data = VPSData(vps_file_path=data_source)
            DataContainer.init_all_data_sources(vps_data, self._logger, self._dynasaur_definitions, volume_path=volume_path)

        elif code_type == "MADYMO":
            madymo_data = MadymoData(madymo_file_path=data_source)
            DataContainer.init_all_data_sources(madymo_data, self._logger, self._dynasaur_definitions, volume_path=volume_path)
        else:
            #TODO: Error msg
            print("Not valid code type")
            return

        self._timestamp = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
        self._units = self._dynasaur_definitions.get_units()
        self._data_requirements = self._dynasaur_definitions.get_required_datatypes(name)
        self._data = None
        self._name = name
        self._sample_types = []

        # ensure unique timestamps
        time.sleep(1)

    def _get_data_from_dynasaur_json(self, json_object, data_offsets):
        '''

        :param json_object:
        :param data_offsets:
        :return:
        '''
        if JsonConstants.FUNCTION in json_object.keys():  # expected name and params
            function_name = json_object[JsonConstants.FUNCTION][JsonConstants.NAME]
            parameter_def = json_object[JsonConstants.FUNCTION][JsonConstants.PARAM]

            param_dict = {}
            for key in parameter_def.keys():
                if type(parameter_def[key]) is dict:  # step into recursion
                    param_dict[key] = self._get_data_from_dynasaur_json(parameter_def[key], data_offsets)
                else:
                    if key == StandardFunctionsDefinition.FUNCTION_NAME:
                        param_dict[key] = {JsonConstants.NAME: parameter_def[key]}
                        continue
                    param_dict[key] = parameter_def[key]

            # START: Standard function
            if function_name == StandardFunctionsDefinition.HIC15:
                return StandardFunction.HIC_15(param_dict, self._units, True)
            elif function_name == StandardFunctionsDefinition.HIC36:
                return StandardFunction.HIC_15(param_dict, self._units, False)
            elif function_name == StandardFunctionsDefinition.BRIC:
                return StandardFunction.bric(param_dict, self._units)
            elif function_name == StandardFunctionsDefinition.A3MS:
                return StandardFunction.a3ms(param_dict, self._units)
            elif function_name == StandardFunctionsDefinition.NIJ:
                return StandardFunction.nij(param_dict, self._units)
            elif function_name == StandardFunctionsDefinition.VC:
                return StandardFunction.vc(param_dict, self._units)
            elif function_name == StandardFunctionsDefinition.TIBIA_INDEX:
                return StandardFunction.tibia_index(param_dict, self._units)
            elif function_name == StandardFunctionsDefinition.CFC:
                return StandardFunction.cfc(param_dict, self._units)
            elif function_name == StandardFunctionsDefinition.RES:
                return StandardFunction.res(param_dict)
            elif function_name == StandardFunctionsDefinition.ABS:
                return StandardFunction.abs(param_dict)
            elif function_name == StandardFunctionsDefinition.TRANSFORM_TO_ORIGIN:
                return StandardFunction.transform_2_origin(param_dict)
            elif function_name == StandardFunctionsDefinition.MAX:
                return StandardFunction.max(param_dict)
            elif function_name == StandardFunctionsDefinition.MAX_IN_ROW:
                return StandardFunction.max_in_row(param_dict)
            elif function_name == StandardFunctionsDefinition.MIN:
                return StandardFunction.minimum(param_dict)
            elif function_name == StandardFunctionsDefinition.MULT:
                return StandardFunction.multiplication(param_dict)
            elif function_name == StandardFunctionsDefinition.SUB:
                return StandardFunction.subtraction(param_dict)
            elif function_name == StandardFunctionsDefinition.ADD:
                return StandardFunction.addition(param_dict)
            elif function_name == StandardFunctionsDefinition.DIVIDE:
                return StandardFunction.divide(param_dict)
            elif function_name == StandardFunctionsDefinition.ABS_SUB:
                return StandardFunction.abs_subtraction(param_dict)
            elif function_name == StandardFunctionsDefinition.ABS_ADD:
                return StandardFunction.abs_addition(param_dict)
            elif function_name == StandardFunctionsDefinition.ABS_SUB_RES:
                return StandardFunction.abs_subtraction_res(param_dict)
            elif function_name == StandardFunctionsDefinition.ABS_MAX:
                return StandardFunction.max(param_dict, absolute=True)
            elif function_name == StandardFunctionsDefinition.NIC:
                return StandardFunction.NIC(param_dict, self._units)
            elif function_name == StandardFunctionsDefinition.uBRIC:
                return StandardFunction.uBRIC(param_dict, self._units)
            elif function_name == StandardFunctionsDefinition.ALL_HIC15_AIS3:
                return StandardFunction.HIC15_AIS3(param_dict)
            elif function_name == StandardFunctionsDefinition.ALL_BRIC_AIS3:
                return StandardFunction.BRIC_AIS3(param_dict)
            elif function_name == StandardFunctionsDefinition.central_differences:
                return StandardFunction.central_differences(param_dict)
            elif function_name == StandardFunctionsDefinition.UNIVERSAL:
                return StandardFunction.object_strain_stress_hist(param_dict)
            elif function_name == StandardFunctionsDefinition.PERCENTILE:
                return StandardFunction.object_strain_stress_percentile(param_dict)
            elif function_name == StandardFunctionsDefinition.LINSPACE:
                return StandardFunction.linspace(param_dict)
            elif function_name == StandardFunctionsDefinition.FORMAN_RIB_CRITERIA:
                return StandardFunction.forman_criteria(param_dict)
            elif function_name == StandardFunctionsDefinition.CCDF_WEIBULL:
                return StandardFunction.ccdf_weibull(param_dict)
            elif function_name == StandardFunctionsDefinition.AT_INDEX:
                return StandardFunction.at_idx(param_dict)
            elif function_name == StandardFunctionsDefinition.ARGMAX:
                return StandardFunction.argmax(param_dict)
            elif function_name == StandardFunctionsDefinition.CSDM:
                return StandardFunction.csdm(param_dict)
            # END: Standard functions
            if self._user_function is not None:
                if self._check_if_user_function(function_name):
                    function = getattr(self._user_function, function_name)
                    return function(param_dict, self._units)
            else:
                self._logger.emit(LOGConstants.ERROR[0],
                                  function_name + StandardFunctionsDefinition.ERROR_NOT_STANDARD_FUNCTION)
                return

        else:  # data to obtain
            if JsonConstants.VALUE in json_object.keys():
                return json_object[JsonConstants.VALUE]

            data_type = json_object[JsonConstants.TYPE]
            return self._data[data_type].get_data_of_defined_json(json_object, data_offsets)

    def _check_if_user_function(self, function_name):
        '''
        :param function_name:
        :return bool:
        '''
        attributes = inspect.getmembers(self._user_function, predicate=inspect.isfunction)
        if function_name in [att[0] for att in attributes]:
            return True
        return False

    def init_plugin_data(self, update):
        '''
        :param update:
        :return:
        '''
        if self._data is None or update:
            self._data = {data: DataContainer.get_data(data) for data in self._data_requirements}
            for data_name in self._data.keys():
                # if self._code_type == CodeType.MADYMO:
                #     self._data[data_name].set_madymo_data()
                #     self._data[data_name].clean_channel_names()
                #     continue
                if self._data[data_name] is None:
                    self._logger.emit(LOGConstants.ERROR[0], data_name + LoggerERROR.print_statements[1])
                if not self._data[data_name].read_binout_data():
                    self._logger.emit(LOGConstants.ERROR[0], data_name + LoggerERROR.print_statements[2])

    def _reduce_sample_offset(self, json_object, sample_offsets):
        '''

        :param json_object:
        :param data_offsets:

        :return sample:
        '''
        self._get_data_from_json_reduce_samples(json_object)
        self._sample_types = list(set(self._sample_types))
        return_sample = []
        for sample in sample_offsets:
            if sample[0] in self._sample_types:
                return_sample.append(sample)
        self._sample_types.clear()
        return return_sample

    def _get_sample_offset(self, param_dict):
        '''
        get sample offset defined between start and end time

        :param param_dict:

        :return sample offset:
        '''
        start_time = param_dict[PluginsParamDictDef.START_TIME] if PluginsParamDictDef.START_TIME in param_dict \
                        and param_dict[PluginsParamDictDef.START_TIME] != "None" else None
        end_time = param_dict[PluginsParamDictDef.END_TIME] if PluginsParamDictDef.END_TIME in param_dict \
                        and param_dict[PluginsParamDictDef.END_TIME] != "None" else None

        sample_offsets = []
        for key in self._data.keys():
            if key == ObjectConstantsForData.VOLUME:
                continue

            if start_time is not None and end_time is not None:
                if start_time >= end_time:
                    # TODO: Discuss maybe brake
                    self._logger.emit(LOGConstants.ERROR[0],
                                      "End time is smaller or equal as start time! End time set to last value in time step list.")
                    end_time = self._data[key].get_()[-1]
                indices = np.argwhere(
                    (start_time * self._units.second() <= self._data[key].get_interpolated_time()) &
                    (self._data[key].get_interpolated_time() <= end_time * self._units.second()))
            elif start_time is not None and end_time == None:
                indices = np.argwhere(start_time * self._units.second() <= self._data[key].get_interpolated_time())

            elif start_time is None and end_time is not None:
                indices = np.argwhere(self._data[key].get_interpolated_time() <= end_time * self._units.second())
            else:
                indices = np.array([np.arange(0, len(self._data[key].get_interpolated_time()))]).transpose()

            sample_offsets.append((key, indices[0][0], indices[-1][-1]))

        return sample_offsets

    def _get_data_from_json_reduce_samples(self, json_object):
        '''
        get sample offset defined between start and end time

        :param json_object:

        :return sample offset:
        '''
        if JsonConstants.FUNCTION in json_object.keys():  # expected name and params
            parameter_def = json_object[JsonConstants.FUNCTION][JsonConstants.PARAM]

            param_dict = {}
            for key in parameter_def.keys():
                if type(parameter_def[key]) is dict:  # step into recursion
                    param_dict[key] = self._get_data_from_json_reduce_samples(parameter_def[key])
                else:
                    param_dict[key] = parameter_def[key]
        else:  # data to obtain
            if JsonConstants.VALUE in json_object.keys():
                return json_object[JsonConstants.VALUE]
            elif "strain_stress" in json_object.keys():
                self._sample_types.append(json_object[JsonConstants.TYPE])
                return json_object["strain_stress"]
            elif JsonConstants.TYPE in json_object.keys():
                self._sample_types.append(json_object[JsonConstants.TYPE])
                return json_object[JsonConstants.ARRAY]
            else:
                assert False


class PluginInterface(metaclass=abc.ABCMeta):

    # @abc.abstractmethod
    # def _store_data_to_dict(self):
    #     '''
    #     Save the data object to the output.
    #     :return:
    #     '''

    @abc.abstractmethod
    def calculate_and_store_results(self, param_dict):
        '''
        :param param_dict:
        :return:
        '''

    def calculate(self, param_dict):
        param_dict_data = self._dynasaur_definitions.get_param_dict_from_command(command=param_dict)
        self.calculate_and_store_results(param_dict_data)
