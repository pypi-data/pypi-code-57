"""GRAPHISOFT"""

from typing import Dict, Any, Tuple
from urllib.request import Request, urlopen
import json


class UnsucceededCommandCall(Exception):
    pass


def post_command(req: Request, jsonStr: str) -> Dict[str, Any]:
    response = urlopen(req, jsonStr.encode("UTF-8"))
    result = response.read()
    return json.loads(result)


class BasicCommands:
    """Collection of the ARCHICAD JSON interface commands
    """
    def __init__(self, req: Request):
        assert req is not None
        self.__req = req

    def IsAlive(self) -> bool:
        """Checks if the ARCHICAD connection is alive.

        Returns:
            bool: Returns true if the connection is alive.

        """

        result = post_command(self.__req, json.dumps({"command": "API.IsAlive"}))
        if not result["succeeded"]:
            raise UnsucceededCommandCall(result)
        return result["result"]["isAlive"]

    def GetProductInfo(self) -> Tuple[int, int, str]:
        """Accesses the version information from the running ARCHICAD.

        Returns:
            int: The version of the running ARCHICAD.
            int: The build number of the running ARCHICAD.
            str: The language code of the running ARCHICAD.

        """

        result = post_command(self.__req, json.dumps({"command": "API.GetProductInfo"}))
        if not result["succeeded"]:
            raise UnsucceededCommandCall(result)
        return result["result"]["version"], result["result"]["buildNumber"], result["result"]["languageCode"]
