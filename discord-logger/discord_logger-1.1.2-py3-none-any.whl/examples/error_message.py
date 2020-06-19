from discord_logger import DiscordLogger

webhook_url = "your discord webhook url"
webhook_url = "https://discordapp.com/api/webhooks/701499939292971048/HDoCQfjLhXv3dEpq1_E9ZVasz8D_xl48fTg1DAmpX0dxD0JufFzvF0P3gso5s-AQOqRb"
options = {
    "application_name": "My Server",
    "service_name": "Backend API",
    "service_icon_url": "https://cdn1.iconfinder.com/data/icons/basic-ui-elements-coloricon/21/36-512.png",
    "service_environment": "Production",
    "default_level": "info",
}

logger = DiscordLogger(webhook_url=webhook_url, **options)

logger.construct(
    title="Health Check",
    description="Issue in establishing DB connections!",
    error="Traceback (most recent call last):\n ValueError: Database connect accepts only string as a parameter!",
    metadata={"module": "DBConnector", "host": 123.332},
)
response = logger.send()
