""" component module.

"""

from abc import ABC

from mindstone.embedded.components.data import component_data
from mindstone.embedded.platforms import get_current_platform


class ComponentABC(ABC):
    """ component abstract base class.

    """

    def __init__(self, model: str = None):
        self.channels = dict()
        self.model = model
        self.properties = component_data[self.__class__.__name__][model] if model else dict()

    def new_channel(self, name, channel_id: int, channel_type: str, **kwargs):
        self.channels[name] = get_current_platform().new_channel(channel_id, channel_type, **kwargs)
