from __future__ import annotations
from copy import copy
from functools import partial
from typing import List

from lxml import etree
from upnpclient import Device, Service, discover
from upnpclient.util import _getLogger


class UPNPService(Service):
    def __setstate__(self, state):
        self.__dict__ = state
        self._log = _getLogger('Service')
        self.scpd_xml = etree.fromstring(state['xml'])
        self._find = partial(self.scpd_xml.find, namespaces=self.scpd_xml.nsmap)
        self._findtext = partial(self.scpd_xml.findtext, namespaces=self.scpd_xml.nsmap)
        self._findall = partial(self.scpd_xml.findall, namespaces=self.scpd_xml.nsmap)

    def __getstate__(self):
        self_dict = copy(self.__dict__)
        del self_dict['scpd_xml']
        del self_dict['_find']
        del self_dict['_findall']
        del self_dict['_findtext']
        del self_dict['_log']
        self_dict['xml'] = etree.tostring(self.scpd_xml)
        return self_dict


class UPNPDevice(Device):
    @classmethod
    def from_device(cls, device: Device) -> UPNPDevice:
        device.__class__ = UPNPDevice
        for service in device.services:
            service.__class__ = UPNPService

        return device

    def __setstate__(self, state):
        self.__dict__ = state
        root = self._root_xml = etree.fromstring(state['xml'])
        findtext = partial(root.findtext, namespaces=root.nsmap)
        self._log = _getLogger('Device')
        self._findtext = findtext
        self._find = partial(root.find, namespaces=root.nsmap)
        self._findall = partial(root.findall, namespaces=root.nsmap)

    def __getstate__(self):
        self_dict = copy(self.__dict__)
        del self_dict['_root_xml']
        del self_dict['_find']
        del self_dict['_findall']
        del self_dict['_findtext']
        del self_dict['_log']
        self_dict['xml'] = etree.tostring(self._root_xml)
        return self_dict


def discover_devices(timeout: float = 2) -> List[UPNPDevice]:
    return [UPNPDevice.from_device(dev) for dev in discover(timeout)]
