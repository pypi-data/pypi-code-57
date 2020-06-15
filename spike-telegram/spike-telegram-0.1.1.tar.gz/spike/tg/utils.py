# Copyright (C) 2020 Esteban López Rodríguez <gnu_stallman@protonmail.ch>
#
# This file is part of Spike.
#
# Spike is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Spike is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from spike.common.textmessage import TextMessage
from spike.common.message import Message
from spike.tg.telegram import Telegram
from spike.config.config import Config
if Config.get_instance().get_emoji_convert_codes():
    import emoji

def create_message_object(msg_dict, users_dict):
    # Telegram instance
    tg = Telegram().get_instance()
    # Message ID fetch
    msg_id = msg_dict["id"]
    # Is message a reply?
    reply_to = msg_dict["reply_to_message_id"]
    # Message epoch fetch
    epoch = msg_dict["date"]
    # Message sender cached fetch
    if msg_dict["sender_user_id"] in list(users_dict.keys()):
        sender = users_dict[msg_dict["sender_user_id"]]
    else:  # Searches the username and caches it in self.user
        result = tg.get_user(msg_dict["sender_user_id"])
        result.wait()
        if result.error:
            sender = "<?>"
        else:
            users_dict[msg_dict["sender_user_id"]] = result.update["first_name"]
            sender = result.update["first_name"]

    # Message classification
    if msg_dict["content"]["@type"] == "messageText":
        if Config.get_instance().get_emoji_convert_codes():
            text = emoji.demojize(msg_dict["content"]["text"]["text"])
        else:
            text = msg_dict["content"]["text"]["text"]
        msg = TextMessage(msg_id, sender, epoch, text, reply_to)
    else:
        msg = Message(msg_id, sender, epoch, reply_to)

    return msg
