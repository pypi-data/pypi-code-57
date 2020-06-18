"""Module that provides all bases classes needed to create a device
plugin for the infoTEN system.
"""

import weakref
from abc import ABC, abstractmethod
from enum import Enum, auto
from inspect import getmembers, isfunction, signature
from typing import Any, Generator, List, Tuple, Union


class UserGui(ABC):
    """The UserGui class is the base class for all GUIs that
    will expose user functions to the user functions.
    """

    pass


class AdminGui(ABC):
    """The AdminGui class is the base class for all GUIs that
    will expose user functions to the admin functions.
    """

    pass


class AbstractPluginEntity(ABC):
    """The AbstractPluginEntity class is the most base class for
    infoTEN device plugins.
    """

    def __init__(self, name: str):
        assert isinstance(name, str)
        self._name = name

    @property
    def name(self) -> str:
        """Read Only (set at object creation). The name of the entity.
        For instances of `infoten.plugin.base.AbstractDevice`, "name"
        must be unique among all instances of
        `infoten.plugin.base.AbstractDevice`. For instances of
        `infoten.plugin.base.AbstractImplementation`, "name" only needs
        to be unique among all instances of
        `infoten.plugin.base.AbstractImplementation` bound to a
        specific instance of `infoten.plugin.base.AbstractDevice`.
        """

        return self._name

    @abstractmethod
    def status(self) -> bool:
        """Returns the status of an instance of
        `infoten.plugin.base.AbstractPluginEntity`.
        """

        pass


class AbstractImplementation(AbstractPluginEntity):
    """The AbstractImplementation class is inherited by any device
    implementation. While this class has no implementation, it serves
    to help identify implementations in general and for a specific
    device.
    """

    # See http://effbot.org/pyfaq/how-do-i-get-a-list-of-all-instances-
    # of-a-given-class.htm
    _instances = set()

    def __init__(self, name: str):
        super().__init__(name=name)
        self.devices = []
        """An implementations device's."""

        # If an implementation uses a device, add it to the
        # implementation's device list.
        for obj_name, obj in getmembers(self):
            if isinstance(obj, AbstractDevice):
                self.devices.append(obj)

        self._instances.add(weakref.ref(self))

    @classmethod
    def instances(cls) -> Generator[object, None, None]:
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead


class Visibility(Enum):
    """Enumeration that defines the visibility of an instance of
    `infoten.plugin.base.AbstractDevice`. USER means the device can be
    directly accessed from the Test Case Creator and the device's GUI
    can be accessed by any user. IMP means the device is used in an
    implementation of a different device, and only admin functions will
    be able to be acccess.

    A device with visibility USER can still be used in a different
    device's implementation. In this scenario, the device is both
    accessible for direct control by any user, and is used as an
    implementation device.
    """

    USER = auto()
    IMP = auto()


