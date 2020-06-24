#
# The unexpected error function required a new service because its use of
# auth_service resulted in circular imports when it was added to message_service
#

from psu_base.classes.Log import Log
from psu_base.services import utility_service
from inspect import getframeinfo, stack
from psu_base.models.error import Error
from psu_base.services import auth_service, message_service
import os

log = Log()


def unexpected_error(error_display=None, error_system=None):
    """
    Logs the error in the db, the log file, and posts an error on-screen
    This service cannot use auth_service (circular import), so user must be provided if you want it logged
    """

    # Gather data
    src = get_caller_data()
    request = utility_service.get_request()
    path = request.path if request else '?'
    method = request.method if request else None
    parameters = utility_service.get_parameters()
    if not parameters:
        parameters = None  # To avoid "{}"
    auth = auth_service.get_auth_object()

    # Gather user authentication data
    user_log_msg = f"User          : {auth.sso_user}"
    if auth.is_impersonating():
        user_log_msg += f"\n\tImpersonating : {auth.impersonated_user}"
    if auth.is_proxying():
        user_log_msg += f"\n\tProxying      : {auth.proxied_user}"

    # Log error in log file
    log.error(
        f"""\n
\t*** UNEXPECTED ERROR ***
\tSystem Error:   {error_system}
\tFriendly Error: {error_display}
\t{user_log_msg}
\tRequest Path:   {f"[{method}] " if method else ''}{path}
\tParameters:     {parameters}
\tRaised From:    {src}
        """,
        trace_error=False
    )

    # Log error in database
    try:
        ee = Error()
        ee.app_code = utility_service.get_app_code()
        ee.path = path
        ee.parameters = parameters
        ee.code_detail = src
        ee.sso_user = auth.sso_user.username
        ee.impersonated_user = auth.impersonated_user.username
        ee.proxied_user = auth.proxied_user.username
        ee.error_friendly = error_display
        ee.error_system = error_system
        ee.save()
    except Exception as ee:
        log.warning(f"Unexpected error was not saved in database: {str(ee)}")

    # Post friendly error to the screen
    if error_display:
        message_service.post_error(error_display)


def get_caller_data():
    """Return the calling code as (file-name, line-number, function-name)"""

    # Ignore this function, and the message_service.<function> that called it
    depth = 2

    # Get the info about the function that generated the message
    caller = getframeinfo(stack()[depth][0])

    # In case of nested functions within this class, may need to look deeper
    while caller.filename.endswith('message_service.py'):
        depth += 1
        caller = getframeinfo(stack()[depth][0])

    return f"{os.path.basename(caller.filename)}.{caller.function}() at line {caller.lineno}"
