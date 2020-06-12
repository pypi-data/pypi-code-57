from __future__ import annotations

import functools
from logging import warning
from pathlib import Path
from typing import Any, Iterable, List, Optional, Union, Dict, Callable, TypeVar

import stringcase
from lxml import etree
from pydantic import BaseModel, Field
from upnpclient import Device, Action
from upnpclient.soap import SOAPError


class APIError(Exception):
    def __init__(self, message: str, **extra: Any):
        super().__init__(message, extra)
        self.message = message
        self.extra = extra

    def __str__(self) -> str:
        return f"""{
            self.message
        }{
            f'''({
                ' '.join(f'{key}={val!r}' for key, val in self.extra.items())
            })''' if self.extra else ''
        }"""


class Config:
    alias_generator = stringcase.camelcase
    allow_population_by_field_name = True


class MediaDevice(BaseModel):
    Config = Config

    udn: str
    name: str = Field(alias='friendly_name')
    description: str = Field(alias='model_description')
    location: str
    icon_url: Optional[str] = None
    presentation_url: Optional[str] = None


class MediaSink(BaseModel):
    Config = Config

    url: str
    meta: Dict[str, Any]


class ServerEntity(BaseModel):
    Config = Config

    id: str
    type: str
    name: str


class MediaContainer(ServerEntity):
    child_count: int


class MediaItem(ServerEntity):
    sinks: List[MediaSink]


class VideoItem(MediaItem):
    pass


class PhotoItem(MediaItem):
    pass


T = TypeVar('T')


def _catch_inner_errors(func: Callable[..., T]) -> Callable[..., T]:
    from requests import exceptions

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except exceptions.RequestException as err:
            raise APIError(
                'error occurs while talking with a server',
                error_type=stringcase.snakecase(type(err).__name__),
            ) from err
        except SOAPError as err:
            raise APIError(err.args[1])

    return wrapper


class _ItemSearcher:
    def __init__(self, browse_action: Action):
        self._browse_action = browse_action

    def lookup_child_id_by_path(self, path: Path) -> str:
        last_id: str = '0'

        for segment in path.parts:
            children = etree.fromstring(
                self._browse_action(
                    ObjectID=last_id,
                    BrowseFlag='BrowseDirectChildren',
                    Filter='*',
                    StartingIndex=0,
                    RequestedCount=100000,
                    SortCriteria='',
                )['Result']
            )
            for child in children:
                child_title: Optional[str] = child.findtext('{*}title')
                if child_title == segment:
                    last_id = child.attrib['id']
                    break
            else:
                raise APIError('could not find child by path', path=path)
        return last_id


class DLNAApi:
    DLNA_DEVICE_UPNP_TYPE = 'urn:schemas-upnp-org:device:MediaServer:1'

    ENTITY_CLS_BY_TYPE = {
        'storageFolder': MediaContainer,
        'container': MediaContainer,
        'videoItem': VideoItem,
        'photo': PhotoItem,
    }

    def __init__(self, devices: List[Device]):
        self._devices = devices

    @_catch_inner_errors
    def list_servers(self) -> Iterable[MediaDevice]:
        return (
            MediaDevice(**device.__dict__)
            for device in self._devices
            if device.device_type == self.DLNA_DEVICE_UPNP_TYPE
        )

    @_catch_inner_errors
    def list_server_items(
        self, served_identificator: Union[str, int], parent: str = None
    ) -> Iterable[ServerEntity]:
        server: Device

        if isinstance(served_identificator, int):
            try:
                server = self._devices[served_identificator]
            except IndexError:
                raise APIError(
                    'could not find server by specified index',
                    index=served_identificator,
                )
        else:
            raise APIError(
                'usage error: server identity must be either index '
                'of server in the servers list or his identifier',
                served_identificator=served_identificator,
            )

        try:
            device_browse_action = server.find_action('Browse')
        except (StopIteration, KeyError):
            raise APIError(
                "internal error: suddenly, server doesn't supports DLNA capabilities",
                server_udn=server.udn,
                server_name=server.friendly_name,
                server_location=server.location,
            )

        if not parent:
            parent = '0'
        else:
            searcher = _ItemSearcher(device_browse_action)
            parent = searcher.lookup_child_id_by_path(Path(parent))

        query_result = device_browse_action(
            ObjectID=parent,
            BrowseFlag='BrowseDirectChildren',
            Filter='*',
            StartingIndex=0,
            RequestedCount=9,
            SortCriteria='',
        )
        return (
            child for child in self._parse_children_response(query_result['Result'])
        )

    def _parse_children_response(self, body: str) -> List[ServerEntity]:
        def process(elem: etree.ElementBase) -> Optional[Dict[str, Any]]:
            tag = elem.tag[pos + 1 if (pos := elem.tag.find('}')) != -1 else 0 :]
            if tag == 'container':
                return process_container(elem)
            elif tag == 'item':
                return process_item(elem)
            else:
                warning(f'no entity with tag "{tag}" supported')
                return None

        def process_base_media_item(elem: etree.ElementBase) -> Dict[str, Any]:
            e_type = elem.findtext('{*}class')
            if '.' in e_type:
                e_type = e_type.split('.')[-1]
            return {
                'name': elem.findtext('{*}title'),
                'type': e_type,
                **elem.attrib,
            }

        def process_container(elem: etree.ElementBase) -> Dict[str, Any]:
            return process_base_media_item(elem)

        def process_item(elem: etree.ElementBase) -> Dict[str, Any]:
            url_descrs = elem.findall('{*}res')
            return {
                **process_base_media_item(elem),
                'date': elem.findtext('{*}date'),
                'sinks': [
                    {'url': descr.text, 'meta': descr.attrib} for descr in url_descrs
                ],
            }

        root = etree.fromstring(body)
        return [
            self.ENTITY_CLS_BY_TYPE.get(raw['type'], ServerEntity)(**raw)
            for raw in (
                processed
                for processed in (process(elem) for elem in root)
                if processed is not None
            )
        ]
