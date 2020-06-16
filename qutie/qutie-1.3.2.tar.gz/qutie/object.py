from .qt import QtCore
from .qt import bind

from .base import Base

__all__ = ['Object']

@bind(QtCore.QObject)
class Object(Base):

    QtPropertyKey = '__qutie_ref'

    def __init__(self, *args, object_name=None, destroyed=None,
                 object_name_changed=None):
        super().__init__(*args)
        self.qt.setProperty(self.QtPropertyKey, self)
        if object_name is not None:
            self.object_name = object_name
        self.destroyed = destroyed
        self.object_name_changed = object_name_changed
        # Connect signals
        self.qt.destroyed.connect(self.__handle_destroyed)
        self.qt.objectNameChanged.connect(self.__handle_object_name_changed)
        self.qt.eventEmitted.connect(self.__handle_event)

    @property
    def object_name(self) -> str:
        return self.qt.objectName()

    @object_name.setter
    def object_name(self, value: str):
        self.qt.setObjectName(value)

    @property
    def destroyed(self) -> object:
        return self.__destroyed

    @destroyed.setter
    def destroyed(self, value: object):
        self.__destroyed = value

    def __handle_destroyed(self, obj: object):
        if callable(self.destroyed):
            self.destroyed(obj.property(self.QtPropertyKey))

    @property
    def object_name_changed(self) -> object:
        return self.__object_name_changed

    @object_name_changed.setter
    def object_name_changed(self, value: object):
        self.__object_name_changed = value

    def __handle_object_name_changed(self):
        if callable(self.object_name_changed):
            self.object_name_changed(self.object_name)

    def __handle_event(self, name, args, kwargs):
        if hasattr(self, name):
            attr = getattr(self, name)
            if callable(attr):
                attr(*args, **kwargs)

    def emit(self, _, *args, **kwargs):
        """Emit event."""
        self.qt.eventEmitted.emit(_, args, kwargs)
