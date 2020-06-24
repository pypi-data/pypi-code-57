#!/usr/bin/env python3.8
"""
Copyright::

    +===================================================+
    |                 © 2020 Privex Inc.                |
    |               https://www.privex.io               |
    +===================================================+
    |                                                   |
    |        Privex's Random IOTA Tools                 |
    |        License: X11/MIT                           |
    |                                                   |
    |        Core Developer(s):                         |
    |                                                   |
    |          (+)  Chris (@someguy123) [Privex]        |
    |                                                   |
    +===================================================+

    Privex's Random IOTA Tools
    Copyright (c) 2020    Privex Inc. ( https://www.privex.io )

"""
import argparse
import sys
import requests.exceptions
from typing import Optional, List, Tuple

from colorama import Fore
from privex.helpers import ErrHelpParser, empty, empty_if, DictObject

from privex.iota import settings
from privex.iota.client import PrivexIota, IOTANodeInfo
import logging

log = logging.getLogger(__name__)


def err(*args, file=sys.stderr, **kwargs):
    print(*args, file=file, **kwargs)


class CriticalNodeFailure(SystemExit):
    code = 2


STORAGE = DictObject(iota=None)


def get_iota(host=None, new_instance=False, **kwargs) -> PrivexIota:
    host = empty_if(host, settings.IOTA_HOST)
    if new_instance or empty(STORAGE.get('iota')):
        if 'iota' in STORAGE:
            del STORAGE['iota']
        STORAGE.iota = PrivexIota(adapter=host, **kwargs)
    return STORAGE.iota


def print_intro():
    err(Fore.MAGENTA)
    err(" ============================================================\n")
    err("    Privex IOTA Node Status Script \n")
    err("    Small python script to query sync status for an IOTA")
    err("    Node via the HTTP API.\n")
    err("    Source: https://github.com/Privex/iota-tools")
    err("    License: X11 / MIT\n")
    err("    (C) 2020 Privex Inc. ( https://www.privex.io )\n")
    err(" ============================================================\n", Fore.RESET)


def handle_args() -> argparse.Namespace:
    parser = ErrHelpParser(
        description="Privex IOTA Node Status Script ( https://www.privex.io )",
    )
    parser.add_argument(
        '--raw', dest='raw', action='store_true', default=False,
        help="When specified, show Raw JSON result instead of pretty printed colour output"
    )
    parser.add_argument(
        'host', default=settings.IOTA_HOST,
        help=f'Full HTTP(S) URL to an IOTA node. Defaults to: {settings.IOTA_HOST}', nargs='?'
    )
    
    parser.set_defaults(host=settings.IOTA_HOST, raw=False)
    
    args = parser.parse_args()

    settings.IOTA_HOST = args.host
    settings.RAW_MODE = args.raw
    
    return args


def load_node_info(host: Optional[str] = None) -> IOTANodeInfo:
    """
    
    :param host:
    :raises ConnectionRefusedError:
    :raises requests.exceptions.ConnectionError:
    :return:
    """
    host = empty_if(host, settings.IOTA_HOST)
    err(f"\n >>> {Fore.GREEN}Connecting to IOTA HTTP API...{Fore.RESET} {host}\n")
    api = get_iota(host=host)
    err(f" >>> {Fore.GREEN}Calling get_node_info / Processing node response...{Fore.RESET}\n")
    return api.get_node_info()


def main(host=None):
    print_intro()
    
    if not empty(host):
        settings.IOTA_HOST = host
    
    handle_args()
    try:
        r = load_node_info()
    except (ConnectionError, ConnectionRefusedError, requests.exceptions.ConnectionError) as e:
        log.error("Failed to connect to %s due to exception: %s %s", settings.IOTA_HOST, type(e), str(e))
        err(f" [!!!] {Fore.RED}CRITICAL ERROR! Cannot connect to host {settings.IOTA_HOST} - host is down?{Fore.RESET}")
        err(f" [!!!] {Fore.RED}Error reason:{Fore.RESET} {type(e)} - {str(e)}")
        raise CriticalNodeFailure(str(e))
    except requests.exceptions.HTTPError as e:
        log.error("Requests HTTPError raised while querying %s - exception was: %s %s", settings.IOTA_HOST, type(e), str(e))
        err(f" [!!!] {Fore.RED}ERROR! Host {settings.IOTA_HOST} threw a HTTP error - the node may be malfunctioning...{Fore.RESET}")
        err(f" [!!!] {Fore.RED}Error reason:{Fore.RESET} {type(e)} - {str(e)}")
        raise CriticalNodeFailure(str(e))
    
    if settings.RAW_MODE:
        err(f" >>> {Fore.YELLOW}Raw mode enabled. Printing JSON result:{Fore.RESET}\n")
        print(r.as_json)
        return

    cols = gen_cols(r)
    print(f"\n{Fore.BLUE}---- Node {settings.IOTA_HOST} ----{Fore.RESET}\n")
    iter_cols(cols)
    print()


def gen_cols(node_info: IOTANodeInfo) -> List[Tuple[str, str, str]]:
    behind = str(node_info.time_behind).split('.')[0]
    human_synced = f"{Fore.GREEN}YES{Fore.RESET}" if node_info.isSynced else f"{Fore.RED}NO{Fore.RESET}"
    return [
        (f'{Fore.CYAN}', 'Node URL', f'{settings.IOTA_HOST}'),
        (f'{Fore.RED}', 'Node Software', f'{node_info.appName}'),
        (f'{Fore.RED}', 'Software Version', f'{node_info.appVersion}'),
        (f'{Fore.RED}', 'Co-ordinator Address', f'{node_info.coordinatorAddress}'),
        (f'{Fore.RED}', 'Features', ', '.join(node_info.features)),
        ('', '', ''),
        (f'{Fore.YELLOW}', 'Synced?', f'{human_synced}'),
        (f'{Fore.YELLOW}', 'Sync Time', f'{str(node_info.time_date)}'),
        (f'{Fore.YELLOW}', 'Time Behind', f'{behind}'),
        ('', '', ''),
        (f'{Fore.GREEN}', 'Neighbors', f'{node_info.neighbors}'),
        ('', '', ''),
        (f'{Fore.CYAN}', 'Latest Milestone', f'{node_info.latestMilestone}'),
        (f'{Fore.CYAN}', 'Latest Solid Subtangle Milestone', f'{node_info.latestSolidSubtangleMilestone}'),
        (f'{Fore.CYAN}', 'Latest Milestone Index', f'{node_info.latestMilestoneIndex}'),
        (f'{Fore.CYAN}', 'Milestone Start Index', f'{node_info.milestoneStartIndex}'),
        (f'{Fore.CYAN}', 'Last Snapshotted Milestone Index', f'{node_info.lastSnapshottedMilestoneIndex}'),
    ]


def iter_cols(columns: List[Tuple[str, str, str]]):
    for colour, title, val in columns:
        if empty(title):
            print()
            continue
        title += ":"
        print(f"{colour}{title:<50}{Fore.RESET}{val}")



