from typing import *
import logging
import asyncio
import datetime
import royalnet.commands as rc
import royalnet.utils as ru

from ..tables import Cvstats


log = logging.getLogger(__name__)


class CvstatsCommand(rc.Command):
    name: str = "cvstats"

    description: str = ""

    syntax: str = ""

    def __init__(self, interface: rc.CommandInterface):
        super().__init__(interface)
        if self.interface.name == "discord":
            self.loop.create_task(self._updater(1800))

    def _is_ryg_member(self, member: dict):
        for role in member["roles"]:
            if role["id"] == self.interface.config["Cv"]["displayed_role_id"]:
                return True
        return False

    async def _update(self, db_session):
        log.info(f"Gathering Cvstats...")
        while True:
            try:
                response: Dict[str, Any] = await self.interface.call_herald_event("discord", "discord_cv")
            except rc.ConfigurationError:
                await asyncio.sleep(10)
                continue
            else:
                break

        users_total = 0
        members_total = 0
        users_online = 0
        members_online = 0
        users_connected = 0
        members_connected = 0
        users_playing = 0
        members_playing = 0

        # noinspection PyUnboundLocalVariable
        for m in response["guild"]["members"]:
            users_total += 1
            if self._is_ryg_member(m):
                members_total += 1

            if m["status"]["main"] != "offline" and m["status"]["main"] != "idle":
                users_online += 1
                if self._is_ryg_member(m):
                    members_online += 1

                if m["voice"] is not None and not m["voice"]["afk"]:
                    users_connected += 1
                    if self._is_ryg_member(m):
                        members_connected += 1

                for mact in m["activities"]:
                    if mact.get("type") == 0:
                        users_playing += 1
                        if self._is_ryg_member(m):
                            members_playing += 1

        assert users_online >= members_online
        assert users_online >= users_connected
        assert users_online >= users_playing
        assert members_online >= members_connected
        assert members_online >= members_playing

        log.debug(f"Total users: {users_total}")
        log.debug(f"Total members: {members_total}")
        log.debug(f"Online users: {users_online}")
        log.debug(f"Online members: {members_online}")
        log.debug(f"Connected users: {users_connected}")
        log.debug(f"Connected members: {members_connected}")
        log.debug(f"Playing users: {users_playing}")
        log.debug(f"Playing members: {members_playing}")

        CvstatsT = self.alchemy.get(Cvstats)

        cvstats = CvstatsT(
            timestamp=datetime.datetime.now(),
            users_total=users_total,
            members_total=members_total,
            users_online=users_online,
            members_online=members_online,
            users_connected=users_connected,
            members_connected=members_connected,
            users_playing=users_playing,
            members_playing=members_playing
        )

        log.debug("Saving to database...")
        db_session.add(cvstats)
        await ru.asyncify(db_session.commit)
        log.debug("Done!")

    async def _updater(self, period: int):
        log.info(f"Started updater with {period}s period")
        while True:
            log.info(f"Updating...")
            session = self.alchemy.Session()
            await self._update(session)
            session.close()
            log.info(f"Sleeping for {period}s")
            await asyncio.sleep(period)

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        CvstatsT = self.alchemy.get(Cvstats)

        cvstats = data.session.query(CvstatsT).order_by(CvstatsT.timestamp.desc()).first()

        message = [
            f"ℹ️ [b]Statistiche[/b]",
            f"Ultimo aggiornamento: [b]{cvstats.timestamp.strftime('%Y-%m-%d %H:%M')}[/b]",
            f"Utenti totali: [b]{cvstats.users_total}[/b]",
            f"Membri totali: [b]{cvstats.members_total}[/b]",
            f"Utenti online: [b]{cvstats.users_online}[/b]",
            f"Membri online: [b]{cvstats.members_online}[/b]",
            f"Utenti connessi: [b]{cvstats.users_connected}[/b]",
            f"Membri connessi: [b]{cvstats.members_connected}[/b]",
            f"Utenti in gioco: [b]{cvstats.users_playing}[/b]",
            f"Membri in gioco: [b]{cvstats.members_playing}[/b]"
        ]

        await data.reply("\n".join(message))
