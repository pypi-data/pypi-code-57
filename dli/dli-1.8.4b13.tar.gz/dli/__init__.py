import os
import warnings
import os

warnings.filterwarnings(
    'always', module="dli"
)

warnings.filterwarnings(
    'ignore', module="dli", category=ResourceWarning
)

__version__ = '1.8.4b13'
__product__ = "ihsm-datalake"


try:
    import simplejson as _  # noqa
    warnings.warn(
        'Incompatible Package `simplejson`.\n\n'
        '\t`simplejson` is a backport of the built in json library in Python. '
        'It contains subtle differences, and is not intended for use beyond '
        'Python 2.6. Please uninstall `simplejson` by running:\n\n'
        '\t\tpip uninstall simplejson\n\n'
        '\tOr run the DLI from a virtual environment as it is known to cause '
        'issues within the DLI.\n',
        ImportWarning
    )
except ImportError:
    pass


def connect(api_key=None,
            root_url="https://catalogue.datalake.ihsmarkit.com/__api",
            host=None,
            debug=None,
            strict=None,
            use_keyring=True,
            log_level=None,
            ):

    from dli.client.session import start_session

    return start_session(
        api_key,
        root_url=root_url,
        host=host,
        debug=debug,
        strict=strict,
        use_keyring=use_keyring,
        log_level=log_level,
    )

