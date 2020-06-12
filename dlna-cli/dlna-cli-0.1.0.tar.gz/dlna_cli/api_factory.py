from __future__ import annotations

import os
import pickle
from asyncio import Protocol
from dataclasses import dataclass
from pathlib import Path
from tempfile import gettempdir
from typing import Dict, List, Optional, cast

from dlna_cli.api import DLNAApi
from dlna_cli.upnp_device import discover_devices, UPNPDevice

DEFAULT_CACHE_FILE = Path(gettempdir()) / 'dlna-cli-cache'
DEFAULT_SCAN_TIMEOUT = 5.0


def create_api_from_discoverer(discoverer: DevicesDiscoverer) -> DLNAApi:
    return DLNAApi(discoverer.discover())


class DevicesDiscoverer(Protocol):
    def discover(self) -> List[UPNPDevice]:
        raise NotImplementedError


class ScanDevicesDiscoverer:
    def __init__(self, scan_timeout: float = DEFAULT_SCAN_TIMEOUT):
        self.scan_timeout = scan_timeout

    def discover(self) -> List[UPNPDevice]:
        return discover_devices(self.scan_timeout)


@dataclass
class _CacheObj:
    devices: Dict[str, UPNPDevice]
    device_udn_order: List[str]


class CacheKeepDeviceIDXDiscoverer:
    def __init__(
        self, inner: DevicesDiscoverer = None, cache_file: Path = DEFAULT_CACHE_FILE
    ):
        self._inner = inner or ScanDevicesDiscoverer()
        self.cache_file = cache_file

    def discover(self) -> List[UPNPDevice]:
        cache = self._load_cache()
        if cache is None:
            devices = self._inner.discover()
            udn_order = [dev.udn for dev in devices]
            devices_by_udn = {dev.udn: dev for dev in devices}
            cache = _CacheObj(devices_by_udn, udn_order)
            self._save_cache(cache)
            return devices

        return [cache.devices[udn] for udn in cache.device_udn_order]

    def _load_cache(self) -> Optional[_CacheObj]:
        try:
            with open(self.cache_file, 'rb') as file:
                loaded = pickle.load(file)
                if not isinstance(loaded, _CacheObj):
                    raise EOFError

                return cast(_CacheObj, loaded)
        except EOFError:
            os.remove(self.cache_file)
            return None
        except (FileNotFoundError, PermissionError):
            return None

    def _save_cache(self, cache: _CacheObj):
        with open(self.cache_file, 'wb') as file:
            pickle.dump(cache, file)
