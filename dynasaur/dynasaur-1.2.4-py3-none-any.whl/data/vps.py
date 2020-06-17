import h5py
from ..data.dynasaur_definitions import DynasaurDefinitions
from ..utils.logger import ConsoleLogger
from ..utils.constants import VPSDataConstant, DataChannelTypesNodout, DataChannelTypesSecforc


class VPSData:

    def __init__(self, vps_file_path):

        self.file_data = {}             # should be wrapped to binout data.

        self._vps_file_path = vps_file_path
        self._d = dict()

        with h5py.File(self._vps_file_path, 'r') as f:
            f['CSMEXPL/multistate'].visititems(self._get_available_data_types_dict)

        logger = ConsoleLogger()
        self.dynasaur_definitions = DynasaurDefinitions(logger)

    def _get_available_data_types_dict(self, name, node):
        if isinstance(node, h5py.Dataset):
            if node.name.split("/")[-1] == 'res':  # result of data
                if node.parent.name.split("/")[5] in [VPSDataConstant.NODE]:
                    self._set_node_elements(node)

                elif node.parent.name.split("/")[5] in [VPSDataConstant.SECTION]:
                    if node.parent.name.split("/")[5] == VPSDataConstant.SECTION:
                        if VPSDataConstant.SECFORC not in self._d.keys():
                            self._d[VPSDataConstant.SECFORC] = ["ids", "time"]
                            DATA_CHANNEL_TYPES = ['x_force', 'y_force', 'z_force', 'total_force', 'x_moment', 'y_moment', 'z_moment',
                                                  'total_moment', 'x_centroid', 'y_centroid', 'z_centroid', 'area']
                        idx_of_data = node.parent.name.split("/").index(node.parent.name.split("/")[5]) + 1
                        # TODO
                        # print("*******************************************")
                        # print(node.parent.name.split("/")[idx_of_data])
                        # print("-------------------------------------------")
                        if node.parent.name.split("/")[idx_of_data] == VPSDataConstant.SECTION_CENTRE_POSITION:
                            self._d[VPSDataConstant.SECFORC].extend([DataChannelTypesSecforc.X_CENTROID,
                                                                     DataChannelTypesSecforc.Y_CENTROID,
                                                                     DataChannelTypesSecforc.Z_CENTROID])
                        elif node.parent.name.split("/")[idx_of_data] == VPSDataConstant.SECTION_FORCE:
                            self._d[VPSDataConstant.SECFORC].extend([DataChannelTypesSecforc.X_FORCE,
                                                                     DataChannelTypesSecforc.Y_FORCE,
                                                                     DataChannelTypesSecforc.Z_FORCE])
                        elif node.parent.name.split("/")[idx_of_data] == VPSDataConstant.SECTION_MOMENT:
                            self._d[VPSDataConstant.SECFORC].extend([DataChannelTypesSecforc.X_MOMENT,
                                                                     DataChannelTypesSecforc.Y_MOMENT,
                                                                     DataChannelTypesSecforc.Z_MOMENT])

                elif node.parent.name.split("/")[5] in [VPSDataConstant.SECTION]:
                    self._set_section_elements(node)

    def _args_to_data(self, args):
        data_type = ""
        data_channel = ""

        if args[1] == "time":
            with h5py.File(self._vps_file_path, 'r') as f:
                path = "/CSMEXPL/multistate/TIMESERIES1/multientityresults/MODEL/TIME/ZONE1_set1/erfblock/entid"
                path = "/CSMEXPL/multistate/TIMESERIES1/multientityresults/MODEL/TIME/ZONE1_set1/erfblock/res"
                return(f[path][()][:,0,0])

        elif args[1] == "ids":
            with h5py.File(self._vps_file_path, 'r') as f:
                if data_type == VPSDataConstant.SECTION:
                    return f["/CSMEXPL/constant/identifiers/" + VPSDataConstant.SECTION + "/erfblock/uid"][()][:, 0]
                entids = f["/CSMEXPL/multistate/TIMESERIES1/multientityresults/" + VPSDataConstant.NODE + "/Acceleration/ZONE1_set1/erfblock/entid"][()]
                uids = f["/CSMEXPL/constant/identifiers/" + VPSDataConstant.NODE + "/erfblock/uid"][()]

                return uids[entids-1][:, 0]

        if args[0] == VPSDataConstant.NODOUT:
            data_type = VPSDataConstant.NODE
            idx, data_channel = self._get_node_index_and_data_channel(args[1])
        elif args[0] == VPSDataConstant.SECFORC:
            data_type = VPSDataConstant.SECTION
            idx, data_channel = self._get_secforc_index_and_data_channel(args[1])


        search_string = "/CSMEXPL/multistate/TIMESERIES1/multientityresults/" + data_type + "/" + data_channel + "/ZONE1_set1/erfblock/res"

        with h5py.File(self._vps_file_path, 'r') as f:
            return f[search_string][:, :, idx]

    def read(self, *argv):
        read_argv = []

        # 4 cases
        # TODO
        #
        #
        for i in argv:
            read_argv.append(i)
        assert 0 <= len(read_argv) <= 4

        if len(read_argv) == 0:
            return self._d.keys()

        if len(read_argv) == 1:
            if read_argv[0] in self._d.keys():
                return self._d[read_argv[0]]
            else:
                return []

        if len(read_argv) == 2:
            if read_argv[0] in self._d.keys():
                if read_argv[1] in self._d[read_argv[0]]:
                    # return data
                    return self._args_to_data(read_argv)
                else:
                    return []
            else:
                return []

    def _visitor_func(self, name, node):
        if isinstance(node, h5py.Dataset):
            print(node.name)
        else:
            #TODO more about that later on!
            pass

    def _get_node_index_and_data_channel(self, arg):
        # NODE
        if arg == DataChannelTypesNodout.X_COORDINATE or \
                arg == DataChannelTypesNodout.Y_COORDINATE or arg == DataChannelTypesNodout.Z_COORDINATE:
            idx = 0 if arg.startswith("x") else (1 if arg.startswith("y") else 2)
            data_channel = VPSDataConstant.COORDINATE
        elif arg == DataChannelTypesNodout.X_DISPLACEMENT or \
                arg == DataChannelTypesNodout.Y_DISPLACEMENT or arg == DataChannelTypesNodout.Z_DISPLACEMENT:
            idx = 0 if arg.startswith("x") else (1 if arg.startswith("y") else 2)
            data_channel = VPSDataConstant.TRANSLATION_DISPLACEMENT
        elif arg == DataChannelTypesNodout.X_VELOCITY or \
                arg == DataChannelTypesNodout.Y_VELOCITY or arg == DataChannelTypesNodout.Z_VELOCITY:
            idx = 0 if arg.startswith("x") else (1 if arg.startswith("y") else 2)
            data_channel = VPSDataConstant.VELOCITY
        elif arg == DataChannelTypesNodout.X_ACCELERATION or \
                arg == DataChannelTypesNodout.Y_ACCELERATION or arg == DataChannelTypesNodout.Z_ACCELERATION:
            idx = 0 if arg.startswith("x") else (1 if arg.startswith("y") else 2)
            data_channel = VPSDataConstant.ACCELERATION
        elif arg == DataChannelTypesNodout.RX_DISPLACEMENT or \
                arg == DataChannelTypesNodout.RY_DISPLACEMENT or arg == DataChannelTypesNodout.RZ_DISPLACEMENT:
            idx = 0 if arg.startswith("rx") else (1 if arg.startswith("ry") else 2)
            data_channel = VPSDataConstant.ROTATION_ANGLE
        elif arg == DataChannelTypesNodout.RX_VELOCITY or \
                arg == DataChannelTypesNodout.RY_VELOCITY or arg == DataChannelTypesNodout.RZ_VELOCITY:
            idx = 0 if arg.startswith("rx") else (1 if arg.startswith("ry") else 2)
            data_channel = VPSDataConstant.ROTATION_VELOCITY
        elif arg == DataChannelTypesNodout.RX_ACCELERATION or \
                arg == DataChannelTypesNodout.RY_ACCELERATION or arg == DataChannelTypesNodout.RZ_ACCELERATION:
            idx = 0 if arg.startswith("rx") else (1 if arg.startswith("ry") else 2)
            data_channel = VPSDataConstant.ROTATION_ACCELERATION
        else:
            #TODO: add console logger
            print("ID FAIL")
            return

        return idx, data_channel

    def _get_secforc_index_and_data_channel(self, arg):
        # SECTION
        if arg == DataChannelTypesSecforc.X_CENTROID or \
                arg == DataChannelTypesSecforc.Y_CENTROID or arg == DataChannelTypesSecforc.Z_CENTROID:
            idx = 0 if arg.startswith("x") else (1 if arg.startswith("y") else 2)
            data_channel = VPSDataConstant.SECTION_CENTRE_POSITION
        elif arg == DataChannelTypesSecforc.X_FORCE or \
                arg == DataChannelTypesSecforc.Y_FORCE or arg == DataChannelTypesSecforc.Z_FORCE:
            idx = 0 if arg.startswith("x") else (1 if arg.startswith("y") else 2)
            data_channel = VPSDataConstant.SECTION_FORCE
        elif arg == DataChannelTypesSecforc.X_MOMENT or \
                arg == DataChannelTypesSecforc.Y_MOMENT or arg == DataChannelTypesSecforc.Z_MOMENT:
            idx = 0 if arg.startswith("x") else (1 if arg.startswith("y") else 2)
            data_channel = VPSDataConstant.SECTION_MOMENT
        else:
            #TODO: add console logger
            print("ID FAIL")
            return

        return idx, data_channel

    def _set_node_elements(self, node):
        if node.parent.name.split("/")[5] == VPSDataConstant.NODE:
            if VPSDataConstant.NODOUT not in self._d.keys():
                self._d[VPSDataConstant.NODOUT] = ["ids", "time"]
            idx_of_data = node.parent.name.split("/").index(node.parent.name.split("/")[5]) + 1
            # TODO
            if node.parent.name.split("/")[idx_of_data] == VPSDataConstant.COORDINATE:
                self._d[VPSDataConstant.NODOUT].extend([DataChannelTypesNodout.X_COORDINATE,
                                                        DataChannelTypesNodout.Y_COORDINATE,
                                                        DataChannelTypesNodout.Z_COORDINATE])
            elif node.parent.name.split("/")[idx_of_data] == VPSDataConstant.TRANSLATION_DISPLACEMENT:
                self._d[VPSDataConstant.NODOUT].extend([DataChannelTypesNodout.X_DISPLACEMENT,
                                                        DataChannelTypesNodout.Y_DISPLACEMENT,
                                                        DataChannelTypesNodout.Z_DISPLACEMENT])
            elif node.parent.name.split("/")[idx_of_data] == VPSDataConstant.VELOCITY:
                self._d[VPSDataConstant.NODOUT].extend([DataChannelTypesNodout.X_VELOCITY,
                                                        DataChannelTypesNodout.Y_VELOCITY,
                                                        DataChannelTypesNodout.Z_VELOCITY])
            elif node.parent.name.split("/")[idx_of_data] == VPSDataConstant.ACCELERATION:
                self._d[VPSDataConstant.NODOUT].extend([DataChannelTypesNodout.X_ACCELERATION,
                                                        DataChannelTypesNodout.Y_ACCELERATION,
                                                        DataChannelTypesNodout.Z_ACCELERATION])
            elif node.parent.name.split("/")[idx_of_data] == VPSDataConstant.ROTATION_ANGLE:
                self._d[VPSDataConstant.NODOUT].extend([DataChannelTypesNodout.RX_DISPLACEMENT,
                                                        DataChannelTypesNodout.RY_DISPLACEMENT,
                                                        DataChannelTypesNodout.RZ_DISPLACEMENT])
            elif node.parent.name.split("/")[idx_of_data] == VPSDataConstant.ROTATION_VELOCITY:
                self._d[VPSDataConstant.NODOUT].extend([DataChannelTypesNodout.RX_VELOCITY,
                                                        DataChannelTypesNodout.RY_VELOCITY,
                                                        DataChannelTypesNodout.RZ_VELOCITY])
            elif node.parent.name.split("/")[idx_of_data] == VPSDataConstant.ROTATION_ACCELERATION:
                self._d[VPSDataConstant.NODOUT].extend([DataChannelTypesNodout.RX_ACCELERATION,
                                                        DataChannelTypesNodout.RY_ACCELERATION,
                                                        DataChannelTypesNodout.RZ_ACCELERATION])

    def _set_section_elements(self, node):
        if node.parent.name.split("/")[5] == VPSDataConstant.SECTION:
            if VPSDataConstant.SECFORC not in self._d.keys():
                self._d[VPSDataConstant.SECFORC] = ["ids", "time"]
            idx_of_data = node.parent.name.split("/").index(node.parent.name.split("/")[5]) + 1
            # #         # TODO
            #         print("*******************************************")
            #         print(node.parent.name.split("/")[idx_of_data])
            #         print("-------------------------------------------")
            if node.parent.name.split("/")[idx_of_data] == VPSDataConstant.SECTION_CENTRE_POSITION:
                self._d[VPSDataConstant.SECFORC].extend([DataChannelTypesSecforc.X_CENTROID,
                                                         DataChannelTypesSecforc.Y_CENTROID,
                                                         DataChannelTypesSecforc.Z_CENTROID])
            elif node.parent.name.split("/")[idx_of_data] == VPSDataConstant.SECTION_FORCE:
                self._d[VPSDataConstant.SECFORC].extend([DataChannelTypesSecforc.X_FORCE,
                                                         DataChannelTypesSecforc.Y_FORCE,
                                                         DataChannelTypesSecforc.Z_FORCE])
            elif node.parent.name.split("/")[idx_of_data] == VPSDataConstant.SECTION_MOMENT:
                self._d[VPSDataConstant.SECFORC].extend([DataChannelTypesSecforc.X_MOMENT,
                                                         DataChannelTypesSecforc.Y_MOMENT,
                                                         DataChannelTypesSecforc.Z_MOMENT])

