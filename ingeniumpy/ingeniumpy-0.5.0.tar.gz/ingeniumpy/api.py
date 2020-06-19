import platform
import subprocess
from os import path

from .connection import start_connection, CustomConnection
from .objects import *


def get_proxy_name():
    machine = platform.machine().lower()
    if "armv7" in machine:
        return "proxy-armv7"
    if "arm64" in machine or "aarch64" in machine or "armv8" in machine:
        return "proxy-arm64"
    if "arm" in machine:
        return "proxy-arm"

    if "x86_64" in machine or "amd64" in machine or "i686" in machine:
        return "proxy-x64"
    if "x86" in machine or "i386" in machine:
        return "proxy-x86"


PROXY_FOLDER = path.join(path.dirname(path.realpath(__file__)), "bin")
PROXY_NAME = get_proxy_name()
PROXY_BIN = path.join(PROXY_FOLDER, PROXY_NAME)


class IngeniumAPI:
    _user: str
    _pass: str
    _host: str

    _is_knx: bool = False
    _objects: List[IngObject] = []
    _connection: CustomConnection
    _proxy: subprocess.Popen

    def __init__(self, data: Dict[str, str]):
        self._user = data["username"].strip() if "username" in data else None
        self._pass = data["password"].strip() if "password" in data else None
        self._host = data["host"].strip() if "host" in data else None

    async def load(self, just_login=False, hass_integration=False):
        self._proxy = subprocess.Popen([PROXY_BIN], universal_newlines=True)
        await asyncio.sleep(1)

        try:
            login_result = await start_connection(self, self._host, self._user, self._pass, just_login,
                                                  hass_integration)
        except BaseException as e:
            print("Exception during login: " + repr(e) + " " + str(e))
            return False

        if login_result is None:
            return False

        # Add all the objects
        self._objects = []
        for o in login_result.get("devices"):
            # Filter out any external devices
            if o.get("externalId") is not None:
                continue

            ctype = get_device_type(o.get("ctype"))
            address = safecast(o.get("address"), int)

            # Skip over invalid types
            if ctype == IngComponentType.NOT_IMPLEMENTED or address is None:
                continue

            components = [IngComponent(c) for c in o.get("components")]

            if ctype.is_actuator():
                self._objects.append(IngActuator(self, self._is_knx, address, ctype, components))
            elif ctype.is_meterbus():
                self._objects.append(IngMeterBus(self, self._is_knx, address, ctype, components))
            elif ctype.is_tsif():
                self._objects.append(IngSif(self, self._is_knx, address, ctype, components))
            elif ctype.is_busing_regulator():
                self._objects.append(IngBusingRegulator(self, self._is_knx, address, ctype, components))
            elif ctype.is_thermostat():
                self._objects.append(IngThermostat(self, self._is_knx, address, ctype, components))

        return True

    @property
    def is_remote(self) -> bool:
        return self._host is None

    @property
    def is_knx(self) -> bool:
        return self._is_knx

    @property
    def objects(self) -> List[IngObject]:
        return self._objects

    @property
    def connection(self) -> CustomConnection:
        return self._connection

    async def send(self, p: Package):
        return await self.connection.send(p)

    async def close(self):
        await self.connection.close()
        if self._proxy is not None:
            self._proxy.terminate()
