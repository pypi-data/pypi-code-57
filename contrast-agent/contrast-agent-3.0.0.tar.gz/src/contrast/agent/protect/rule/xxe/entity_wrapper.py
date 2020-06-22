# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import re

from contrast.utils.object_share import ObjectShare


class EntityWrapper(object):
    SYSTEM_ID_REGEX = re.compile(r'<!ENTITY\s+([a-zA-Z0-f]+)\s+SYSTEM\s+"(.*?)">')
    PUBLIC_ID_REGEX = re.compile(
        r'<!ENTITY\s+([a-zA-Z0-f]+)\s+PUBLIC\s+".*?"\s+"(.*?)">'
    )
    DTD_MARKER = ".dtd"
    FILE_START = "file:"
    FTP_START = "ftp:"
    GOPHER_START = "gopher:"
    JAR_START = "jar:"
    UP_DIR_LINUX = "../"
    UP_DIR_WIN = "..\\"

    FILE_PATTERN_WINDOWS = re.compile(r"^[\\\\]*[a-z]{1,3}:.*", flags=re.IGNORECASE)

    def __init__(self, entity):
        self.system_id = self.parse_system_id(entity)
        self.public_id = self.parse_public_id(entity)
        self.external_entity = None

    def is_external_entity(self):
        if self.external_entity is None:
            if self.system_id:
                self.external_entity = self.external_id(self.system_id)
            elif self.public_id:
                self.external_entity = self.external_id(self.public_id)
            else:
                self.external_entity = None
        return self.external_entity

    def parse_system_id(self, entity):
        match = self.SYSTEM_ID_REGEX.search(entity)
        if not match:
            return ""
        return match.group(2)

    def parse_public_id(self, entity):
        match = self.PUBLIC_ID_REGEX.search(entity)
        if not match:
            return ""
        return match.group(2)

    def external_id(self, entity_id):
        tmp_id = entity_id.lower()

        http = self._starts_with_any(
            tmp_id, ObjectShare.HTTP_START, ObjectShare.HTTPS_START
        )

        if http and tmp_id.endswith(self.DTD_MARKER):
            return True

        if self._starts_with_any(
            tmp_id, self.FTP_START, self.FILE_START, self.JAR_START, self.GOPHER_START
        ):
            return True

        if self._starts_with_any(tmp_id, ObjectShare.SLASH, ObjectShare.PERIOD):
            return True

        if self._starts_with_any(tmp_id, self.UP_DIR_LINUX, self.UP_DIR_WIN):
            return True

        if self.FILE_PATTERN_WINDOWS.search(tmp_id):
            return True

    def _starts_with_any(self, string, *args):
        for arg in args:
            if string.startswith(arg):
                return True
        return False
