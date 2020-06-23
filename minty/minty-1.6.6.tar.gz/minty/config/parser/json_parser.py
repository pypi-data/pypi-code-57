import json
from .base import ConfigParserBase
from typing import Dict


class JSONConfigParser(ConfigParserBase):
    __slots__ = ["content"]

    def parse(self, content: str) -> Dict:
        """Parse JSON file and return dict.

        :param content: content from JSON file
        :type content: str
        :raises ValueError: if content is empty
        :return: parsed config dict
        :rtype: dict
        """
        preparsed_content = super().parse(content)

        if preparsed_content["content"] == "":
            raise ValueError("Cannot parse empty configuration")

        with self.statsd.get_timer().time("parse_time"):
            config = json.loads(preparsed_content["content"])

        self.statsd.get_counter().increment("parse")
        return config
