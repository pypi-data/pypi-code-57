import traceback

from discord_logger import DiscordLogger


def get_traceback(e):
    tb = (
        "Traceback (most recent call last):\n"
        + "".join(traceback.format_list(traceback.extract_tb(e.__traceback__)))
        + type(e).__name__
        + ": "
        + str(e)
    )
    return tb


webhook_url = "your discord webhook url"
webhook_url = "https://discordapp.com/api/webhooks/701499939292971048/HDoCQfjLhXv3dEpq1_E9ZVasz8D_xl48fTg1DAmpX0dxD0JufFzvF0P3gso5s-AQOqRb"
options = {
    "application_name": "My Server",
    "service_name": "Backend API",
    "service_icon_url": "https://cdn1.iconfinder.com/data/icons/basic-ui-elements-coloricon/21/36-512.png",
    "service_environment": "Production",
    "default_level": "info",
}

err = KeyError("`email` field cannot be None")

logger = DiscordLogger(webhook_url=webhook_url, **options)

logger.construct(
    title="Runtime Exception",
    description=err.__str__(),
    error=get_traceback(err),
    metadata={"email": None, "module": "auth", "method": "POST"},
)
response = logger.send()
