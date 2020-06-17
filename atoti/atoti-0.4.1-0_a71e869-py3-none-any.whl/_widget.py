"""Interactive dataviz widget."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from time import time
from typing import TYPE_CHECKING, Any, Callable, Optional

from ._ipython_utils import run_from_ipython
from ._version import VERSION

if TYPE_CHECKING:
    from ipykernel.comm import Comm
    from .session import Session

_TOKEN_COMM_TARGET_NAME = "atoti-token"  # nosec
_WIDGET_COMM_TARGET_NAME = "atoti-widget"

# Number of seconds to wait for the JupyterLab extension to open a comm with us.
# This is only used for the first displayed widget.
# If we have no response before the end of this period, we will consider that
# the JupyterLab extension is disabled and will unblock the capture of execute_request events.
_MAX_JUPYTERLAB_EXTENSION_RESPONSE_TIME = 4.20

# Same naming scheme as Plotly:
# https://github.com/plotly/plotly.py/blob/3ca829c73bd4841666c8b810f5e8457514eb3c99/packages/javascript/jupyterlab-plotly/src/javascript-renderer-extension.ts#L24-L28
_WIDGET_MIME_TYPE = f"application/vnd.atoti.v{VERSION.split('.')[0]}+json"


@dataclass
class Status:
    """The status in which the kernel is regarding the JupyterLab extension."""

    captured_once: bool = False
    extension_enabled: bool = False
    widget_loaded: bool = False


_STATUS = Status()


def register_comm_targets(get_session: Callable[[str], Session]):
    """Register Jupyter comm targets with our extension.

    - _TOKEN_COMM_TARGET_NAME sends fresh admin tokens.
      It stays open until the session is stopped or the browser tab is closed.
    - _WIDGET_COMM_TARGET_NAME detects if our extension is enabled
      and sends session details to the extension.
      It only stays open during the widget loading process.

    Args:
        get_session: the function to call to get a session by its name.

    """
    if not run_from_ipython():
        return
    from IPython import get_ipython

    ipython = get_ipython()

    if not hasattr(ipython, "kernel") or not hasattr(ipython.kernel, "comm_manager"):
        # When run from IPython or another less elaborated environment
        # than JupyterLab, these attributes might be missing.
        # In that case, there is no need to register anything.
        return

    def _token_callback(comm: Comm, open_msg: Any):  # type: ignore
        session_name = open_msg["content"]["data"]["session"]
        session = get_session(session_name)
        comm.send(
            {"token": session._generate_token(),}  # pylint: disable= protected-access
        )

    def _widget_callback(comm: Comm, open_msg: Any):  # type: ignore
        @comm.on_msg
        def _recv(msg: Any):
            if msg["content"]["data"]["loaded"]:
                _STATUS.widget_loaded = True
                comm.close()

        # If the comm is established, it means the extension asked for it.
        _STATUS.extension_enabled = True
        session_name = open_msg["content"]["data"]["session"]
        session = get_session(session_name)
        comm.send(
            {
                "executionCount": ipython.execution_count,
                "session": {
                    "port": session.port,
                    "token": session._generate_token(),  # pylint: disable= protected-access
                    "url": session.url,
                },
            }
        )

    ipython.kernel.comm_manager.register_target(
        _TOKEN_COMM_TARGET_NAME, _token_callback
    )
    ipython.kernel.comm_manager.register_target(
        _WIDGET_COMM_TARGET_NAME, _widget_callback
    )


def _capture_until_widget_loaded(ipython: Any):
    """Capture execute_request events until the widget is loaded and then replay them.

    The goal is to block execution of other cells until the ActiveUI widget is done loading.
    This is to prevent the ActiveUI widget from getting back a cellset corresponding to a state of
    the cube different than the one it was in when cube.visualize() was called.

    Adapted from:
    https://github.com/kafonek/ipython_blocking/blob/98082426d5e77d854b1d48f2a7c75cb8bc6b1ae2/ipython_blocking/ipython_blocking.py

    Args:
        ipython: instance of IPython.

    """
    captured_events = []
    kernel = ipython.kernel
    original_handler = kernel.shell_handlers["execute_request"]

    started_capture_at = time()
    _STATUS.widget_loaded = False

    # Overwrite IPython handler to capture instead of executing new cell-execution requests.
    kernel.shell_handlers[
        "execute_request"
    ] = lambda stream, ident, parent: captured_events.append((stream, ident, parent))

    while True:
        if _STATUS.widget_loaded:
            break

        # The time out logic only needs to be run for the first displayed widget.
        # Because after that, we know whether the extension is enabled or not.
        if not _STATUS.extension_enabled:
            no_response_from_jupyterlab_extension = (
                time() > started_capture_at + _MAX_JUPYTERLAB_EXTENSION_RESPONSE_TIME
            )
            if no_response_from_jupyterlab_extension:
                _STATUS.extension_enabled = False
                break

        kernel.do_one_iteration()

    # Increment execution count to prevent collision error.
    ipython.execution_count += 1

    # Revert the kernel shell handler to the original execute_request behavior.
    kernel.shell_handlers["execute_request"] = original_handler

    # Flush before replaying so messages show up in current cell and not captured cells.
    sys.stdout.flush()
    sys.stderr.flush()
    for stream, ident, parent in captured_events:
        # Using kernel.set_parent is the key to getting the output of the replayed events
        # to show up in the cells that were captured instead of the current cell.
        kernel.set_parent(ident, parent)
        kernel.execute_request(stream, ident, parent)


def display_widget(cube: str, session: str, name: Optional[str]):
    """Display the output that will lead the atoti JupyterLab extension to show a widget."""
    # pylint: disable=line-too-long
    # This is what happens when our JupyterLab extension is enabled:
    #
    #                                           +---------+                                            +-----------+
    #                                           | Kernel  |                                            | Extension |
    #                                           +---------+                                            +-----------+
    #                                                |                                                       |
    #                                                | [output]: display widget mime type data               |
    #                                                |------------------------------------------------------>|
    #         -------------------------------------\ |                                                       |
    #         | Capturing execute_request events   |-|                                                       |
    #         | -> execution of next cells blocked | |                                                       |
    #         |------------------------------------| |                                                       | ------------------\
    #                                                |                                                       |-| Mounting widget |
    #                                                |                                                       | |-----------------|
    #                                                |                                                       |
    #                                                |              [comm]: open and ask for session details |
    #                                                |<------------------------------------------------------|
    #                                                |                                                       |
    #                                                | [comm]: send session details (url, token, etc.)       |
    #                                                |------------------------------------------------------>|
    #                                                |                                                       | ---------------------------------------\
    #                                                |                                                       |-| Adding corresponding server and      |
    #                                                |                                                       | | loading widget (executing MDX query) |
    #                                                |                                                       | |--------------------------------------|
    #                                                |                            [comm]: tell widget loaded |
    #                                                |<------------------------------------------------------|
    #                                                |                                                       |
    #                                                | [comm]: close                                         |
    #                                                |------------------------------------------------------>|
    # ---------------------------------------------\ |                                                       |
    # | Replaying captured execute_request events  |-|                                                       |
    # | -> executing next cells (kernel unblocked) | |                                                       |
    # |--------------------------------------------| |                                                       | (made with https://textart.io/sequence)
    #
    #
    # If the kernel doesn't receive the "[comm]: open and ask for session details" in the next {{_MAX_JUPYTERLAB_EXTENSION_RESPONSE_TIME}} seconds
    # following the beginning of the "execute_request" events capture, it will consider that the extension is not enabled:
    # - it will immediately stop the capture and replay the captured events to unblock the kernel.
    # - it won't capture anything in the following "display_widget" calls.
    # pylint: enable=line-too-long
    if run_from_ipython():
        from IPython.display import publish_display_data
        from IPython import get_ipython

        ipython = get_ipython()
        publish_display_data(
            {
                _WIDGET_MIME_TYPE: {"cube": cube, "name": name, "session": session},
                "text/plain": "Install and enable the atoti JupyterLab extension to see this widget.",
            }
        )
        if (not _STATUS.captured_once) or _STATUS.extension_enabled:
            _STATUS.captured_once = True
            _capture_until_widget_loaded(ipython)
    else:
        print(
            "atoti widgets can only be shown in JupyterLab with the atoti JupyterLab extension enabled."
        )