class AbstractDevice(AbstractPluginEntity):
    """The Device class provides common functionality to all
    devices in the infoTEN plugin system.
    """

    # See http://effbot.org/pyfaq/how-do-i-get-a-list-of-all-instances-
    # of-a-given-class.htm
    _instances = set()

    def __init__(self, name: str, visibility: Visibility):
        self._visibility = visibility
        self._imp = None
        self._user_gui = None
        self._admin_gui = None

        self.imps = []
        """A list containing all instances of
        `infoten.plugin.base.AbstractImplementation` for a specific
        instance of `infoten.plugin.base.AbstractDevice`.
        """

        # Ensure the Device "name" property is unique
        names = [obj.name for obj in AbstractDevice.instances()]
        if name in names:
            raise ValueError(f'an instance of AbstractDevice with name'
                             '={name} already exists. "name" must be unique.')
        super().__init__(name=name)
        self._instances.add(weakref.ref(self))

    @property
    def visibility(self) -> Visibility:
        """The visibility level of a device."""
        return self._visibility

    @visibility.setter
    def visibility(self, v: Visibility):
        assert isinstance(v, Visibility)
        self._visibility = v

    @property
    def imp(self) -> AbstractImplementation:
        """The currently selected instance of
        `infoten.plugin.base.AbstractImplementation` for this device.
        This value is set to the 0th item in
        `infoten.plugin.base.AbstractDevice.imps` the first time
        `infoten.plugin.base.AbstractDevice.add_imp` is called in order
        to provide a default value.
        """

        return self._imp

    @imp.setter
    def imp(self, i: str):
        assert isinstance(i, str)
        self._imp = self.imps[self.imp_names.index(i)]

    @property
    def imp_names(self) -> List[str]:
        """The names of all 
        `infoten.plugin.base.AbstractImplementation` instances 
        belonging to an instance of
        `infoten.plugin.base.AbstractDevice`.
        """

        return [i.name for i in self.imps]

    @property
    def user_gui(self) -> UserGui:
        """The GUI, an instance of `infoten.plugin.base.UserGui`, that
        will expose all user functions to the end user.
        """

        return self._user_gui

    @user_gui.setter
    def user_gui(self, g: UserGui):
        assert isinstance(g, UserGui)
        self._user_gui = g

    @property
    def admin_gui(self) -> AdminGui:
        """The GUI, an instance of `infoten.plugin.base.AdminGui`, that
        will expose all admin functions to the end user.
        """

        return self._admin_gui

    @admin_gui.setter
    def admin_gui(self, g: AdminGui):
        assert isinstance(g, AdminGui)
        self._admin_gui = g

    def user_fns(self) -> List[str]:
        """Returns the names of a device's user functions."""

        return self._get_fns(AbstractUserFunctions)

    def admin_fns(self) -> List[str]:
        """Returns the names of a device's admin functions."""

        return self._get_fns(AbstractAdminFunctions)

    def fn_args(self, func_name: str) -> List[Tuple[str, type, Any]]:
        """
        Inspects a device to retrieve the parameters for the specified
        function. Returns a list of parameters, where each element is a
        tuple containing a parameter name, type, and default value in
        that order (order follows Python type hint syntax). If there
        are no parameters, the returned list is empty.

        If the parameter type or default value is not specified in the
        original function, their value will be "inspect._empty", which
        is equivalent to inspect.Parameter.empty (useful for type
        checking).
        """

        args = []
        for base in type(self.imps[0]).__bases__:
            for fn_name, fn_obj in getmembers(base, isfunction):
                if fn_name != func_name:
                    continue
                if not self._is_dunder(fn_obj):
                    sig = signature(fn_obj)
                    for arg_name, param in sig.parameters.items():
                        if arg_name == 'self':
                            continue
                        args.append(
                            (arg_name, param.annotation, param.default))
        return args

    def call_fn(self, func_name: str, *args, **kwargs):
        """Calls a device's function using the currently-selected
        implementation. Any arguments to be passed to the function are
        handled by \*args and \**kwargs.

        For example, if there was a device with a function
        "touch_screen" with argumments "x" and "y", both of the
        following calls would be correct. Note that this example does
        not show all possible call examples.\n\t
            call_fn("touch_screen", 3, 54)\n\t
            call_fn("touch_screen", x=3, y=54)

        Parameters
        ----------
        func_name : str
            The name of the function to be called.
        """

        try:
            getattr(self.imp, func_name)(*args, **kwargs)
        except AttributeError:
            print('either "imp" or "func_name" is not correct')
        except TypeError:
            print('missing arguments')

    def add_imp(self, imp: AbstractImplementation):
        """Adds an instance of
        `infoten.plugin.base.AbstractImplementation` to an instance of
        `infoten.plugin.base.AbstractDevice`. The first instance of
        `infoten.plugin.base.AbstractImplementation` that's added is
        automatcially set as the current implementation.

        Parameters
        ----------
        imp : An instance of
            `infoten.plugin.base.AbstractImplementation`.

        Raises
        ------
        TypeError
            Raised if 'imp' is not an instance of
            `infoten.plugin.base.AbstractImplementation`.

        ValueError
            Raised if an instance of
            `infoten.plugin.base.AbstractDevice` already has an
            instance of `infoten.plugin.base.AbstractImplementation`
            with the same value for
            `infoten.plugin.base.AbstractImplementation.name`.
        """

        if not isinstance(imp, AbstractImplementation):
            raise TypeError(
                '"imp" must be an instance of "AbstractImplementation"')

        imp_names = [i.name for i in self.imps]
        if imp.name in imp_names:
            raise ValueError(f'"{self.name}" already has an instance of '
                             'AbstractImplementation with name='
                             f'"{imp.name}". Implementation names must be '
                             'unique for a specific device.')

        self.imps.append(imp)
        if len(self.imps) == 1:
            self.imp = self.imps[0].name

    def status(self) -> bool:
        """Returns the status of an
        `infoten.plugin.base.AbstractDevice` instance. This assumes
        that as long as one instance of
        `infoten.plugin.base.AbstractImplementation` has an
        `infoten.plugin.base.AbstractImplementation.status` of True,
        then the instance of `infoten.plugin.base.AbstractDevice`
        itself is True.

        This assumption may of course be incorrect. For example, maybe
        other conditions need to be met for an instance of
        `infoten.plugin.base.AbstractDevice` to have a
        `infoten.plugin.base.AbstractPluginEntity.status` of True. In
        this case, this should be overridden.
        """

        for imp in self.imps:
            if imp.status():
                return True
        return False

    def _is_dunder(self, method: Union[str, object]) -> bool:
        """Checks if a method name corresponds to a dunder method.

        Parameters
        ----------
        method : Union[str, object]
            The method name or method object.
        """

        try:
            method = method.__name__
        except AttributeError:
            pass
        return method.startswith('__') and method.endswith('__')

    def _get_fns(self, base_class) -> List[str]:
        fns = []
        for base in type(self.imps[0]).__bases__:
            if issubclass(base, base_class):
                for fn_name, _ in getmembers(base, isfunction):
                    fns.append(fn_name)
                break
        return fns

    @classmethod
    def instances(cls) -> Generator[object, None, None]:
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead


class AbstractUserFunctions(ABC):
    """The AbstractUserFunctions class is the base class for all
    interfaces that contain user functions.
    """

    pass


class AbstractAdminFunctions(ABC):
    """The AbstractAdminFunctions class is the base class for all
    interfaces that contain admin functions.
    """

    pass
