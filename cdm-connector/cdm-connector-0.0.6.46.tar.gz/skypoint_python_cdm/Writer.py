import abc

class Writer(metaclass=abc.ABCMeta):
        @abc.abstractmethod
        def write_df(self, location, dataframe, number_of_partition=5): ()

        @abc.abstractmethod
        def get_existing(self, location, snapshot_dir_name): ()

        @abc.abstractmethod
        def write_json(self, location, json_dict, lease_id=None): ()
