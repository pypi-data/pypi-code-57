import logging
import telegram
from typing import *
from royalnet.serf.telegram.telegramserf import TelegramSerf, escape
from royalnet.commands import *


log = logging.getLogger(__name__)


class TelegramMessageEvent(Event):
    name = "telegram_message"

    async def run(self, chat_id, text, **kwargs) -> dict:
        if not self.interface.name == "telegram":
            raise UnsupportedError()

        # noinspection PyTypeChecker
        serf: TelegramSerf = self.interface.serf

        log.debug("Forwarding message from Herald to Telegram.")
        await serf.api_call(serf.client.send_message,
                            chat_id=chat_id,
                            text=escape(text),
                            parse_mode="HTML",
                            disable_web_page_preview=True)

        return {}
