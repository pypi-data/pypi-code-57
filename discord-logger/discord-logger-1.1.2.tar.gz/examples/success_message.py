from discord_logger import DiscordLogger

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
    title="Celery Task Manager",
    description="Successfully completed training job for model v1.3.3!",
    level="success",
    metadata={
        "Metrics": {
            "Accuracy": 78.9,
            "Inference time": "0.8 sec",
            "Model size": "32 MB",
        },
        "Deployment status": "progress",
    },
)
response = logger.send()
