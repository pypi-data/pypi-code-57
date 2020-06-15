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

from telegram.client import Telegram as T
from spike.config.config import Config

class Telegram:
    __instance = None

    def __init__(self):
        if Telegram.__instance == None:
            config = Config.get_instance()
            Telegram.__instance = T(
                api_id = config.get_tg_api_id(),
                api_hash = config.get_tg_api_hash(),
                phone = config.get_tg_phone(),
                database_encryption_key = config.get_tg_db_encryption_key(),
                files_directory = config.get_tg_files_directory()
            )
            self.__instance.login()

    @staticmethod
    def get_instance():
        if Telegram.__instance == None:
            Telegram()
        return Telegram.__instance


    def _set_status(self, status):
        params = {
            "name": "online",
            "value": status
        }
        self.__instance.call_method("setOption", params=params)


    def set_online(self):
        self._set_status(True)


    def set_offline(self):
        self._set_status(False)
