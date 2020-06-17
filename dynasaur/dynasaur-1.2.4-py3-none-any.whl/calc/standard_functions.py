import numpy as np
from scipy.integrate import cumtrapz
from scipy.stats import norm

from ..calc.cfc import CFC
from ..calc.risk_function_util import DCDF, RibCriteria
from ..calc.object_calculation_util import ObjectCalcUtil, UniversalLimit
from ..data.ls_dyna import EloutIndex
from ..utils.constants import LOGConstants, PluginsParamDictDef, OutputStringForPlugins


class StandardFunction:

    @staticmethod
    def res(param_dict):
        '''
        :param param_dict:
        :return:
        '''
        return np.linalg.norm(param_dict["data_vector"], axis=1).reshape(-1, 1)

    @staticmethod
    def max(param_dict, absolute=False):
        '''
        :param param_dict:
        :param absolute:
        :return:
        '''
        data_vector = np.abs(param_dict['data_vector']) if absolute else param_dict['data_vector']
        maximum = np.max(data_vector)

        return maximum

    @staticmethod
    def max_in_row(param_dict):
        '''
        :param param_dict:
        :param absolute:
        :return:
        '''

        data_vector = param_dict['data_vector']
        assert len(data_vector.shape) == 2

        return np.max(data_vector, axis=1)

    @staticmethod
    def argmax(param_dict):
        '''
        :param param_dict:
        :param absolute:
        :return:
        '''
        data_vector = np.abs(param_dict['data_vector'])
        index_of_maximum = np.argmax(data_vector)
        return index_of_maximum

    @staticmethod
    def minimum(param_dict):
        '''
        :param param_dict:
        :return:
        '''
        minimum = np.min(param_dict['data_vector'])

        return minimum

    @staticmethod
    def multiplication(param_dict):
        '''
        :param param_dict:
        :return:
        '''
        data_vector_1 = param_dict["data_vector_1"]
        data_vector_2 = param_dict["data_vector_2"]
        return np.multiply(data_vector_1, data_vector_2)

    @staticmethod
    def abs(param_dict):
        '''
        :param param_dict:
        :return:
        '''
        data_vec = param_dict['data_vector']
        return np.abs(data_vec)

    @staticmethod
    def transform_2_origin(param_dict):
        '''
        :param param_dict:
        :return:
        '''
        data_vec = param_dict['data_vector']
        return data_vec - data_vec[0]

    @staticmethod
    def at_idx(param_dict):
        '''
        :param param_dict:
        :return:
        '''
        index = param_dict["index"]
        data_vector = param_dict["data_vector"]
        return data_vector[index]

    @staticmethod
    def linspace(param_dict):
        '''
        :param param_dict:
        :return:
        '''
        start = param_dict["start"]
        stop = param_dict["stop"]
        num = param_dict["num"]
        endpoint = param_dict["endpoint"]
        return np.linspace(start, stop, num, endpoint).reshape(-1, 1)

    @staticmethod
    def subtraction(param_dict):
        '''
        :param param_dict:
        :return:
        '''
        data_vector_1 = param_dict["data_vector_1"]
        data_vector_2 = param_dict["data_vector_2"]
        return np.subtract(data_vector_1, data_vector_2)

    @staticmethod
    def addition(param_dict):
        '''
        :param param_dict:
        :return:
        '''
        data_vector_1 = param_dict["data_vector_1"]
        data_vector_2 = param_dict["data_vector_2"]
        return np.add(data_vector_1, data_vector_2)

    @staticmethod
    def divide(param_dict):
        '''
        :param param_dict:
        :return:
        '''
        data_vector_1 = param_dict["data_vector_1"]
        data_vector_2 = param_dict["data_vector_2"]
        return np.divide(data_vector_1, data_vector_2)

    @staticmethod
    def row_sum(param_dict):
        '''
        :param param_dict:
        :return:
        '''
        mat = param_dict["matrix"]
        return np.sum(mat, axis=1)

    @staticmethod
    def abs_subtraction(param_dict):
        '''
        :param param_dict:
        :return:
        '''
        data_vector_1 = param_dict["data_vector_1"]
        data_vector_2 = param_dict["data_vector_2"]
        return np.abs(np.subtract(data_vector_1, data_vector_2))

    @staticmethod
    def abs_addition(param_dict):
        '''
        :param param_dict:
        :return:
        '''
        data_vector_1 = param_dict["data_vector_1"]
        data_vector_2 = param_dict["data_vector_2"]
        return np.abs(np.add(data_vector_1, data_vector_2))

    @staticmethod
    def abs_subtraction_res(param_dict):
        '''
        :param param_dict:
        :return:
        '''
        data_vector_1 = param_dict["data_vector_1"]
        data_vector_2 = param_dict["data_vector_2"]
        rel_dist = []
        rel_dist_m = np.subtract(data_vector_1, data_vector_2)
        for i in range(len(rel_dist_m)):
            rel_dist.append((rel_dist_m[i, 0] ** 2 + rel_dist_m[i, 1] ** 2 + rel_dist_m[i, 2] ** 2) ** (1 / 2))

        return np.abs(rel_dist)

    @staticmethod
    def ccdf_weibull(param_dict):
        '''
        :param param_dict:
        :return:
        '''
        lambda_ = param_dict["lambda"]
        k = param_dict["k"]
        x = param_dict["x"]
        return 1 - np.exp(-(x / lambda_) ** k)

    @staticmethod
    def cfc(param_dict, units):
        '''
        :param param_dict:
        :param units:
        :return:
        '''
        assert ('time' in param_dict)
        assert (len(param_dict['time']) >= 2)

        Time = (param_dict['time'][1] - param_dict['time'][0])[0] / units.second()
        cfc = CFC(cfc=param_dict['cfc'], T=Time)
        nr_sampled_array_data_series = param_dict['sampled_array'].shape[1]
        mirroring_def = param_dict['mirroring'] if 'mirroring' in param_dict else False
        mirroring = mirroring_def in ["yes", "Yes", "true", "True"]
        return np.transpose(cfc.filter(
            sampled_array=np.transpose(param_dict['sampled_array'].reshape(-1, nr_sampled_array_data_series)),
            time=param_dict['time'], time_to_seconds_factor=units.second(), mirroring_flag=mirroring))

    @staticmethod
    def HIC15_AIS3(param_dict):
        '''
        :param param_dict:
        :param units:
        :return:
        '''
        injuryvalue = param_dict["injuryvalue"]
        offset = param_dict["offset"]
        divide = param_dict["divide"]
        risk = norm.cdf((np.log(injuryvalue[0]) - offset) / divide)

        return risk

    @staticmethod
    def BRIC_AIS3(param_dict):
        '''
        :param param_dict:
        :param units:
        :return:
        '''
        injuryvalue = param_dict["injuryvalue"]
        divide = param_dict["divide"]
        power = param_dict["power"]
        risk = 1 - (np.exp(-((injuryvalue) / divide) ** power))
        return risk

    @staticmethod
    def central_differences(param_dict):
        '''
        :param param_dict:
        :return:
        '''
        v = param_dict['data_vector_1'].flatten()
        time = param_dict['data_vector_2']
        a = np.gradient(v, np.squeeze(time))
        return np.array(a).reshape(-1, 1)


    @staticmethod
    def tibia_index(param_dict, units):
        '''

        :param param_dict:
        :param units:
        :return:
        '''
        mx = param_dict['Mx'] / ((units.meter() ** 2) / (units.second() ** 2))
        my = param_dict['My'] / ((units.meter() ** 2) / (units.second() ** 2))
        fz = param_dict['Fz'] / (units.meter() / (units.second() ** 2))
        critical_bending_moment = param_dict["critical_bending_moment"]  # Input def: Nm
        critical_compression_force = param_dict["critical_compression_force"]  # Input def: N

        mr = np.linalg.norm(np.stack([mx, my], axis=1)[:, :, 0], axis=1)
        ti = np.abs(mr / critical_bending_moment) + np.abs(fz / critical_compression_force)

        return ti

    @staticmethod
    def NIC(param_dict, units):
        '''

        :param param_dict:
        :param units:
        :return:
        '''
        a_t1 = param_dict['a_T1'].flatten()
        a_head = param_dict['a_head'].flatten()
        a_t1 /= units.meter() / (units.second() ** 2)  # a_t1 in [m/s^2]
        a_head /= units.meter() / (units.second() ** 2)  # a_head in [m/s^2]
        a_rel = a_t1 - a_head

        t = param_dict['time'].flatten() / units.second()  # t in [s]
        v_rel = cumtrapz(a_rel, t, initial=0)  # integral

        return_value_nic = 0.2 * a_rel + v_rel ** 2

        return np.array(return_value_nic).reshape(-1, 1)


    @staticmethod
    def HIC_15(param_dict, units, flag=True):
        '''
        time vector in ms
        a_res in mm/s²

        make that consistent and use definitions here!
        use more outputs here!
        possible to return HIC for each time step
        :param param_dict:
        :param units:
        :param flag(HIC15/HIC36):

        :return:
        '''
        t = param_dict['time'].flatten() / units.second()  # t in [s]
        a_res = param_dict['a_res'].flatten()
        a_res /= units.meter() / (units.second() ** 2)  # a_res in [m/s^2]
        a_res /= units.grav_const  # a_res in [g]

        vel = cumtrapz(a_res, t, initial=0)
        hic15 = []
        time2 = []
        dt = (t[1] - t[0])
        if flag:
            nidx = int(round(0.015 / dt))
        else:
            nidx = int(round(0.036 / dt))

        # TODO
        # RuntimeWarning: invalid value encountered in double_
        # scalars temp.append((tdiff) * (((vel[jt] - vel[ut]) / (tdiff)) ** 2.5))
        # problem None values

        for ut in range(len(t) - 1):
            temp = []
            for jt in range(ut + 1, min([len(t), ut + nidx])):
                tdiff = t[jt] - t[ut]
                temp.append(tdiff * (((vel[jt] - vel[ut]) / tdiff) ** 2.5))

            m = np.nanmax(temp)
            hic15.append(m)
            time2.append(t[ut])

        hic15.append(hic15[-1])
        return np.array(hic15).reshape(-1, 1)

    @staticmethod
    def find_index(value, time_history_list, units):
        '''
        :param value:
        :param time_history_list:
        :param units:
        :return:
        '''
        time_hist_array = np.asarray(time_history_list)
        return (np.abs(time_hist_array - (float(value) * units.second()))).argmin()

    @staticmethod
    def object_strain_stress_percentile(param_dict):
        '''
        only one value possible to return

        :param param_dict:

        :return:
        '''
        part_ids = param_dict["object_data"]["part_ids"]
        part_data = param_dict["object_data"]["part_data"]
        part_idx = param_dict["object_data"]["part_idx"]
        time_step_indices = param_dict["object_data"]["time_step_indices"]

        selection_tension_compression = param_dict[PluginsParamDictDef.SELECTION_TENSION_COMPRESSION]
        integration_point = param_dict[PluginsParamDictDef.INTEGRATION_POINT]
        percentile = param_dict[PluginsParamDictDef.PERCENTILE]

        obj_calc = ObjectCalcUtil()
        (function_overall_tension_compression, integration_point_function) = \
            obj_calc.retrieve_functions(selection_tension_compression, integration_point)

        percentile_values = []
        element_count = 0
        for part_id in part_ids:
            index = part_idx[part_id]
            data = part_data[part_id]
            element_ids = np.unique(index[:, 0])
            element_count += len(element_ids)

            for element_id in element_ids:
                row_ids = np.where(index[:, 0] == element_id)[0]

                reduced_integration_point_data = integration_point_function(data[:, row_ids, :], axis=1)
                result_data = function_overall_tension_compression(reduced_integration_point_data, axis=1)
                result_data = result_data[~np.isnan(result_data)]

                # max value for histogram
                max_value_time_index = np.nanargmax(result_data)
                max_value = result_data[max_value_time_index]
                percentile_values.append(max_value)

        # percentile calculation
        percentile_limit = 0
        if len(part_ids):
            percentile_values = sorted(percentile_values)
            if selection_tension_compression == UniversalLimit.TENSION_COMPRESSION_VALUES[2]:
                # compression, flip array to descending order
                percentile_values.reverse()

            value_size = len(percentile_values)
            percentile_value = float(percentile)

            percentile_upper_limit = 1 - (1 / element_count)
            if percentile_value <= percentile_upper_limit:
                percentile_limit = percentile_values[int(np.ceil(percentile_value * value_size))]
            else:
                percentile_limit = percentile_values[int(np.ceil(percentile_upper_limit * value_size))]

        return percentile_limit

    @staticmethod
    def object_strain_stress_hist(param_dict):
        '''

        :param param_dict:
        :param units:

        :return:
        '''
        '''
        only one value possible to return
        maybe some visualisation possible?!?
        '''
        part_ids = param_dict["object_data"]["part_ids"]
        part_data = param_dict["object_data"]["part_data"]
        part_idx = param_dict["object_data"]["part_idx"]

        limit = param_dict[PluginsParamDictDef.LIMIT]
        selection_tension_compression = param_dict[PluginsParamDictDef.SELECTION_TENSION_COMPRESSION]
        integration_point = param_dict[PluginsParamDictDef.INTEGRATION_POINT]

        obj_calc = ObjectCalcUtil()
        (function_overall_tension_compression, integration_point_function) = \
            obj_calc.retrieve_functions(selection_tension_compression, integration_point)

        nr_bins = param_dict["bins"]

        histogram_data = [0] * (nr_bins + 1)
        for part_id in part_ids:
            index = part_idx[part_id]
            data = part_data[part_id]
            element_ids = np.unique(index[:, 0])

            for element_id in element_ids:
                row_ids = np.where(index[:, 0] == element_id)[0]

                reduced_integration_point_data = integration_point_function(data[:, row_ids, :], axis=1)
                result_data = function_overall_tension_compression(reduced_integration_point_data, axis=1)
                result_data = result_data[~np.isnan(result_data)]

                # max value for histogram
                max_value_time_index = np.nanargmax(result_data)
                max_value = result_data[max_value_time_index]

                histogram_index = min(nr_bins, int(nr_bins * max_value / limit))
                histogram_data[histogram_index] += 1

        return np.array([histogram_data]).reshape(-1, 1)

    @staticmethod
    def forman_criteria(param_dict):
        '''

        :param param_dict:
        :param units:

        :return histogram probability broken ribs:
        '''
        part_ids = param_dict["object_data"]["part_ids"]
        part_data = param_dict["object_data"]["part_data"]
        part_idx = param_dict["object_data"]["part_idx"]
        element_type = param_dict["object_data"]["element_type"]

        nr_largest_elements = param_dict[PluginsParamDictDef.NR_LARGESR_EL]
        age = param_dict[PluginsParamDictDef.AGE]
        dcdf = DCDF(param_dict["dcdf"])
        rib_criteria = RibCriteria(dcdf)

        smax = {}
        solid = {OutputStringForPlugins.ALL_MAX: [], OutputStringForPlugins.FRAC_MAX: [],
                 OutputStringForPlugins.ALL_FRAC: np.array([]).astype(dtype=int)}
        shell = {OutputStringForPlugins.ALL_MAX: [], OutputStringForPlugins.FRAC_MAX: [],
                 OutputStringForPlugins.ALL_FRAC: np.array([]).astype(dtype=int)}
        d_matrix = {EloutIndex.SHELL: shell, EloutIndex.SOLID: solid}

        detail_risk_matrix = {}
        detail_risk_matrix["object"] = np.empty((0, 4))
        element_count = 0

        x = dcdf.get_x_where_risk_is_value(0.5)

        # NOTE
        # compare with universal controller
        # calculate mean for the main directions ... maybe
        # maximum value for all timesteps
        # maximum over the time!
        for part_id in part_ids:
            abs_max_all = np.empty(shape=(0, 2))
            index = part_idx[part_id]
            data = part_data[part_id]
            element_ids = np.unique(index[:, 0])
            element_count += len(element_ids)

            for element_id in element_ids:
                row_ids = np.where(index[:, 0] == element_id)[0]
                reduced_integration_point_data = np.mean(data[:, row_ids, :], axis=1)
                result_data = np.max(reduced_integration_point_data, axis=1)
                try:
                    res = np.max(np.abs(result_data[~np.isnan(result_data)]))
                except ValueError:
                    res = 0
                abs_max_all = np.concatenate((abs_max_all, [[res, element_id]]), axis=0)
                if res > x / 100:
                    d_matrix[element_type][OutputStringForPlugins.ALL_FRAC] = np.append(
                        d_matrix[element_type][OutputStringForPlugins.ALL_FRAC], element_id)

            ind_of_largest_elements = abs_max_all[:, 0].argsort()[-nr_largest_elements:][::-1]
            max_index = ind_of_largest_elements[-1]

            abs_max_value = abs_max_all[max_index][0]
            if np.isnan(abs_max_value):
                print(LOGConstants.WARNING[0],
                      "Due to deleted elements, the maximum Value for " + str(part_id) + " is NaN!")

            element_id_abs_max = abs_max_all[max_index][1]

            # store the values for the export set
            d_matrix[element_type][OutputStringForPlugins.ALL_MAX].append(int(element_id_abs_max))
            if rib_criteria.calculate_age_risk(abs_max_value, age) > 0.0:
                d_matrix[element_type][OutputStringForPlugins.FRAC_MAX].append(int(element_id_abs_max))

            smax[part_id] = abs_max_value

        rib_ids = list(smax.keys())

        risk = {id: rib_criteria.calculate_age_risk(smax[id], age) for id in rib_ids}
        broken_ribs_prob = np.array(rib_criteria.calc_num_frac(rib_ids, risk))

        return broken_ribs_prob

    @staticmethod
    def csdm(param_dict):
        '''
        :param param_dict:
        :return:
        '''
        limit = param_dict[PluginsParamDictDef.LIMIT]

        part_ids = param_dict["object_data"]["part_ids"]
        part_data = param_dict["object_data"]["part_data"]
        part_idx = param_dict["object_data"]["part_idx"]
        volume_data = param_dict["object_data"]["part_value"]
        element_volume_by_part_id_and_element_id = param_dict["object_data"]["el_by_part_id_el_id"]

        limit = float(limit) if 0.0 < float(limit) < 1.0 else 0.2
        injvol = 0.0
        sumvol = 0.0

        for part_id in part_ids:
            index = part_idx[part_id]
            data = part_data[part_id]
            part__volume = volume_data[part_id]

            # calculate csdm
            # absolute maximum over all time steps for each element
            abs_max_all = np.max(np.max(np.abs(data), axis=2), axis=0)
            # get element ids which are greater than the limit
            element_ids_greater_limit = index[np.where(abs_max_all > limit)[0], 0]

            csdm = 0.0
            if len(element_ids_greater_limit) != 0:
                volumes = [element_volume_by_part_id_and_element_id[part_id][element_id] for
                           element_id in
                           element_ids_greater_limit]
                csdm = sum(volumes) / part__volume

            sumvol += part__volume
            injvol += (part__volume * csdm)

        csdm = injvol / sumvol
        return csdm

    @staticmethod
    def bric(param_dict, units):
        '''
        :param param_dict:
        :param units:

        :return:
        '''
        r_vel = param_dict["r_vel"] * units.second()
        crit_rx_velocity = param_dict["crit_rx_velocity"]  # [rad/s]
        crit_ry_velocity = param_dict["crit_ry_velocity"]  # [rad/s]
        crit_rz_velocity = param_dict["crit_rz_velocity"]  # [rad/s]
        bric = np.linalg.norm([np.max(np.abs(r_vel[:, 0])) / crit_rx_velocity,
                               np.max(np.abs(r_vel[:, 1])) / crit_ry_velocity,
                               np.max(np.abs(r_vel[:, 2])) / crit_rz_velocity])

        return bric

    @staticmethod
    def uBRIC(param_dict, units):
        '''
        :param param_dict:
        :param units:

        :return:
        '''
        r_vel = param_dict["r_vel"] * units.second()
        r_acc = param_dict["r_acc"] * (units.second() ** 2)

        a = np.max(np.abs(r_vel[:, 0]))

        crit_rx_velocity = param_dict["crit_rx_velocity"]  # [rad/s]
        crit_ry_velocity = param_dict["crit_ry_velocity"]  # [rad/s]
        crit_rz_velocity = param_dict["crit_rz_velocity"]  # [rad/s]

        crit_rx_acceleration = param_dict["crit_rx_acceleration"]  # [rad/s^2]
        crit_ry_acceleration = param_dict["crit_ry_acceleration"]  # [rad/s^2]
        crit_rz_acceleration = param_dict["crit_rz_acceleration"]  # [rad/s^2]

        # absolute max. of r_vel and r_acc normalized
        wx = np.max(np.abs(r_vel[:, 0])) / crit_rx_velocity
        wy = np.max(np.abs(r_vel[:, 1])) / crit_ry_velocity
        wz = np.max(np.abs(r_vel[:, 2])) / crit_rz_velocity
        ax = np.max(np.abs(r_acc[:, 0])) / crit_rx_acceleration
        ay = np.max(np.abs(r_acc[:, 1])) / crit_ry_acceleration
        az = np.max(np.abs(r_acc[:, 2])) / crit_rz_acceleration

        ubric = ((wx + (ax - wx) * np.exp(-(ax / wx))) ** 2 + (wy + (ay - wy) * np.exp(-(ay / wy))) ** 2 + (
                    wz + (az - wz) * np.exp(-(az / wz))) ** 2) ** (1 / 2)

        return ubric

    @staticmethod
    def vc(param_dict, units):
        '''
        :param param_dict:
        :param units:

        :return:
        '''
        scfa = param_dict['scaling_factor']
        defconst = param_dict['deformation_constant']
        y = param_dict['y'] / units.meter()
        t = param_dict['time'] / units.second()

        delta_t = t[1] - t[0]

        # vc derivative
        deformation_velocity = np.zeros(len(t))
        for i in range(2, len(t) - 2):
            deformation_velocity[i] = (8 * (y[i + 1] - y[i - 1]) - (y[i + 2] - y[i - 2]))

        deformation_velocity[0] = (8 * (y[1] - y[0]) - (y[2] - y[0]))
        deformation_velocity[1] = (8 * (y[2] - y[0]) - (y[3] - y[0]))
        deformation_velocity[-2] = (8 * (y[-1] - y[-3]) - (y[-1] - y[-4]))
        deformation_velocity[-1] = (8 * (y[-1] - y[-2]) - (y[-1] - y[-3]))

        deformation_velocity /= (12 * delta_t)
        vc = np.multiply(scfa * (y / defconst), deformation_velocity.reshape(-1, 1))

        return vc

    @staticmethod
    def nij(param_dict, units):
        '''
        :param param_dict:
        :param units:

        :return:
        '''
        force_x = param_dict['force_x'] / (units.meter() / (units.second() ** 2))
        force_z = param_dict['force_z'] / (units.meter() / (units.second() ** 2))
        moment_y = param_dict['moment_y'] / ((units.meter() ** 2) / (units.second() ** 2))

        moc_d = param_dict['distance_occipital_condyle']  # m
        nij_fzc_te = param_dict['nij_fzc_te']  # N
        nij_fzc_co = param_dict['nij_fzc_co']  # N
        nij_myc_fl = param_dict['nij_myc_fl']  # Nm
        nij_myc_ex = param_dict['nij_myc_ex']  # Nm

        nij = np.zeros(shape=(len(force_z)))
        temp_n_value = np.zeros(shape=(4,))

        mtot = moment_y - moc_d * force_x

        for o in range(len(force_z)):
            # NCF
            temp_n_value[0] = force_z[o] / nij_fzc_co + mtot[o] / nij_myc_fl if force_z[o] <= 0 and mtot[o] > 0 else 0
            # NCE
            temp_n_value[1] = force_z[o] / nij_fzc_co + mtot[o] / nij_myc_ex if force_z[o] <= 0 and mtot[o] <= 0 else 0
            # NTF
            temp_n_value[2] = force_z[o] / nij_fzc_te + mtot[o] / nij_myc_fl if force_z[o] > 0 and mtot[o] > 0 else 0
            # NTE
            temp_n_value[3] = force_z[o] / nij_fzc_te + mtot[o] / nij_myc_ex if force_z[o] > 0 and mtot[o] <= 0 else 0

            nij[o] = np.max(temp_n_value)
            temp_n_value = np.zeros(shape=(4,))

        return nij.reshape((-1, 1))

    @staticmethod
    def a3ms(param_dict, units):
        '''
        :param param_dict:
        :param units:
        :return:
        '''

        time = param_dict['time'].flatten()  # t in [s]
        a_res = param_dict['a_res'].flatten()
        # TODO
        # implementation in a central point
        t = time / units.second()
        a_res /= units.meter() / (units.second() ** 2)
        a_res /= units.grav_const

        ls_ind = []
        last = 0  # possible because time is ascending!
        for i in range(len(t)):
            if last == len(t) - 1:
                ls_ind.append((i, last + 1))
                # continue

            for j in range(last, len(t)):
                if t[j] - t[i] > 0.003:  # found start stop indices
                    ls_ind.append((i, j))
                    last = j
                    break

        a3ms_values = np.array([np.min(a_res[ind_tuple[0]:ind_tuple[1]]) for ind_tuple in ls_ind])
        return a3ms_values.reshape((-1, 1))
