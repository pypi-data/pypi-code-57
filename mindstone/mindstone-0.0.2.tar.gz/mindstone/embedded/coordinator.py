""" coordinator module.

"""

from mindstone.embedded.components import COMPONENT_REGISTER
from mindstone.embedded.components.component import ComponentABC
from mindstone.embedded.components.mutable import MutableComponentABC
from mindstone.embedded.components.observable import ObservableComponentABC
from mindstone.embedded.reporting import display


class Coordinator(object):
    """ coordinator class.

    """

    def __init__(self, components: dict = None):
        self.components = components if components else dict()

    def add_component(self, name: str, component_type: str, **kwargs):
        self.components[name] = COMPONENT_REGISTER[component_type](**kwargs)

    def update(self, configurations: dict):
        for name, configuration in configurations.items():
            if not isinstance(self.components[name], MutableComponentABC):
                raise TypeError("Object with name '{}' to update is not of type {}".format(
                    name,
                    MutableComponentABC.__class__.__name__))
            self.components[name].update(**configuration)
            display("Updated component '{}' with configuration: {}".format(name, configuration))

    def observations(self) -> dict:
        observation_data = dict()
        for name in self.components.keys():
            if isinstance(self.components[name], ObservableComponentABC):
                observation_data[name] = self.components[name].observe()
            display("Observed component '{}': {}".format(name, observation_data[name]))
        return observation_data

    def properties(self) -> dict:
        components = dict()
        for name in self.components.keys():
            if not isinstance(self.components[name], ComponentABC):
                raise TypeError("Object is not of type {}".format(
                    ComponentABC.__class__.__name__))
            components[name] = self.components[name].properties
        return components
