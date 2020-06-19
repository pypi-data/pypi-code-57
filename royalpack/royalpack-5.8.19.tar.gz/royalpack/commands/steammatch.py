from typing import *
import steam.webapi
import requests.exceptions
import royalnet.commands as rc
import royalnet.utils as ru
import royalnet.backpack.tables as rbt

from ..tables import Steam


class SteamGame:
    def __init__(self,
                 appid=None,
                 name=None,
                 playtime_forever=None,
                 img_icon_url=None,
                 img_logo_url=None,
                 has_community_visible_stats=None,
                 playtime_windows_forever=None,
                 playtime_mac_forever=None,
                 playtime_linux_forever=None,
                 playtime_2weeks=None):
        self.appid = appid
        self.name = name
        self.playtime_forever = playtime_forever
        self.img_icon_url = img_icon_url
        self.img_logo_url = img_logo_url
        self.has_community_visible_stats = has_community_visible_stats
        self.playtime_windows_forever = playtime_windows_forever
        self.playtime_mac_forever = playtime_mac_forever
        self.playtime_linux_forever = playtime_linux_forever
        self.playtime_2weeks = playtime_2weeks

    def __hash__(self):
        return self.appid

    def __eq__(self, other):
        if isinstance(other, SteamGame):
            return self.appid == other.appid
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.appid} ({self.name})>"


class SteammatchCommand(rc.Command):
    name: str = "steammatch"

    description: str = "Vedi quali giochi hai in comune con uno o più membri!"

    syntax: str = "{royalnet_username}+"

    def __init__(self, interface: rc.CommandInterface):
        super().__init__(interface)
        if "Steam" not in self.config or "web_api_key" not in self.config["Steam"]:
            raise rc.ConfigurationError("[c]Steam.web_api_key[/c] config option is missing!")
        self._api = steam.webapi.WebAPI(self.config["Steam"]["web_api_key"])

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        users = []

        author = await data.get_author(error_if_none=True)
        users.append(author)

        for arg in args:
            user = await rbt.User.find(self.alchemy, data.session, arg)
            users.append(user)

        if len(users) < 2:
            raise rc.InvalidInputError("Devi specificare almeno un altro utente!")

        shared_games: Optional[set] = None
        for user in users:
            user_games = set()
            if len(user.steam) == 0:
                raise rc.UserError(f"{user} non ha un account Steam registrato!")
            for steam_account in user.steam:
                steam_account: Steam
                try:
                    response = await ru.asyncify(self._api.IPlayerService.GetOwnedGames,
                                                 steamid=steam_account._steamid,
                                                 include_appinfo=True,
                                                 include_played_free_games=True,
                                                 include_free_sub=True,
                                                 appids_filter=0)
                except requests.exceptions.HTTPError:
                    raise rc.ExternalError(f"L'account Steam di {user} è privato!")
                games = response["response"]["games"]
                for game in games:
                    user_games.add(SteamGame(**game))
            if shared_games is None:
                shared_games = user_games
            else:
                shared_games = shared_games.intersection(user_games)

        message_rows = [f"🎮 Giochi in comune tra {ru.andformat([str(user) for user in users], final=' e ')}:"]
        for game in sorted(list(shared_games), key=lambda g: g.name):
            message_rows.append(f"- {game}")

        message = "\n".join(message_rows)
        await data.reply(message)
