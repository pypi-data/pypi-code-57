import traceback

from slack_logger import SlackLogger


def get_traceback(e):
    tb = (
        "Traceback (most recent call last):\n"
        + "".join(traceback.format_list(traceback.extract_tb(e.__traceback__)))
        + type(e).__name__
        + ": "
        + str(e)
    )
    return tb


token = "xoxb-238162737221-950522891462-xtHa5UeQfw73LyXKp25ug4Ba"
options = {
    "service_name": "Backend API",
    "service_environment": "Production",
    "default_level": "info",
}

err = KeyError("'email' field cannot be None")

logger = SlackLogger(token=token, **options)

channel = "#test"
response = logger.send(
    channel=channel,
    title="Runtime Exception",
    description=err.__str__(),
    error=get_traceback(err),
    metadata={"email": None, "module": "auth", "method": "POST"},
)
