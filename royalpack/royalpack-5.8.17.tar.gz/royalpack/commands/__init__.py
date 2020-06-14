# Imports go here!
from .ciaoruozi import CiaoruoziCommand
from .color import ColorCommand
from .cv import CvCommand
from .diario import DiarioCommand
from .rage import RageCommand
from .reminder import ReminderCommand
from .ship import ShipCommand
from .smecds import SmecdsCommand
from .videochannel import VideochannelCommand
from .pause import PauseCommand
from .play import PlayCommand
from .queue import QueueCommand
from .skip import SkipCommand
from .summon import SummonCommand
from .youtube import YoutubeCommand
from .soundcloud import SoundcloudCommand
from .emojify import EmojifyCommand
from .leagueoflegends import LeagueoflegendsCommand
from .diarioquote import DiarioquoteCommand
from .peertubeupdates import PeertubeUpdatesCommand
from .googlevideo import GooglevideoCommand
from .yahoovideo import YahoovideoCommand
from .userinfo import UserinfoCommand
from .spell import SpellCommand
from .ahnonlosoio import AhnonlosoioCommand
from .eat import EatCommand
from .pmots import PmotsCommand
from .peertube import PeertubeCommand
from .funkwhale import FunkwhaleCommand
from .eval import EvalCommand
from .exec import ExecCommand
from .trivia import TriviaCommand
from .steampowered import SteampoweredCommand
from .steammatch import SteammatchCommand
from .dota import DotaCommand
from .magickfiorygi import MagickfiorygiCommand
from .brawlhalla import BrawlhallaCommand
from .diarioshuffle import DiarioshuffleCommand
from .funkwhaleplaylist import FunkwhaleplaylistCommand
from .voicestatus import VoicestatusCommand
from .playmode import PlaymodeCommand
from .lazyplay import LazyplayCommand
from .lazyfunkwhale import LazyfunkwhaleCommand
from .lazyfunkwhaleplaylist import LazyfunkwhaleplaylistCommand
from .lazygooglevideo import LazygooglevideoCommand
from .lazypeertube import LazypeertubeCommand
from .lazysoundcloud import LazysoundcloudCommand
from .lazyyahoovideo import LazyyahoovideoCommand
from .lazyyoutube import LazyyoutubeCommand
from .funkwhalealbum import FunkwhalealbumCommand
from .lazyfunkwhalealbum import LazyfunkwhalealbumCommand
from .matchmaking import MatchmakingCommand
from .cvstats import CvstatsCommand
from .elevatormusic import ElevatormusicCommand
from .royalpack import RoyalpackCommand
from .givefiorygi import GivefiorygiCommand
from .help import HelpCommand
from .pug import PugCommand
from .magicktreasure import MagicktreasureCommand
from .treasure import TreasureCommand
from .givetreasure import GivetreasureCommand
from .cat import CatCommand

# Enter the commands of your Pack here!
available_commands = [
    CiaoruoziCommand,
    ColorCommand,
    CvCommand,
    DiarioCommand,
    RageCommand,
    ReminderCommand,
    ShipCommand,
    SmecdsCommand,
    VideochannelCommand,
    PauseCommand,
    PlayCommand,
    QueueCommand,
    SkipCommand,
    SummonCommand,
    YoutubeCommand,
    SoundcloudCommand,
    EmojifyCommand,
    LeagueoflegendsCommand,
    DiarioquoteCommand,
    PeertubeUpdatesCommand,
    GooglevideoCommand,
    YahoovideoCommand,
    UserinfoCommand,
    SpellCommand,
    AhnonlosoioCommand,
    EatCommand,
    PmotsCommand,
    PeertubeCommand,
    EvalCommand,
    ExecCommand,
    FunkwhaleCommand,
    TriviaCommand,
    SteampoweredCommand,
    SteammatchCommand,
    DotaCommand,
    MagickfiorygiCommand,
    BrawlhallaCommand,
    DiarioshuffleCommand,
    FunkwhaleplaylistCommand,
    VoicestatusCommand,
    PlaymodeCommand,
    LazyplayCommand,
    LazyfunkwhaleCommand,
    LazyfunkwhaleplaylistCommand,
    LazygooglevideoCommand,
    LazypeertubeCommand,
    LazysoundcloudCommand,
    LazyyahoovideoCommand,
    LazyyoutubeCommand,
    FunkwhalealbumCommand,
    LazyfunkwhalealbumCommand,
    MatchmakingCommand,
    CvstatsCommand,
    ElevatormusicCommand,
    RoyalpackCommand,
    GivefiorygiCommand,
    HelpCommand,
    PugCommand,
    MagicktreasureCommand,
    TreasureCommand,
    GivetreasureCommand,
    CatCommand,
]

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_commands]
