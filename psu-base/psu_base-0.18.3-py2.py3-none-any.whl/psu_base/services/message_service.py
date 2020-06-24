from psu_base.classes.Log import Log
from psu_base.services import utility_service
from django.contrib import messages
log = Log()


def post_info(msg):
    return post_message(msg, "info")


def post_success(msg):
    return post_message(msg, "success")


def post_warning(msg):
    return post_message(msg, "warning")


def post_error(msg):
    return post_message(msg, "error")


def post_message(msg, msg_type):
    request = utility_service.get_request()
    message = str(msg)

    if request is None:
        log.error(f"Request does not exist. Could not post message: {message}")
    else:
        log_msg = f"[POSTED] {msg}"
        if msg_type == "info":
            messages.info(request, message)
            log.info(log_msg, strip_html=True)
        elif msg_type == "success":
            messages.success(request, message)
            log.info(log_msg, strip_html=True)
        elif msg_type == "warning":
            messages.warning(request, message)
            log.warning(log_msg, strip_html=True)
        elif msg_type == "error":
            messages.error(request, message)
            log.error(log_msg, trace_error=False, strip_html=True)

    return None
