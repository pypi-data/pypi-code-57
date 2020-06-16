# Copyright 2020 Cognite AS

import numpy as np

from cognite.geospatial.internal import SpatialTypesDTO

try:
    from collections.abc import Mapping  # noqa
    from collections.abc import MutableMapping  # noqa
except ImportError:
    from collections import Mapping  # noqa
    from collections import MutableMapping  # noqa


class SpatialObject:
    def __init__(
        self,
        client=None,
        id: int = None,
        external_id: str = None,
        name: str = None,
        description: str = None,
        source: str = None,
        crs: str = None,
        metadata=None,
        asset_ids=None,
        geometry=None,
        start_time: int = None,
        end_time: int = None,
        last_updated_time: int = None,
        created_time: int = None,
    ):
        self.client = client
        self.id = id
        self.external_id = external_id
        self.name = name
        self.description = description
        self.source = source
        self.crs = crs
        self.metadata = metadata
        self.asset_ids = asset_ids
        self.geometry = geometry
        self.start_time = start_time
        self.end_time = end_time
        self.last_updated_time = last_updated_time
        self.created_time = created_time

        self.double_vector = {}
        self.integer_vector = {}
        self.boolean_vector = {}
        self.text_vector = {}

    def add_double(self, name: str, vector):
        self.double_vector[name] = np.array(vector, dtype=np.double)

    def add_integer(self, name: str, vector):
        self.integer_vector[name] = np.array(vector, dtype=np.int32)

    def add_boolean(self, name: str, vector):
        self.boolean_vector[name] = np.array(vector, dtype=np.bool)

    def add_text(self, name: str, value: str):
        self.text_vector[name] = value

    def __getitem__(self, name: str):
        if name in self.double_vector:
            return self.double_vector[name]

        if name in self.integer_vector:
            return self.integer_vector[name]

        if name in self.boolean_vector:
            return self.boolean_vector[name]

        if name in self.text_vector:
            return self.text_vector[name]

        return None

    def coverage(self, projection: str = None):
        coverage = self.client.get_coverage(id=self.id, projection=projection)
        if coverage is not None:
            return coverage.wkt
        return None

    def get(self):
        if self.geometry.type == SpatialTypesDTO.RASTER:
            active = self.__getitem__("Active")
            x = self.__getitem__("X")
            y = self.__getitem__("Y")
            z = self.__getitem__("Z")
            if z is None:
                data = np.stack((x, y), axis=-1)
            else:
                data = np.stack((x, y, z), axis=-1)
            if active is None:
                return data
            active = active[: len(data)]
            return data[active]
        else:
            return self.geometry.wkt

    def width(self):
        size = self.metadata["Grid_size"]
        if size is not None:
            dimensions = size.split("x")
            return int(dimensions[0].strip())

        return None

    def height(self):
        size = self.metadata["Grid_size"]
        if size is not None:
            dimensions = size.split("x")
            return int(dimensions[1].strip())

    def grid(self):
        if self.geometry.type == SpatialTypesDTO.RASTER:
            active = self.__getitem__("Active")
            x = self.__getitem__("X")
            y = self.__getitem__("Y")
            z = self.__getitem__("Z")
            if z is None:
                points = np.stack((x, y), axis=-1)
            else:
                points = np.stack((x, y, z), axis=-1)

            if active is None:
                rows = self.__getitem__("Row")
                columns = self.__getitem__("Column")
                if rows is None or columns is None:
                    return None
                height = rows.max() - rows.min() + 1
                width = columns.max() - columns.min() + 1
                data = np.ndarray(shape=(height, width, points.shape[1]), dtype=np.double)
                for i in range(len(points)):
                    r = rows[i] - rows.min()
                    c = columns[i] - columns.min()
                    data[r, c] = points[i]
            else:
                width = self.width()
                height = self.height()
                data = np.ndarray(shape=(width, height, points.shape[1]), dtype=np.double)
                size = min(len(active), len(points))
                active_indx = np.argwhere(active[:size] == True)
                for i in active_indx:
                    r = int(i % height)
                    c = int((i - r) / height)
                    data[c, r] = points[i]

            return data
        return None
