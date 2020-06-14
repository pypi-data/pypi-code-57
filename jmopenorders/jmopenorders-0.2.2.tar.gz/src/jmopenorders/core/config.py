#
# Copyright (c) 2019-2020 Jürgen Mülbert. All rights reserved.
#
# Licensed under the EUPL, Version 1.2 or – as soon they
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
#
# https://joinup.ec.europa.eu/page/eupl-text-11-12
#
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
#
# Lizenziert unter der EUPL, Version 1.2 oder - sobald
#  diese von der Europäischen Kommission genehmigt wurden -
# Folgeversionen der EUPL ("Lizenz");
# Sie dürfen dieses Werk ausschließlich gemäß
# dieser Lizenz nutzen.
# Eine Kopie der Lizenz finden Sie hier:
#
# https://joinup.ec.europa.eu/page/eupl-text-11-12
#
# Sofern nicht durch anwendbare Rechtsvorschriften
# gefordert oder in schriftlicher Form vereinbart, wird
# die unter der Lizenz verbreitete Software "so wie sie
# ist", OHNE JEGLICHE GEWÄHRLEISTUNG ODER BEDINGUNGEN -
# ausdrücklich oder stillschweigend - verbreitet.
# Die sprachspezifischen Genehmigungen und Beschränkungen
# unter der Lizenz sind dem Lizenztext zu entnehmen.
#
"""Global application configuration.

This module defines a global configuration object. Other modules should use
this object to store application-wide configuration values.

"""
from re import compile
from typing import Any, Dict

from yaml import safe_load

from .logger import logger

__all__ = ["config", "YamlConfig"]


class _AttrDict(Dict):
    """A dict-like object with attribute access."""

    def __getitem__(self, key: str) -> Any:
        """Access dict values by key.

        Args:
            key: key to retrieve

        Returns:
            Any: The item
        """
        value = super().__getitem__(key)
        if isinstance(value, dict):
            # For mixed recursive assignment (e.g. `a["b"].c = value` to work
            # as expected, all dict-like values must themselves be _AttrDicts.
            # The "right way" to do this would be to convert to an
            # _AttrDict on
            # assignment, but that requires overriding both __setitem__
            # (straightforward) and __init__ (good luck). An explicit type
            # check is used here instead of EAFP because exceptions would be
            # frequent for hierarchical data with lots of nested dicts.
            self[key] = value = _AttrDict(value)
        return value

    def __getattr__(self, key: str) -> Any:
        """Get dict values as attributes.

        Args:
            key: key to retrieve

        Returns:
            Any: The DictValue from the key.
        """
        return self[key]

    def __setattr__(self, key: str, value: str) -> None:
        """Set dict values as attributes.

        Args:
            key: key to set
            value: new value for key
        """
        self[key] = value
        return


class YamlConfig(_AttrDict):
    """Store YAML configuration data.

    Data can be accessed as dict values or object attributes.
    """

    def __init__(self, path: str, root: str, macros: Dict) -> Any:
        """Initialize this object.

        Args:
            path: config file path to load
            root: place config values at this root
            macros: macro substitutions
        """
        super().__init__()
        if path:
            self.load(path, root, macros)
        return

    def load(self, path: str, root: str, macros: Dict) -> Any:
        """Load data from YAML configuration files.

        Configuration values are read from a sequence of one or more YAML
        files. Files are read in the given order, and a duplicate value will
        overwrite the existing value. If 'root' is specified the config data
        will be loaded under that attribute instead of the dict root.

        The optional 'macros' argument is a dict-like object to use for macro
        substitution in the config files. Any text matching "%key;" will be
        replaced with the value for 'key' in 'macros'.

        Args:
            path: config file path to load
            root: place config values at this root
            macros: macro substitutions
        """

        def replace(match: Dict) -> str:
            """Callback for re.sub to do macro replacement.

            Args:
                match: The search pattern.

            Returns:
                The macro that match.
            """
            # This allows for multi-pattern substitution in a single pass.
            return macros[match.group(0)]

        macros = (
            {fr"%{key:s};": val for (key, val,) in macros.items()} if macros else {}
        )
        regex = compile("|".join(macros) or r"^(?!)")
        for path in [path] if isinstance(path, str) else path:
            with open(path) as stream:
                # Global text substitution is used for macro replacement. Two
                # drawbacks of this are 1) the entire config file has to be
                # read into memory first; 2) it might be nice if comments were
                # excluded from replacement. A more elegant (but complex)
                # approach would be to use PyYAML's various hooks to do the
                # substitution as the file is parsed.
                logger.info(f"reading config data from '{path:s}'")
                yaml = regex.sub(replace, stream.read())
            data = safe_load(yaml)
            try:
                if root:
                    self.setdefault(root, {}).update(data)
                else:
                    self.update(data)
            except TypeError:  # data is None
                logger.warning(f"config file {path:s} is empty")
        return


config = YamlConfig()
