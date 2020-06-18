"""Module that contains the `infoten.plugin.manager.PluginManager`
class.
"""

from typing import List

from .base import AbstractDevice, AbstractImplementation, Visibility


class PluginManager:
    """Provides access to all intances of both
    `infoten.plugin.base.AbstractDevice` and
    `infoten.plugin.base.AbstractImplementation` in the infoTEN system.
    """

    def __init__(self):
        self._dev = None
        self._all_devs = []
        self._all_dev_names = []
        self._all_imps = []
        self._all_imp_names = []
        self.refresh()

    @property
    def dev(self) -> AbstractDevice:
        """The currently-selected `infoten.plugin.base.AbstractDevice`
        instance.
        """

        return self._dev

    @dev.setter
    def dev(self, d: str):
        assert isinstance(d, str)
        if d not in self.all_dev_names:
            raise ValueError
        self._dev = self.all_devs[self.all_dev_names.index(d)]

    @property
    def all_devs(self) -> List[object]:
        """A list of all instances of
        `infoten.plugin.base.AbstractDevice` present in the system.
        """

        return self._all_devs

    @property
    def all_dev_names(self) -> List[str]:
        """A list of the names of all instances of
        `infoten.plugin.base.AbstractDevice` present in the system.
        """

        return self._all_dev_names

    @property
    def all_imps(self) -> List[object]:
        """A list of all instances of
        `infoten.plugin.base.AbstractImplementation` present in the
        system.
        """

        return self._all_imps

    @property
    def all_imp_names(self) -> List[str]:
        """A list of the names of all instances of
        `infoten.plugin.base.AbstractImplementation` present in the
        system.
        """

        return self._all_imp_names

    def devs(self, visibility: Visibility) -> List[object]:
        """Returns a list of all instances of
        `infoten.plugin.base.AbstractDevice` that have the specified
        `infoten.plugin.base.Visibility`.
        """
        assert isinstance(visibility, Visibility)
        return [d for d in self.all_devs if d.visibility is visibility]

    def dev_names(self, visibility: Visibility) -> List[str]:
        """Returns a list of names of all instances of
        `infoten.plugin.base.AbstractDevice` that have the specified
        `infoten.plugin.base.Visibility`.
        """
        assert isinstance(visibility, Visibility)
        return [d.name for d in self.all_devs if d.visibility is visibility]

    def refresh(self):
        """Rebuilds all lists in this class."""
        self._build_devs()
        self._build_imps()

    def _build_devs(self):
        for dev_obj in AbstractDevice.instances():
            self._all_devs.append(dev_obj)
            self._all_dev_names.append(dev_obj.name)

    def _build_imps(self):
        for imp_obj in AbstractImplementation.instances():
            self._all_imps.append(imp_obj)
            self._all_imp_names.append(imp_obj.name)
