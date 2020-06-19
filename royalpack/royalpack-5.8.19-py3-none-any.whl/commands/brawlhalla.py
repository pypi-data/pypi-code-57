from typing import *

import asyncio
import logging
import aiohttp
from royalnet.commands import *
from royalnet.utils import *
from royalnet.serf.telegram.escape import escape as tg_escape
from sqlalchemy import or_, and_

from ..tables import Steam, Brawlhalla, BrawlhallaDuo
from ..types import BrawlhallaRank, BrawlhallaMetal, BrawlhallaTier

log = logging.getLogger(__name__)


class BrawlhallaCommand(Command):
    name: str = "brawlhalla"

    aliases = ["bh", "bruhalla", "bruhlalla"]

    description: str = "Visualizza le tue statistiche di Dota!"

    syntax: str = ""

    def __init__(self, interface: CommandInterface):
        super().__init__(interface)
        if self.interface.name == "telegram" and self.config["Brawlhalla"]["updater"]:
            self.loop.create_task(self._updater(7200))

    async def _send(self, message):
        client = self.serf.client
        await self.serf.api_call(client.send_message,
                                 chat_id=self.config["Telegram"]["main_group_id"],
                                 text=tg_escape(message),
                                 parse_mode="HTML",
                                 disable_webpage_preview=True)

    @staticmethod
    def _display(bh: Brawlhalla) -> str:
        string = [f"ℹ️ [b]{bh.name}[/b]", ""]

        if bh.rank_1v1:
            string.append("👤 [b]1v1[/b]")
            string.append(f"[b]{bh.rank_1v1}[/b] ({bh.rating_1v1} MMR)")
            string.append("")

        if len(bh.duos) != 0:
            string.append(f"👥 [b]2v2[/b]")

        for duo in bh.duos:
            other = duo.other(bh)
            string.append(f"Con [b]{other.steam.user}[/b]: [b]{duo.rank_2v2}[/b] ({duo.rating_2v2} MMR)")

        if len(bh.duos) != 0:
            string.append("")

        return "\n".join(string)

    async def _notify(self,
                      obj: Union[Brawlhalla, BrawlhallaDuo],
                      attribute_name: str,
                      old_value: Any,
                      new_value: Any):
        if attribute_name == "rank_1v1":
            old_rank: Optional[BrawlhallaRank] = old_value
            new_rank: Optional[BrawlhallaRank] = new_value
            if new_rank > old_rank:
                message = f"📈 [b]{obj.steam.user}[/b] è salito a [b]{new_value}[/b] ({obj.rating_1v1} MMR) in 1v1 su Brawlhalla! Congratulazioni!"
            else:
                message = f"📉 [b]{obj.steam.user}[/b] è sceso a [b]{new_value}[/b] ({obj.rating_1v1} MMR) in 1v1 su Brawlhalla."
            await self._send(message)
        elif attribute_name == "rank_2v2":
            old_rank: Optional[BrawlhallaRank] = old_value
            new_rank: Optional[BrawlhallaRank] = new_value
            if new_rank > old_rank:
                message = f"📈 [b]{obj.one.steam.user}[/b] e [b]{obj.two.steam.user}[/b] sono saliti a [b]{new_value}[/b] ({obj.rating_2v2} MMR) in 2v2 su Brawlhalla! Congratulazioni!"
            else:
                message = f"📉 [b]{obj.one.steam.user}[/b] e [b]{obj.two.steam.user}[/b] sono scesi a [b]{new_value}[/b] ({obj.rating_2v2} MMR) in 2v2 su Brawlhalla."
            await self._send(message)

    @staticmethod
    async def _change(obj: Union[Brawlhalla, BrawlhallaDuo],
                      attribute_name: str,
                      new_value: Any,
                      callback: Callable[[Union[Brawlhalla, BrawlhallaDuo], str, Any, Any], Awaitable[None]]):
        old_value = obj.__getattribute__(attribute_name)
        if old_value != new_value:
            await callback(obj, attribute_name, old_value, new_value)
        obj.__setattr__(attribute_name, new_value)

    async def _update(self, steam: Steam, db_session):
        BrawlhallaT = self.alchemy.get(Brawlhalla)
        DuoT = self.alchemy.get(BrawlhallaDuo)
        log.info(f"Updating: {steam}")
        async with aiohttp.ClientSession() as session:
            bh: Brawlhalla = steam.brawlhalla
            if bh is None:
                log.debug(f"Checking if player has an account...")
                async with session.get(f"https://api.brawlhalla.com/search?steamid={steam.steamid.as_64}&api_key={self.config['Brawlhalla']['api_key']}") as response:
                    if response.status != 200:
                        raise ExternalError(f"Brawlhalla API /search returned {response.status}!")
                    j = await response.json()
                    if j == {} or j == []:
                        log.debug("No account found.")
                        return
                    bh = BrawlhallaT(
                        steam=steam,
                        brawlhalla_id=j["brawlhalla_id"],
                        name=j["name"]
                    )
                    db_session.add(bh)
                    message = f"↔️ Account {bh} connesso a {bh.steam.user}!"
                    await self._send(message)
            async with session.get(f"https://api.brawlhalla.com/player/{bh.brawlhalla_id}/ranked?api_key={self.config['Brawlhalla']['api_key']}") as response:
                if response.status != 200:
                    raise ExternalError(f"Brawlhalla API /ranked returned {response.status}!")
                j = await response.json()
                if j == {} or j == []:
                    log.debug("No ranked info found.")
                else:
                    await self._change(bh, "rating_1v1", j["rating"], self._notify)
                    metal_name, tier_name = j["tier"].split(" ", 1)
                    metal = BrawlhallaMetal[metal_name.upper()]
                    tier = BrawlhallaTier(int(tier_name))
                    rank = BrawlhallaRank(metal=metal, tier=tier)
                    await self._change(bh, "rank_1v1", rank, self._notify)

                    for jduo in j.get("2v2", []):
                        bhduo: Optional[BrawlhallaDuo] = await asyncify(
                            db_session.query(DuoT)
                                .filter(
                                    or_(
                                        and_(
                                            DuoT.id_one == jduo["brawlhalla_id_one"],
                                            DuoT.id_two == jduo["brawlhalla_id_two"]
                                        ),
                                        and_(
                                            DuoT.id_one == jduo["brawlhalla_id_two"],
                                            DuoT.id_two == jduo["brawlhalla_id_one"]
                                        )
                                    )
                                )
                                .one_or_none
                        )
                        if bhduo is None:
                            if bh.brawlhalla_id == jduo["brawlhalla_id_one"]:
                                otherbh: Optional[Brawlhalla] = await asyncify(
                                    db_session.query(BrawlhallaT).get, jduo["brawlhalla_id_two"]
                                )
                            else:
                                otherbh: Optional[Brawlhalla] = await asyncify(
                                    db_session.query(BrawlhallaT).get, jduo["brawlhalla_id_one"]
                                )
                            if otherbh is None:
                                continue
                            bhduo = DuoT(
                                one=bh,
                                two=otherbh,
                            )

                            db_session.add(bhduo)
                        await self._change(bhduo, "rating_2v2", jduo["rating"], self._notify)
                        metal_name, tier_name = jduo["tier"].split(" ", 1)
                        metal = BrawlhallaMetal[metal_name.upper()]
                        tier = BrawlhallaTier(int(tier_name))
                        rank = BrawlhallaRank(metal=metal, tier=tier)
                        await self._change(bhduo, "rank_2v2", rank, self._notify)

            await asyncify(db_session.commit)

    async def _updater(self, period: int):
        log.info(f"Started updater with {period}s period")
        while True:
            log.info(f"Updating...")
            session = self.alchemy.Session()
            log.info("")
            steams = session.query(self.alchemy.get(Steam)).all()
            for steam in steams:
                try:
                    await self._update(steam, session)
                except Exception as e:
                    sentry_exc(e)
                await asyncio.sleep(1)
            await asyncify(session.commit)
            session.close()
            log.info(f"Sleeping for {period}s")
            await asyncio.sleep(period)

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        author = await data.get_author(error_if_none=True)

        found_something = False

        message = ""
        for steam in author.steam:
            await self._update(steam, data.session)
            if steam.brawlhalla is None:
                continue
            found_something = True
            message += self._display(steam.brawlhalla)
            message += "\n"
        if not found_something:
            raise UserError("Nessun account di Brawlhalla trovato.")
        await data.reply(message)
