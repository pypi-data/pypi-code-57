from typing import *
import datetime
import re
import dateparser
import typing
import random
import enum
import asyncio as aio
from telegram import Bot as PTBBot
from telegram import Message as PTBMessage
from telegram import InlineKeyboardMarkup as InKM
from telegram import InlineKeyboardButton as InKB
from telegram.error import TelegramError
import royalnet.commands as rc
from royalnet.serf.telegram import TelegramSerf as TelegramBot
from royalnet.serf.telegram import escape as telegram_escape
from royalnet.utils import asyncify, sleep_until, sentry_async_wrap
from royalnet.backpack.tables import User

from ..tables import MMEvent, MMResponse, FiorygiTransaction
from ..types import MMChoice, MMInterfaceDataTelegram


class Interrupts(enum.Enum):
    TIME_RAN_OUT = enum.auto()
    MANUAL_START = enum.auto()
    MANUAL_DELETE = enum.auto()


class MatchmakingCommand(rc.Command):
    name: str = "matchmaking"

    description: str = "Cerca persone per una partita a qualcosa!"

    syntax: str = "[ {ora} ] {nome}\n[descrizione]"

    aliases = ["mm", "lfg"]

    tables = {MMEvent, MMResponse}

    def __init__(self, interface: rc.CommandInterface):
        super().__init__(interface)
        # Find all relevant MMEvents and run them
        session = self.alchemy.Session()
        mmevents = (
            session
            .query(self.alchemy.get(MMEvent))
            .filter(self.alchemy.get(MMEvent).interface == self.interface.name,
                    self.alchemy.get(MMEvent).datetime > datetime.datetime.now(),
                    self.alchemy.get(MMEvent).interrupted == False)
            .all()
        )
        self.tasks_created = {}
        self.queue: Dict[int, aio.queues.Queue] = {}
        for mmevent in mmevents:
            task = self.interface.loop.create_task(self._run_mmevent(mmevent.mmid))
            self.tasks_created[mmevent.mmid] = task

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        # Create a new MMEvent and run it
        if self.interface.name != "telegram":
            raise rc.UnsupportedError(f"{self.interface.prefix}matchmaking funziona solo su Telegram. Per ora.")
        author = await data.get_author(error_if_none=True)

        try:
            timestring, title, description = args.match(r"\[\s*([^]]+)\s*]\s*([^\n]+)\s*\n?\s*(.+)?\s*", re.DOTALL)
        except rc.InvalidInputError:
            timestring, title, description = args.match(r"\s*(.+?)\s*\n\s*([^\n]+)\s*\n?\s*(.+)?\s*", re.DOTALL)
        try:
            dt: typing.Optional[datetime.datetime] = dateparser.parse(timestring, settings={
                "PREFER_DATES_FROM": "future"
            })
        except OverflowError:
            dt = None
        if dt is None:
            raise rc.InvalidInputError("La data che hai specificato non è valida.")
        if dt <= datetime.datetime.now():
            raise rc.InvalidInputError("La data che hai specificato è nel passato.")
        if dt - datetime.datetime.now() >= datetime.timedelta(days=366):
            raise rc.InvalidInputError("Hai specificato una data tra più di un anno!\n"
                                       "Se volevi scrivere un'orario, ricordati che le ore sono separate da due punti"
                                       " (:) e non da punto semplice!")
        mmevent: MMEvent = self.alchemy.get(MMEvent)(creator=author,
                                                     datetime=dt,
                                                     title=title,
                                                     description=description,
                                                     interface=self.interface.name)
        data.session.add(mmevent)
        await data.session_commit()
        self.loop.create_task(self._run_mmevent(mmevent.mmid))
        await data.reply(f"🚩 Matchmaking creato!")

    _mmchoice_values = {
        MMChoice.YES: 4,
        MMChoice.LATE_SHORT: 3,
        MMChoice.LATE_MEDIUM: 2,
        MMChoice.LATE_LONG: 1,
        MMChoice.MAYBE: 0,
        MMChoice.NO: -1
    }

    def _gen_mm_message(self, mmevent: MMEvent) -> str:
        text = f"🚩 [{mmevent.datetime.strftime('%Y-%m-%d %H:%M')}] [b]{mmevent.title}[/b]\n"
        if mmevent.description:
            text += f"{mmevent.description}\n"
        text += "\n"
        for response in sorted(mmevent.responses, key=lambda r: -self._mmchoice_values[r.choice]):
            response: MMResponse

            if response.choice == MMChoice.LATE_SHORT:
                td = mmevent.datetime + datetime.timedelta(minutes=10)
                time_text = f" [{td.strftime('%H:%M')}]"
            elif response.choice == MMChoice.LATE_MEDIUM:
                td = mmevent.datetime + datetime.timedelta(minutes=30)
                time_text = f" [{td.strftime('%H:%M')}]"
            elif response.choice == MMChoice.LATE_LONG:
                td = mmevent.datetime + datetime.timedelta(minutes=60)
                time_text = f" [{td.strftime('%H:%M')}+]"
            else:
                time_text = ""

            creator_crown = " 👑" if response.user == mmevent.creator else ""

            text += f"{response.choice.value} {response.user}{time_text}{creator_crown}\n"
        return text

    @staticmethod
    def _gen_telegram_keyboard(mmevent: MMEvent):
        if mmevent.datetime <= datetime.datetime.now():
            return None
        return InKM([
            [
                InKB(f"{MMChoice.YES.value} Ci sarò!",
                     callback_data=f"mm{mmevent.mmid}_YES"),
                InKB(f"{MMChoice.MAYBE.value} Forse...",
                     callback_data=f"mm{mmevent.mmid}_MAYBE"),
                InKB(f"{MMChoice.NO.value} Non mi interessa.",
                     callback_data=f"mm{mmevent.mmid}_NO"),
            ],
            [
                InKB(f"{MMChoice.LATE_SHORT.value} 10 min",
                     callback_data=f"mm{mmevent.mmid}_LATE_SHORT"),
                InKB(f"{MMChoice.LATE_MEDIUM.value} 30 min",
                     callback_data=f"mm{mmevent.mmid}_LATE_MEDIUM"),
                InKB(f"{MMChoice.LATE_LONG.value} 60+ min",
                     callback_data=f"mm{mmevent.mmid}_LATE_LONG"),
            ],
            [
                InKB(f"🗑 Elimina",
                     callback_data=f"mm{mmevent.mmid}_DELETE"),
                InKB(f"🚩 Inizia",
                     callback_data=f"mm{mmevent.mmid}_START"),
            ]
        ])

    async def _update_telegram_mm_message(self, client: PTBBot, mmevent: MMEvent):
        try:
            await self.interface.serf.api_call(client.edit_message_text,
                                               chat_id=self.config["Matchmaking"]["mm_chat_id"],
                                               text=telegram_escape(self._gen_mm_message(mmevent)),
                                               message_id=mmevent.interface_data.message_id,
                                               parse_mode="HTML",
                                               disable_web_page_preview=True,
                                               reply_markup=self._gen_telegram_keyboard(mmevent))
        except TelegramError:
            pass

    def _gen_mm_telegram_callback(self, client: PTBBot, mmid: int, choice: MMChoice):
        async def callback(data: rc.CommandData):
            author = await data.get_author(error_if_none=True)
            mmevent: MMEvent = await asyncify(data.session.query(self.alchemy.get(MMEvent)).get, mmid)
            mmresponse: MMResponse = await asyncify(
                data.session.query(self.alchemy.get(MMResponse)).filter_by(user=author, mmevent=mmevent).one_or_none)
            if mmresponse is None:
                mmresponse = self.alchemy.get(MMResponse)(user=author, mmevent=mmevent, choice=choice)
                data.session.add(mmresponse)
                if random.randrange(14) == 0:
                    await FiorygiTransaction.spawn_fiorygi(data, author, 1, "aver risposto a un matchmaking")
            else:
                mmresponse.choice = choice
            await data.session_commit()
            await self._update_telegram_mm_message(client, mmevent)
            await data.reply(f"{choice.value} Messaggio ricevuto!")
        return callback

    def _gen_mm_telegram_delete(self, client, mmid: int):
        async def callback(data: rc.CommandData):
            author: User = await data.get_author(error_if_none=True)
            mmevent: MMEvent = await asyncify(data.session.query(self.alchemy.get(MMEvent)).get, mmid)
            if author != mmevent.creator and "admin" not in author.roles:
                raise rc.UserError("Non sei il creatore di questo matchmaking!")
            await self.queue[mmid].put(Interrupts.MANUAL_DELETE)
            await data.reply(f"🗑 Evento eliminato!")
        return callback

    def _gen_mm_telegram_start(self, client, mmid: int):
        async def callback(data: rc.CommandData):
            author = await data.get_author(error_if_none=True)
            mmevent: MMEvent = await asyncify(data.session.query(self.alchemy.get(MMEvent)).get, mmid)
            if author != mmevent.creator and "admin" not in author.roles:
                raise rc.UserError("Non sei il creatore di questo matchmaking!")
            await self.queue[mmid].put(Interrupts.MANUAL_START)
            await data.reply(f"🚩 Evento avviato!")
        return callback

    async def _set_event_after(self, mmid: int, dt: datetime.datetime):
        await sleep_until(dt)
        if mmid in self.queue:
            await self.queue[mmid].put(Interrupts.TIME_RAN_OUT)

    def _gen_event_start_message(self, mmevent: MMEvent):
        text = f"🚩 L'evento [b]{mmevent.title}[/b] è iniziato!\n\n"
        for response in sorted(mmevent.responses, key=lambda r: -self._mmchoice_values[r.choice]):
            response: MMResponse
            text += f"{response.choice.value} {response.user}\n"
        return text

    @staticmethod
    def _gen_unauth_message(user: User):
        return f"⚠️ Non sono autorizzato a mandare messaggi a [b]{user.username}[/b]!\n" \
               f"{user.telegram[0].mention()}, apri una chat privata con me e mandami un messaggio!"

    @sentry_async_wrap()
    async def _run_mmevent(self, mmid: int):
        """Run a MMEvent."""
        # Create the event in the dict
        self.queue[mmid] = aio.Queue()
        # Open a new Alchemy Session
        session = self.alchemy.Session()
        # Find the MMEvent with the current session
        mmevent: MMEvent = await asyncify(session.query(self.alchemy.get(MMEvent)).get, mmid)
        if mmevent is None:
            raise ValueError("Invalid mmid.")
        # Ensure the MMEvent hasn't already started
        if mmevent.datetime <= datetime.datetime.now():
            raise ValueError("MMEvent has already started.")
        # Ensure the MMEvent interface matches the current one
        if mmevent.interface != self.interface.name:
            raise ValueError("Invalid interface.")
        # If the matchmaking message hasn't been sent yet, do so now
        if mmevent.interface_data is None:
            if self.interface.name == "telegram":
                bot: TelegramBot = self.interface.serf
                client: PTBBot = bot.client
                # Send the keyboard
                message: PTBMessage = await self.interface.serf.api_call(
                    client.send_message,
                    chat_id=self.config["Matchmaking"]["mm_chat_id"],
                    text=telegram_escape(
                        self._gen_mm_message(mmevent)),
                    parse_mode="HTML",
                    disable_webpage_preview=True,
                    reply_markup=self._gen_telegram_keyboard(mmevent)
                )
                # Store message data in the interface data object
                mmevent.interface_data = MMInterfaceDataTelegram(chat_id=self.config["Matchmaking"]["mm_chat_id"],
                                                                 message_id=message.message_id)
                await asyncify(session.commit)
            else:
                raise rc.UnsupportedError()
        # Register handlers for the keyboard events
        if self.interface.name == "telegram":
            bot: TelegramBot = self.interface.serf
            client: PTBBot = bot.client
            bot.register_keyboard_key(f"mm{mmevent.mmid}_YES", key=rc.KeyboardKey(
                interface=self.interface,
                short=f"{MMChoice.YES.value}",
                text="Ci sarò!",
                callback=self._gen_mm_telegram_callback(client, mmid, MMChoice.YES)
            ))
            bot.register_keyboard_key(f"mm{mmevent.mmid}_LATE_SHORT", key=rc.KeyboardKey(
                interface=self.interface,
                short=f"{MMChoice.LATE_SHORT.value}",
                text="10 min",
                callback=self._gen_mm_telegram_callback(client, mmid, MMChoice.LATE_SHORT)
            ))
            bot.register_keyboard_key(f"mm{mmevent.mmid}_LATE_MEDIUM", key=rc.KeyboardKey(
                interface=self.interface,
                short=f"{MMChoice.LATE_MEDIUM.value}",
                text="30 min",
                callback=self._gen_mm_telegram_callback(client, mmid, MMChoice.LATE_MEDIUM)
            ))
            bot.register_keyboard_key(f"mm{mmevent.mmid}_LATE_LONG", key=rc.KeyboardKey(
                interface=self.interface,
                short=f"{MMChoice.LATE_LONG.value}",
                text="60 min",
                callback=self._gen_mm_telegram_callback(client, mmid, MMChoice.LATE_LONG)
            ))
            bot.register_keyboard_key(f"mm{mmevent.mmid}_MAYBE", key=rc.KeyboardKey(
                interface=self.interface,
                short=f"{MMChoice.MAYBE.value}",
                text="Forse...",
                callback=self._gen_mm_telegram_callback(client, mmid, MMChoice.MAYBE)
            ))
            bot.register_keyboard_key(f"mm{mmevent.mmid}_NO", key=rc.KeyboardKey(
                interface=self.interface,
                short=f"{MMChoice.NO.value}",
                text="Non mi interessa.",
                callback=self._gen_mm_telegram_callback(client, mmid, MMChoice.NO)
            ))
            bot.register_keyboard_key(f"mm{mmevent.mmid}_DELETE", key=rc.KeyboardKey(
                interface=self.interface,
                short=f"🗑",
                text="Elimina",
                callback=self._gen_mm_telegram_delete(client, mmid)
            ))
            bot.register_keyboard_key(f"mm{mmevent.mmid}_START", key=rc.KeyboardKey(
                interface=self.interface,
                short=f"🚩",
                text="Inizia",
                callback=self._gen_mm_telegram_start(client, mmid)
            ))
        else:
            raise rc.UnsupportedError()
        # Sleep until something interrupts
        self.loop.create_task(self._set_event_after(mmid, mmevent.datetime))
        interrupt = await self.queue[mmid].get()
        mmevent.interrupted = True
        await asyncify(session.commit)
        del self.queue[mmid]
        # Notify the positive answers of the event start
        if self.interface.name == "telegram":
            bot: TelegramBot = self.interface.serf
            client: PTBBot = bot.client
            bot.unregister_keyboard_key(f"mm{mmevent.mmid}_YES")
            bot.unregister_keyboard_key(f"mm{mmevent.mmid}_MAYBE")
            bot.unregister_keyboard_key(f"mm{mmevent.mmid}_LATE_SHORT")
            bot.unregister_keyboard_key(f"mm{mmevent.mmid}_LATE_MEDIUM")
            bot.unregister_keyboard_key(f"mm{mmevent.mmid}_LATE_LONG")
            bot.unregister_keyboard_key(f"mm{mmevent.mmid}_NO")
            bot.unregister_keyboard_key(f"mm{mmevent.mmid}_DELETE")
            bot.unregister_keyboard_key(f"mm{mmevent.mmid}_START")

            await self.interface.serf.api_call(client.delete_message,
                                               chat_id=mmevent.interface_data.chat_id,
                                               message_id=mmevent.interface_data.message_id)

            if interrupt == Interrupts.TIME_RAN_OUT or interrupt == Interrupts.MANUAL_START:
                await asyncify(client.send_message,
                               chat_id=self.config["Telegram"]["main_group_id"],
                               text=telegram_escape(self._gen_event_start_message(mmevent)),
                               parse_mode="HTML",
                               disable_webpage_preview=True)

                for response in mmevent.responses:
                    if response.choice == MMChoice.NO:
                        return
                    try:
                        await asyncify(client.send_message,
                                       chat_id=response.user.telegram[0].tg_id,
                                       text=telegram_escape(self._gen_event_start_message(mmevent)),
                                       parse_mode="HTML",
                                       disable_webpage_preview=True)
                    except TelegramError:
                        await self.interface.serf.api_call(
                            client.send_message,
                            chat_id=self.config["Telegram"]["main_group_id"],
                            text=telegram_escape(self._gen_unauth_message(response.user)),
                            parse_mode="HTML",
                            disable_webpage_preview=True
                        )

            elif interrupt == Interrupts.MANUAL_DELETE:
                await self.interface.serf.api_call(
                    client.send_message,
                    chat_id=self.config["Telegram"]["main_group_id"],
                    text=telegram_escape(f"🗑 L'evento [b]{mmevent.title}[/b] è stato annullato."),
                    parse_mode="HTML",
                    disable_webpage_preview=True
                )
        else:
            raise rc.UnsupportedError()
        # The end!
        await asyncify(session.close)
        del self.tasks_created[mmid]
