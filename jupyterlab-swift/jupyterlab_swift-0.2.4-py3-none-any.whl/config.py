from os import environ
from traitlets import Integer, Unicode
from traitlets.config import Configurable

class SwiftConfig(Configurable):
    """User- or operator-configurable properties.
    """
    root_container = Unicode(
        'jupyter:{project_name}', config=True,
        help=('A root Swift container to mount. If not defined, all containers '
              'are mounted under a dummy directory')
    )
    max_file_size_bytes = Integer(
        100*1024*1024, config=True,
        help=('Maximum file size (in bytes) to allow when uploading '
              'or downloading')
    )
