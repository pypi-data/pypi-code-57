from .. import Module, Log, Settings
from .. import ConfigFileNotFound, MissingSetting, HTTPDriverException
from .. import CommandMessage
from ..httpclient import HTTPClient, WebResponse

from datetime import datetime

log = Log("CORE:Uptime", verbose="log")

class Uptime(Module):

    def __init__(self, channel):
        Module.__init__(self, "Uptime")
        self.channel = channel
    
    def on_command(self, data: CommandMessage):
        if "uptime" == data.KEYWORD:
            try:
                settings = Settings()
                if settings.has_key("database.user") and settings.has_key("database.pass") and settings.has_key("database.name"):
                    client = HTTPClient("Uptime Command Handler", use_model=True)
                elif settings.has_key("twitch.oauth"):
                    client = HTTPClient("Uptime Command Handler", twitch_oauth=settings.get_setting("twitch.oauth"))
                else:
                    raise MissingSetting("You must provide either 'twitch.oauth' or 'database.user' and 'database.pass' and 'database.name' in your settings file.")
            except ConfigFileNotFound:
                raise HTTPDriverException("To use the 'Uptime' command, you must use a config file and specify a value for:\n - twitch.oauth or\n - database.user and database.pass with the correct tokens table")
            streamURL = f"https://api.twitch.tv/helix/streams?user_login={data.channel}"
            response = client.GetFromTwitch(streamURL)
            message = ""
            if len(response.json["data"]) > 0:
                delta = datetime.utcnow() - datetime.strptime(response.json["data"][0]["started_at"],"%Y-%m-%dT%H:%M:%SZ")
                seconds = int(round(delta.total_seconds()))
                minutes, seconds = divmod(seconds, 60)
                hours, minutes = divmod(minutes, 60)
                message = "{:d} hours, {:02d} minutes".format(hours, minutes)
            else:
                message = f"{data.channel} isn't live right now {data.display_name}, please try again later when the stream is live."
            
            self.channel.send(message)


def setup(channel):
    if channel.channel_name.lower() == "lowkotv":
        return
    try:
        settings = Settings()
        try:
            if settings.get_setting("commands.uptime") == True:
                channel.load_module(Uptime(channel))
                log.log(f"[{channel.channel_name}]: Loaded Module Uptime")
        except (KeyError, MissingSetting):
            channel.load_module(Uptime(channel))
            log.log(f"[{channel.channel_name}]: Loaded Module Uptime")
    except ConfigFileNotFound:
        channel.load_module(Uptime(channel))
        log.log(f"[{channel.channel_name}]: Loaded Module Uptime")

def teardown(channel):
    log.log(f"[{channel.channel_name}]: Removed Module Uptime")