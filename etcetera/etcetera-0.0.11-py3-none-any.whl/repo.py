import importlib
import re


class Repo:

    @classmethod
    def load(cls, url, **conf):
        mtc = re.match(r'([a-zA-Z\d]+)://', url)
        if mtc is None:
            raise ValieError('Could not determine URL protocol: ' + url)
        protocol = mtc.group(1)

        try:
            impl = importlib.import_module('etcetera.impl.' + protocol)
            return impl.load(url, **conf)
        except ImportError:
            raise
            raise ValueError(f'Implementation for the URL protocol {protocol} not found')