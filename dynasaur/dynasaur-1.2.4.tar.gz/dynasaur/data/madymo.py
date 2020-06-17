from ..utils.constants import LOGConstants, UnitsConstants, MadymoConstants, DataChannelTypesNodout, DataChannelTypesSecforc
import numpy as np
import h5py
from ..utils.logger import ConsoleLogger
from ..data.dynasaur_definitions import DynasaurDefinitions


class MadymoData:

    def _extratct_data(self, node, data_type, idx_mady_mo_data):

        for idx, id_ in enumerate(self._d['nodout']['ids']):
            keys = [i for i in node.keys() if i.startswith("SIGNAL")]
            for key in keys:
                id_to_compare = ''.join([chr(i) for i in list(node[key].attrs.items())[0][1] if i != 0]).split(" ")[0]
                if id_to_compare == id_:
                    self._d["nodout"][data_type][:, idx] = node[key]["Y_VALUES"][idx_mady_mo_data, :]

    def __init__(self, madymo_file_path):
        print(madymo_file_path)
        self.file_data = {}             # should be wrapped to binout data.

        self._madymo_file_path = madymo_file_path
        self._d = dict()

        with h5py.File(self._madymo_file_path, 'r') as f:
            f['MODEL_0'].visititems(self._get_available_data_types_dict)
            # extend the data dictionary
            dimension = (self._d['nodout']['time'].shape[0], len(self._d['nodout']['ids']))
            data_types_to_be_filled = [i for i in self._d['nodout'].keys() if i != "ids" and i != "time"]
            for data_type in data_types_to_be_filled:
                self._d['nodout'][data_type] = np.empty(dimension)
                self._d['nodout'][data_type][:] = np.nan

                if data_type == DataChannelTypesNodout.RX_DISPLACEMENT or \
                        data_type == DataChannelTypesNodout.RY_DISPLACEMENT or \
                        data_type == DataChannelTypesNodout.RZ_DISPLACEMENT:
                    idx_mady_mo_data = 0 if data_type == DataChannelTypesNodout.RX_DISPLACEMENT else (1 if data_type == DataChannelTypesNodout.RY_DISPLACEMENT else 2)
                    self._extratct_data(f["MODEL_0/Angular displacements"], data_type, idx_mady_mo_data=idx_mady_mo_data)

                elif data_type == DataChannelTypesNodout.RX_VELOCITY or \
                        data_type == DataChannelTypesNodout.RY_VELOCITY or \
                        data_type == DataChannelTypesNodout.RZ_VELOCITY:
                    idx_mady_mo_data = 0 if data_type == DataChannelTypesNodout.RX_VELOCITY else (1 if data_type == DataChannelTypesNodout.RY_VELOCITY else 2)
                    self._extratct_data(f["MODEL_0/Angular velocities"], data_type, idx_mady_mo_data=idx_mady_mo_data)

                elif data_type == DataChannelTypesNodout.RX_ACCELERATION or \
                        data_type == DataChannelTypesNodout.RY_ACCELERATION or \
                        data_type == DataChannelTypesNodout.RZ_ACCELERATION:
                    idx_mady_mo_data = 0 if data_type == DataChannelTypesNodout.RX_ACCELERATION else (1 if data_type == DataChannelTypesNodout.RY_ACCELERATION else 2)
                    self._extratct_data(f["MODEL_0/Angular accelerations"], data_type, idx_mady_mo_data=idx_mady_mo_data)

                elif data_type == DataChannelTypesNodout.X_ACCELERATION or \
                        data_type == DataChannelTypesNodout.Y_ACCELERATION or \
                        data_type == DataChannelTypesNodout.Z_ACCELERATION:
                    idx_mady_mo_data = 1 if data_type == DataChannelTypesNodout.X_ACCELERATION else (2 if data_type == DataChannelTypesNodout.Y_ACCELERATION else 3)
                    self._extratct_data(f["MODEL_0/Linear accelerations"], data_type,idx_mady_mo_data=idx_mady_mo_data)

                elif data_type == DataChannelTypesNodout.X_VELOCITY or \
                        data_type == DataChannelTypesNodout.Y_VELOCITY or \
                        data_type == DataChannelTypesNodout.Z_VELOCITY:
                    idx_mady_mo_data = 1 if data_type == DataChannelTypesNodout.X_VELOCITY else (2 if data_type == DataChannelTypesNodout.Y_VELOCITY else 3)
                    self._extratct_data(f["MODEL_0/Linear velocities"], data_type, idx_mady_mo_data=idx_mady_mo_data)

                elif data_type == DataChannelTypesNodout.X_COORDINATE or \
                        data_type == DataChannelTypesNodout.Y_COORDINATE or \
                        data_type == DataChannelTypesNodout.Z_COORDINATE:
                    idx_mady_mo_data = 1 if data_type == DataChannelTypesNodout.X_COORDINATE else (2 if data_type == DataChannelTypesNodout.Y_COORDINATE else 3)
                    self._extratct_data(f["MODEL_0/Linear positions"], data_type, idx_mady_mo_data=idx_mady_mo_data)

                elif data_type == DataChannelTypesNodout.X_DISPLACEMENT or \
                        data_type == DataChannelTypesNodout.Y_DISPLACEMENT or \
                        data_type == DataChannelTypesNodout.Z_DISPLACEMENT:
                    idx_mady_mo_data = 1 if data_type == DataChannelTypesNodout.X_DISPLACEMENT else (2 if data_type == DataChannelTypesNodout.Y_DISPLACEMENT else 3)
                    self._extratct_data(f["MODEL_0/Linear displacements"], data_type, idx_mady_mo_data=idx_mady_mo_data)

            f['MODEL_0'].visititems(self._insert_data)

        logger = ConsoleLogger()
        self.dynasaur_definitions = DynasaurDefinitions(logger)

    def _insert_data(self, name, node):
        data_types_to_be_filled = [i for i in self._d['nodout'].keys() if i != "ids" and i != "time"]

        pass
        #print(data_types_to_be_filled)

    def _add_ids(self, node, data_type):
        # add signal ids
        signals = [signal for signal in node.keys() if signal.startswith("SIGNAL")]
        for signal in signals:
            id_string = ''.join([chr(i) for i in list(node[signal].attrs.items())[0][1] if i != 0])
            id_string = id_string.split(" ")[0]
            assert(id_string not in self._d[data_type]["ids"])
            # if assert: ID is already in id list

            self._d[data_type]["ids"].append(id_string)

    def _add_time(self, node, data_type):
        # add signal ids
        time_ = [signal for signal in node.keys() if signal == "X_VALUES"]
        assert len(time_) == 1
        if self._d[data_type]["time"] is None:
            self._d[data_type]["time"] = node["X_VALUES"][:]
        else:
            # Issue with different time lengths or different values
            assert self._d[data_type]["time"].shape == node["X_VALUES"][:].shape
            assert all([self._d[data_type]["time"][i] == node["X_VALUES"][i] for i in np.arange(self._d[data_type]["time"].shape[0])])

    def _get_available_data_types_dict(self, name, node):

        if hasattr(node, "value"):
            # component names
            if "COMP" in node.name.split("/"):
                if 'nodout' not in self._d.keys():
                    if node.parent.name.split("/")[-1].startswith("Angular ") or node.parent.name.split("/")[-1].startswith("Linear "):
                        self._d['nodout'] = {"ids": [], "time": None}

                if 'glstat' not in self._d.keys():
                    if node.parent.name.split("/")[-1].startswith("Energy output"):
                        self._d['glstat'] = {"time": None}

                if node.parent.name.split("/")[-1].startswith("Energy output"):
                    # TODO
                    # self._d['glstat'][DataChannelTypesNodout.RX_ACCELERATION] = None
                    # self._d['glstat'][DataChannelTypesNodout.RY_ACCELERATION] = None
                    # self._d['glstat'][DataChannelTypesNodout.RZ_ACCELERATION] = None
                    # self._add_ids(node.parent, data_type="glstat")
                    self._add_time(node.parent, data_type="glstat")

                if node.parent.name.split("/")[-1].startswith("Angular accelerations"):
                    self._d['nodout'][DataChannelTypesNodout.RX_ACCELERATION] = None
                    self._d['nodout'][DataChannelTypesNodout.RY_ACCELERATION] = None
                    self._d['nodout'][DataChannelTypesNodout.RZ_ACCELERATION] = None
                    self._add_ids(node.parent, data_type="nodout")
                    self._add_time(node.parent, data_type="nodout")

                elif node.parent.name.split("/")[-1].startswith("Angular velocity"):
                    self._d['nodout'][DataChannelTypesNodout.RX_VELOCITY] = None
                    self._d['nodout'][DataChannelTypesNodout.RY_VELOCITY] = None
                    self._d['nodout'][DataChannelTypesNodout.RZ_VELOCITY] = None
                    self._add_ids(node.parent, data_type="nodout")
                    self._add_time(node.parent, data_type="nodout")

                elif node.parent.name.split("/")[-1].startswith("Angular displacements"):
                    self._d['nodout'][DataChannelTypesNodout.RX_DISPLACEMENT] = None
                    self._d['nodout'][DataChannelTypesNodout.RY_DISPLACEMENT] = None
                    self._d['nodout'][DataChannelTypesNodout.RZ_DISPLACEMENT] = None
                    self._add_ids(node.parent, data_type="nodout")
                    self._add_time(node.parent, data_type="nodout")

                elif node.parent.name.split("/")[-1].startswith("Linear accelerations"):
                    self._d['nodout'][DataChannelTypesNodout.X_ACCELERATION] = None
                    self._d['nodout'][DataChannelTypesNodout.Y_ACCELERATION] = None
                    self._d['nodout'][DataChannelTypesNodout.Z_ACCELERATION] = None
                    self._add_ids(node.parent, data_type="nodout")
                    self._add_time(node.parent, data_type="nodout")

                elif node.parent.name.split("/")[-1].startswith("Linear displacements"):
                    self._d['nodout'][DataChannelTypesNodout.X_DISPLACEMENT] = None
                    self._d['nodout'][DataChannelTypesNodout.Y_DISPLACEMENT] = None
                    self._d['nodout'][DataChannelTypesNodout.Z_DISPLACEMENT] = None
                    self._add_ids(node.parent, data_type="nodout")
                    self._add_time(node.parent, data_type="nodout")

                elif node.parent.name.split("/")[-1].startswith("Linear positions"):
                    self._d['nodout'][DataChannelTypesNodout.X_COORDINATE] = None
                    self._d['nodout'][DataChannelTypesNodout.Y_COORDINATE] = None
                    self._d['nodout'][DataChannelTypesNodout.Z_COORDINATE] = None
                    self._add_ids(node.parent, data_type="nodout")
                    self._add_time(node.parent, data_type="nodout")

                elif node.parent.name.split("/")[-1].startswith("Linear velocities"):
                    self._d['nodout'][DataChannelTypesNodout.X_VELOCITY] = None
                    self._d['nodout'][DataChannelTypesNodout.Y_VELOCITY] = None
                    self._d['nodout'][DataChannelTypesNodout.Z_VELOCITY] = None
                    self._add_ids(node.parent, data_type="nodout")
                    self._add_time(node.parent, data_type="nodout")

    def read(self, *argv):
        read_argv = []

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
                    return self._d[read_argv[0]][read_argv[1]]
                else:
                    return []
            else:
                return []

