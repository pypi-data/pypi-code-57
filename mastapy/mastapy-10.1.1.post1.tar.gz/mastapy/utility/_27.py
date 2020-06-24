'''_27.py

PushbulletSettings
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy.utility import _78
from mastapy._internal.python_net import python_net_import

_PUSHBULLET_SETTINGS = python_net_import('SMT.MastaAPI.Utility', 'PushbulletSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('PushbulletSettings',)


class PushbulletSettings(_78.PerMachineSettings):
    '''PushbulletSettings

    This is a mastapy class.
    '''

    TYPE = _PUSHBULLET_SETTINGS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PushbulletSettings.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def enable_pushbullet(self) -> 'bool':
        '''bool: 'EnablePushbullet' is the original name of this property.'''

        return self.wrapped.EnablePushbullet

    @enable_pushbullet.setter
    def enable_pushbullet(self, value: 'bool'):
        self.wrapped.EnablePushbullet = bool(value) if value else False

    @property
    def generate_pushbullet_token(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'GeneratePushbulletToken' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GeneratePushbulletToken

    @property
    def pushbullet_token(self) -> 'str':
        '''str: 'PushbulletToken' is the original name of this property.'''

        return self.wrapped.PushbulletToken

    @pushbullet_token.setter
    def pushbullet_token(self, value: 'str'):
        self.wrapped.PushbulletToken = str(value) if value else None

    @property
    def send_progress_screenshot_interval_minutes(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'SendProgressScreenshotIntervalMinutes' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.SendProgressScreenshotIntervalMinutes) if self.wrapped.SendProgressScreenshotIntervalMinutes else None

    @send_progress_screenshot_interval_minutes.setter
    def send_progress_screenshot_interval_minutes(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.TYPE
        enclosed_type = overridable.Overridable_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.SendProgressScreenshotIntervalMinutes = value
