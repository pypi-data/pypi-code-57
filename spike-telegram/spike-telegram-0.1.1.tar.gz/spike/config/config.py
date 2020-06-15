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

from configparser import ConfigParser
from os import environ, makedirs
from os.path import dirname, exists

class Config:
    __instance = None

    FILES_DIRECTORY = "{}/.local/share/spike-telegram".format(environ["HOME"])
    CONFIG_FILE = "{}/.config/spikerc".format(environ["HOME"])

    DEF_API_ID = "XXXXXXX"
    DEF_API_HASH = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    DEF_PHONE = "+YYXXXXXXXXX"
    DEF_DB_ENCRYPTION_KEY = ""
    DEF_NOTIFICATIONS = True
    DEF_SOUND = True
    DEF_ONLINE = True
    DEF_MARK_SEEN_MSG = True
    try:
        import emoji  # Check for the presence of emoji library
        DEF_EMOJI_CODES = True
    except ModuleNotFoundError:
        DEF_EMOJI_CODES = False

    def __init__(self):
        if Config.__instance == None:
            Config.__instance = self
            self.config_parser = ConfigParser()

            if exists(Config.CONFIG_FILE):
                self.config_parser.read(Config.CONFIG_FILE)
            else:
                self._write_default_config()
                print("Writing default config file to", Config.CONFIG_FILE)
                print("Please edit Telegram credentials and relaunch Spike")
                exit(0)


    @staticmethod
    def get_instance():
        if Config.__instance == None:
            Config()
        return Config.__instance


    def _write_config(self):
        if not exists(dirname(Config.CONFIG_FILE)):
            makedirs(dirname(Config.CONFIG_FILE))

        with open(Config.CONFIG_FILE, "w") as f:
            self.config_parser.write(f)


    def _write_default_config(self):
        self.config_parser["Telegram"] = {
            "api_id": Config.DEF_API_ID,
            "api_hash": Config.DEF_API_HASH,
            "phone": Config.DEF_PHONE,
            "db_encryption_key": Config.DEF_DB_ENCRYPTION_KEY,
        }
        self.config_parser["settings"] = {
            "notifications": Config.DEF_NOTIFICATIONS,
            "notifications_sound": Config.DEF_SOUND
        }
        self.config_parser["privacy"] = {
            "online_status": Config.DEF_ONLINE,
            "mark_as_seen": Config.DEF_MARK_SEEN_MSG
        }
        self.config_parser["emojis"] = {
            "convert_to_codes": Config.DEF_EMOJI_CODES
        }
        self._write_config()


    def get_tg_api_id(self):
        return self.config_parser["Telegram"].get("api_id", Config.DEF_API_ID)


    def get_tg_api_hash(self):
        return self.config_parser["Telegram"].get("api_hash", Config.DEF_API_HASH)


    def get_tg_phone(self):
        return self.config_parser["Telegram"].get("phone", Config.DEF_PHONE)


    def get_tg_db_encryption_key(self):
        return self.config_parser["Telegram"].get("db_encryption_key",
                                                  Config.DEF_DB_ENCRYPTION_KEY)

    def get_tg_files_directory(self):
        return Config.FILES_DIRECTORY

    def get_sttg_notifications(self):
        return self.config_parser["settings"].get("notifications",
                Config.DEF_NOTIFICATIONS).lower() == "true"

    def get_sttg_sound(self):
        return self.config_parser["settings"].get("notifications_sound",
                Config.DEF_SOUND).lower() == "true"

    def get_priv_online(self):
        return self.config_parser["privacy"].get("online_status",
                Config.DEF_ONLINE).lower() == "true"

    def get_priv_mark_as_seen(self):
        return self.config_parser["privacy"].get("mark_as_seen",
                Config.DEF_MARK_SEEN_MSG).lower() == "true"

    def get_emoji_convert_codes(self):
        return self.config_parser["emojis"].get("convert_to_codes",
                Config.DEF_EMOJI_CODES).lower() == "true"
