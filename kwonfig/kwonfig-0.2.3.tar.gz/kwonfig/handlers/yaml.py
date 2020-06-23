from kwonfig.constants import YAML_SUPPORTED
from . import Handler

if YAML_SUPPORTED:
    from ruamel import yaml


class YamlHandler(Handler):
    enabled = YAML_SUPPORTED

    suffix = ('yaml', 'yml')

    @classmethod
    def load(cls, fp) -> Handler.Data:
        data = yaml.load(fp, Loader=yaml.SafeLoader)
        if data is None:
            data = {}

        return data
