"""atoti's entrypoint."""

import atexit

import atoti._compatibility  # Import first to fail fast
import atoti._functions as _functions
import atoti.agg as agg
import atoti.array as array
import atoti.config as config
import atoti.query as query
import atoti.scope as scope

from ._functions import *  # pylint: disable=redefined-builtin
from ._java_utils import retrieve_info_from_jar
from ._licensing import EULA as __license__
from ._licensing import check_license, hide_new_license_agreement_message
from ._sessions import Sessions
from ._tutorial import copy_tutorial
from ._version import VERSION as __version__
from ._widget import register_comm_targets
from .query import open_query_session

# pylint: disable=invalid-name
sessions = Sessions()
create_session = sessions.create_session
_get_session_as_json = sessions._get_session_as_json  # pylint: disable=protected-access
# pylint: enable=invalid-name

register_comm_targets(lambda session_name: sessions[session_name])


@atexit.register
def close() -> None:
    """Close all opened sessions."""
    sessions.close()


(_EDITION, _LICENSE_END_DATE) = retrieve_info_from_jar()
__edition__ = str(_EDITION)

check_license(_EDITION, _LICENSE_END_DATE)

__all__ = [
    copy_tutorial.__name__,
    create_session.__name__,
    open_query_session.__name__,
    "__edition__",
    "__version__",
]
__all__.extend(_functions.__all__)
if __license__:
    __all__.append("__license__")
