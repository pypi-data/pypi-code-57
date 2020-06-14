# Imports go here!
from .discord_cv import DiscordCvEvent
from .discord_summon import DiscordSummonEvent
from .discord_play import DiscordPlayEvent
from .discord_skip import DiscordSkipEvent
from .discord_queue import DiscordQueueEvent
from .discord_pause import DiscordPauseEvent
from .discord_playable import DiscordPlaymodeEvent
from .discord_lazy_play import DiscordLazyPlayEvent
from .telegram_message import TelegramMessageEvent

# Enter the commands of your Pack here!
available_events = [
    DiscordCvEvent,
    DiscordSummonEvent,
    DiscordPlayEvent,
    DiscordSkipEvent,
    DiscordQueueEvent,
    DiscordPauseEvent,
    DiscordPlaymodeEvent,
    DiscordLazyPlayEvent,
    TelegramMessageEvent,
]

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_events]
