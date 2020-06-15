""" body engine module.

"""

import math

from mindstone.control.engines.engine import EngineABC
from mindstone.control.network import Node, Network


def magnitude(*components) -> float:
    return math.sqrt(sum([c ** 2 for c in components]))


def cartesian_to_spherical(x: float = 0, y: float = 0, z: float = 0) -> tuple:
    r = magnitude(x, y, z)
    theta = math.acos(z / r)
    phi = math.acos(x / (r * math.sin(theta)))
    return r, theta, phi


def spherical_to_cartesian(r: float = 0, theta: float = 0, phi: float = 0) -> tuple:
    x = r * math.sin(theta) * math.cos(phi)
    y = r * math.sin(theta) * math.sin(phi)
    z = r * math.cos(phi)
    return x, y, z


def get_absolute_position(self, absolute_position: tuple, relative_position: tuple) -> tuple:
    pass


def get_absolute_orientation(self, absolute_orientation: tuple, relative_orientation: tuple) -> tuple:
    pass


class Point(Node):
    """ point class.

    """
    PARAMETERS = {"x_trans", "y_trans", "z_trans", "x_rot", "y_rot", "z_rot"}

    def __init__(self, position, orientation):
        self.position = list(position)
        self.orientation = list(orientation)
        self.references = set()
        super().__init__()

    def new_reference(self, parameter: str, component_name: str, state_key: str):
        if parameter not in self.PARAMETERS:
            raise ValueError("Invalid degree of freedom '{}' provided. Try one of these {}".format(
                parameter, self.PARAMETERS))
        self.references.add((parameter, component_name, state_key))

    def update(self, parameters: dict):
        for parameter, state_value in parameters.items():
            if parameter == "x_trans":
                self.position[0] = state_value
            elif parameter == "y_trans":
                self.position[1] = state_value
            elif parameter == "z_trans":
                self.position[2] = state_value
            elif parameter == "x_rot":
                self.orientation[0] = state_value
            elif parameter == "y_rot":
                self.orientation[1] = state_value
            elif parameter == "z_rot":
                self.orientation[2] = state_value


class BodyEngine(EngineABC, Network):
    """ body engine class.

    """

    def update(self, component_observations: dict):
        for point in self.nodes:
            if not isinstance(point, Point):
                raise TypeError
            for degree_of_freedom, component_name, state_key in point.references:
                value = float(component_observations[component_name][state_key])
                point.update({degree_of_freedom: value})

    def configuration(self) -> dict:
        pass

    def resolve(self) -> dict:
        return self._resolve_util(self.nodes[self.start])

    def _resolve_util(self, point: Point, points: dict = None) -> dict:
        points = {} if points is None else points
        if len(point.children) == 0:
            return points

    def _get_absolute_position(self, prev_absolute: tuple, relative: tuple) -> tuple:
        pass

    def _get_absolute_orientation(self, prev_absolute: tuple, relative: tuple) -> tuple:
        pass
