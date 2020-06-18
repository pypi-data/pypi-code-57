from slack_logger import SlackLogger

token = "your slack app token"
token = "xoxb-238162737221-950522891462-xtHa5UeQfw73LyXKp25ug4Ba"
options = {
    "service_name": "Backend API",
    "service_environment": "Production",
    "default_level": "info",
}

logger = SlackLogger(token=token, **options)

channel = "#test"
response = logger.send(
    channel=channel,
    title="Health Check",
    description="Issue in establishing DB connections!",
    error="Traceback (most recent call last):\n ValueError: Database connect accepts only string as a parameter!",
    metadata={"module": "DBConnector", "host": 123.332},
)
