from requests import post
from time import time

from .settings import Settings
from .errors import TelemetryUnavailable
from .log import Log




class Telemetry():
    

    def __init__(self, sender: str):
        self.log = Log(f"Telemetry: {sender}", "Telemetry", "log")

    def low_priority(self,  message: str, urlTitle: str=None, url: str=None):
        self.__send_message(-1, message, urlTitle=urlTitle, url=url)

    def normal_priority(self,  message: str, urlTitle: str=None, url: str=None):
        self.__send_message(0, message, urlTitle=urlTitle, url=url)

    def high_priority(self,  message: str, urlTitle: str=None, url: str=None):
        self.__send_message(1, message, urlTitle=urlTitle, url=url)

    def critical_priority(self,  message: str, urlTitle: str=None, url: str=None):
        self.__send_message(2, message, urlTitle=urlTitle, url=url)
        


    def __send_message(self, priority: int, message: str, urlTitle: str=None, url: str=None):
        settings = Settings()
        
        if not settings.has_key("tokens.pushover.user"):
            raise TelemetryUnavailable("The pushover settings have not been set in the setting file. These must be set first before attempting to use Telemetry.")

        self.log.log(f"Telemetry Sent:\n| Message | {message} |\n|Url|[{urlTitle}]({url})|")
        
        body = {
            "token": settings.get_setting("tokens.pushover.token"),
            "user": settings.get_setting("tokens.pushover.user"),
            "message": message,
            "timestamp": time(),
            "priority": priority
        }

        if urlTitle is not None and url is not None:
            body["url_title"] = urlTitle
            body["url"] = url
        elif url is not None: 
            body["url"] = url

        response = post(
            "https://api.pushover.net/1/messages.json",
            body=body
        )

        self.log.log(f"Telemetry received the response from pushover:\n| Status Code | {response.status_code} |\n| Response Text | {response.text} |")
