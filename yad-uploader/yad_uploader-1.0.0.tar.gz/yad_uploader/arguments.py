import argparse
import os
from dataclasses import dataclass
from typing import List


@dataclass
class Arguments:
    yad_id: str
    yad_password: str
    yad_token: str
    local_source_dir: str
    yad_dest_dir: str
    tg_token: str
    tg_chats_id: List[str]


def parse_args() -> Arguments:
    parser = argparse.ArgumentParser(
        description="Бэкап в Я.Диск",
    )
    parser.add_argument("--yad_id", "-i", type=str,
                        help="ID приложения", required=True)
    parser.add_argument("--yad_password", "-p", type=str,
                        help="Пароль приложения", required=True)
    parser.add_argument("--yad_token", "-t", type=str,
                        help="Oauth token", required=False)
    parser.add_argument("--source", "-s", type=existed_path,
                        help="Что копировать", required=True)
    parser.add_argument("--dest", "-d", type=str,
                        help="Папка на Я.Диск", required=True)
    parser.add_argument("--tg_token", "-g", type=str, required=False,
                        help="Telegram token")
    parser.add_argument("--tg_chat_id", "-a", dest='tg_chat_ids', type=str, action='append',
                        help="Telegram chat id")
    options = parser.parse_args()
    return Arguments(
        yad_id=options.yad_id,
        yad_password=options.yad_password,
        yad_token=options.yad_token,
        local_source_dir=options.source,
        yad_dest_dir=options.dest,
        tg_token=options.tg_token,
        tg_chats_id=options.tg_chat_ids,
    )


def existed_path(argument: str) -> str:
    if not os.path.exists(argument):
        raise argparse.ArgumentTypeError("%s folder does not exist" % argument)
    return argument
