import signal
import sys

from .qt import QtCore
from .qt import QtGui
from .qt import QtWidgets
from .qt import bind

from .icon import Icon
from .object import Object

__all__ = ['CoreApplication', 'GuiApplication', 'Application']

@bind(QtCore.QCoreApplication)
class CoreApplication(Object):

    def __init__(self, name=None, *, version=None, organization=None,
                 domain=None, name_changed=None, version_changed=None,
                 organization_changed=None, domain_changed=None):
        super().__init__(sys.argv)
        if name is not None:
            self.name = name
        if version is not None:
            self.version = version
        if organization is not None:
            self.organization = organization
        if domain is not None:
            self.domain = domain
        self.name_changed = name_changed
        self.version_changed = version_changed
        self.organization_changed = organization_changed
        self.domain_changed = domain_changed
        # Connect signals
        self.qt.applicationNameChanged.connect(self.__handle_name_changed)
        self.qt.applicationVersionChanged.connect(self.__handle_version_changed)
        self.qt.organizationNameChanged.connect(self.__handle_organization_changed)
        self.qt.organizationDomainChanged.connect(self.__handle_domain_changed)

    @classmethod
    def instance(cls):
        if cls.QtClass.instance() is not None:
            return cls.QtClass.instance().property(cls.QtPropertyKey)
        return None

    @property
    def name(self):
        return self.qt.applicationName()

    @name.setter
    def name(self, value):
        self.qt.setApplicationName(value)

    @property
    def version(self):
        return self.qt.applicationVersion()

    @version.setter
    def version(self, value):
        self.qt.setApplicationVersion(value)

    @property
    def organization(self):
        return self.qt.organizationName()

    @organization.setter
    def organization(self, value):
        self.qt.setOrganizationName(value)

    @property
    def domain(self):
        return self.qt.organizationDomain()

    @domain.setter
    def domain(self, value):
        self.qt.setOrganizationDomain(value)

    def run(self):
        # Register interupt signal handler
        def signal_handler(signum, frame):
            if signum == signal.SIGINT:
                self.quit()
        signal.signal(signal.SIGINT, signal_handler)

        # Run timer to process interrupt signals
        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(250)

        return self.qt.exec_()

    def quit(self):
        self.qt.quit()

    @property
    def name_changed(self):
        return self.__name_changed

    @name_changed.setter
    def name_changed(self, value):
        self.__name_changed = value

    def __handle_name_changed(self):
        if callable(self.name_changed):
            self.name_changed(self.name)

    @property
    def version_changed(self):
        return self.__version_changed

    @version_changed.setter
    def version_changed(self, value):
        self.__version_changed = value

    def __handle_version_changed(self):
        if callable(self.version_changed):
            self.version_changed(self.version)

    @property
    def organization_changed(self):
        return self.__organization_changed

    @organization_changed.setter
    def organization_changed(self, value):
        self.__organization_changed = value

    def __handle_organization_changed(self):
        if callable(self.organization_changed):
            self.organization_changed(self.organization)

    @property
    def domain_changed(self):
        return self.__domain_changed

    @domain_changed.setter
    def domain_changed(self, value):
        self.__domain_changed = value

    def __handle_domain_changed(self):
        if callable(self.domain_changed):
            self.domain_changed(self.domain)

@bind(QtGui.QGuiApplication)
class GuiApplication(CoreApplication):

    def __init__(self, name=None, *, display_name=None, icon=None,
                 display_name_changed=None, last_window_closed=None, **kwargs):
        super().__init__(name=name, **kwargs)
        if display_name is not None:
            self.display_name = display_name
        if icon is not None:
            self.icon = icon
        self.display_name_changed = display_name_changed
        self.last_window_closed = last_window_closed
        # Connect signals
        self.qt.applicationDisplayNameChanged.connect(self.__handle_display_name_changed)
        self.qt.lastWindowClosed.connect(self.__handle_last_window_closed)

    @property
    def display_name(self):
        return self.qt.applicationDisplayName()

    @display_name.setter
    def display_name(self, value):
        self.qt.setApplicationDisplayName(value)

    @property
    def icon(self):
        icon = self.qt.windowIcon()
        if icon.isNull():
            return None
        return Icon(qt=icon)

    @icon.setter
    def icon(self, value):
        if value is None:
            self.qt.setWindowIcon(QtGui.QIcon())
        else:
            if not isinstance(value, Icon):
                value = Icon(value)
            self.qt.setWindowIcon(value.qt)

    @property
    def display_name_changed(self):
        return self.__display_name_changed

    @display_name_changed.setter
    def display_name_changed(self, value):
        self.__display_name_changed = value

    def __handle_display_name_changed(self):
        if callable(self.display_name_changed):
            self.display_name_changed(self.display_name)

    @property
    def last_window_closed(self):
        return self.__last_window_closed

    @last_window_closed.setter
    def last_window_closed(self, value):
        self.__last_window_closed = value

    def __handle_last_window_closed(self):
        if callable(self.last_window_closed):
            self.last_window_closed()

@bind(QtWidgets.QApplication)
class Application(GuiApplication):

    def __init__(self, name=None, *, focus_changed=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.focus_changed = focus_changed
        # Connect signals
        self.qt.focusChanged.connect(self.__handle_focus_changed)

    @property
    def focus_changed(self):
        return self.__focus_changed

    @focus_changed.setter
    def focus_changed(self, value):
        self.__focus_changed = value

    def __handle_focus_changed(self, old, now):
        if callable(self.focus_changed):
            self.focus_changed(old, now)

    def quit(self):
        """Request quit application by closing all windows."""
        self.qt.closeAllWindows()
