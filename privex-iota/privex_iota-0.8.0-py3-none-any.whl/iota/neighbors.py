from collections import namedtuple
from typing import Dict, List

from colorama import Fore
from iota import BadApiResponse
from privex.helpers import DictObject, empty_if

from privex.iota import settings
from privex.iota.client import err, get_iota
from privex.iota.objects import Neighbor
import logging

log = logging.getLogger(__name__)


NEIGHBOR_COLS = [
    'address', 'connected', 'domain', 'alias', 'connectionType', 'autopeeringId', 'numberOfAllTransactions',
    'numberOfReceivedMilestoneReq', 'numberOfSentHeartbeats'
]
NEIGHBOR_TITLE_COLOUR = Fore.MAGENTA
NEIGHBOR_ROW_COLOUR = Fore.CYAN
NeighborTableRow = namedtuple(
    'NodeTableRow',
    'address connected domain alias connectionType autopeeringId numberOfAllTransactions '
    'numberOfReceivedMilestoneReq numberOfSentHeartbeats',
)
NeighborTableColumn = namedtuple('NeighborTableColumn', 'title title_padding content_padding', defaults=(25, 25))

# Mapping of NeighborTableRow key, to a tuple of (column_title, title_padding, content_padding)
table_columns: Dict[str, NeighborTableColumn] = DictObject(
    address=NeighborTableColumn('Address', 55, 55),
    connected=NeighborTableColumn('Connected?', 22, 32),
    domain=NeighborTableColumn('Domain', 40, 40),
    alias=NeighborTableColumn('Alias', 40, 40),
    connectionType=NeighborTableColumn('Proto', 20, 20),
    autopeeringId=NeighborTableColumn('Peer ID', 35, 35),
    numberOfAllTransactions=NeighborTableColumn('Total TX', 25, 25),
    numberOfReceivedMilestoneReq=NeighborTableColumn('Recv Milestones', 30, 30),
    numberOfSentHeartbeats=NeighborTableColumn('Heartbeats', 25, 25),
)


def _neighbor_row(neighbor: Neighbor):
    n = DictObject(
        address=neighbor.address,
        domain=neighbor.domain,
        alias=empty_if(neighbor.alias, 'N/A'),
        connectionType=neighbor.connectionType,
        autopeeringId=empty_if(neighbor.autopeeringId, 'N/A'),
        numberOfAllTransactions=str(neighbor.numberOfAllTransactions),
        numberOfReceivedMilestoneReq=str(neighbor.numberOfReceivedMilestoneReq),
        numberOfSentHeartbeats=str(neighbor.numberOfSentHeartbeats),
    )
    n.connected = f"{Fore.GREEN}YES{Fore.RESET}" if neighbor.connected else f"{Fore.RED}NO{Fore.RESET}"
    return NeighborTableRow(**n)


def _render_neighbor_row(row: NeighborTableRow = None, columns: list = None) -> str:
    columns = empty_if(columns, NEIGHBOR_COLS)
    r = ''
    
    for c in columns:
        col = table_columns[c]
        data, padding = NEIGHBOR_TITLE_COLOUR + col.title + Fore.RESET, col.title_padding
        if row:
            data, padding = NEIGHBOR_ROW_COLOUR + getattr(row, c) + Fore.RESET, col.content_padding

        r += ("{:<" + str(padding) + "}").format(str(data))
    
    return r


def display_neighbors():
    try:
        api = get_iota(host=settings.IOTA_HOST)
        res = api.get_neighbors()
    except BadApiResponse as e:
        lowmsg = str(e).lower()
        if 'command' in lowmsg and 'is protected' in lowmsg:
            err(f" [!!!] {Fore.YELLOW}Warning: cannot display neighbors as node {settings.IOTA_HOST} is a remote host.{Fore.RESET}")
            err(f" [!!!] {Fore.YELLOW}The getNeighbors API appears to be disabled for security reasons.{Fore.RESET}\n")
            return False
        log.error("BadApiResponse raised while querying %s - exception was: %s %s", settings.IOTA_HOST, type(e), str(e))
        err(f" [!!!] {Fore.RED}Error reason:{Fore.RESET} {type(e)} - {str(e)}")
        return False
    
    print(f"{Fore.GREEN}Neighbour List:{Fore.RESET}")
    _print_neighbors(res.neighbors)


def _print_neighbors(neighbors: List[Neighbor]):
    ncols = [_neighbor_row(n) for n in neighbors]
    print(_render_neighbor_row())
    for n in ncols:
        print(_render_neighbor_row(n))
    print()
