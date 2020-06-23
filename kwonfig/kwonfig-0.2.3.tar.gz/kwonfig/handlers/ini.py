from kwonfig.constants import INI_SUPPORTED
from . import Handler

if INI_SUPPORTED:
    import ini


class IniHandler(Handler):
    enabled = INI_SUPPORTED

    suffix = 'ini'

    @classmethod
    def load(cls, fp) -> Handler.Data:
        content: str = fp.read()
        return ini.parse(content)
