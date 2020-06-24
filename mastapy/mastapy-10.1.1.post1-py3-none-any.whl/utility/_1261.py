'''_1261.py

EnvironmentSummary
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.utility import _1270, _1260
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ENVIRONMENT_SUMMARY = python_net_import('SMT.MastaAPI.Utility', 'EnvironmentSummary')


__docformat__ = 'restructuredtext en'
__all__ = ('EnvironmentSummary',)


class EnvironmentSummary(_1.APIBase):
    '''EnvironmentSummary

    This is a mastapy class.
    '''

    TYPE = _ENVIRONMENT_SUMMARY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'EnvironmentSummary.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def entry_assembly(self) -> 'str':
        '''str: 'EntryAssembly' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EntryAssembly

    @property
    def user_name(self) -> 'str':
        '''str: 'UserName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.UserName

    @property
    def machine_name(self) -> 'str':
        '''str: 'MachineName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MachineName

    @property
    def operating_system(self) -> 'str':
        '''str: 'OperatingSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OperatingSystem

    @property
    def is_64_bit_operating_system(self) -> 'bool':
        '''bool: 'Is64BitOperatingSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Is64BitOperatingSystem

    @property
    def current_net_version(self) -> 'str':
        '''str: 'CurrentNETVersion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CurrentNETVersion

    @property
    def prerequisites(self) -> 'str':
        '''str: 'Prerequisites' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Prerequisites

    @property
    def processor(self) -> 'str':
        '''str: 'Processor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Processor

    @property
    def ram(self) -> 'str':
        '''str: 'RAM' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RAM

    @property
    def installed_video_controllers(self) -> 'str':
        '''str: 'InstalledVideoControllers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InstalledVideoControllers

    @property
    def open_gl_version(self) -> 'str':
        '''str: 'OpenGLVersion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OpenGLVersion

    @property
    def open_gl_vendor(self) -> 'str':
        '''str: 'OpenGLVendor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OpenGLVendor

    @property
    def open_gl_renderer(self) -> 'str':
        '''str: 'OpenGLRenderer' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OpenGLRenderer

    @property
    def current_culture_system_locale(self) -> 'str':
        '''str: 'CurrentCultureSystemLocale' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CurrentCultureSystemLocale

    @property
    def current_ui_culture_system_locale(self) -> 'str':
        '''str: 'CurrentUICultureSystemLocale' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CurrentUICultureSystemLocale

    @property
    def licence_key(self) -> 'str':
        '''str: 'LicenceKey' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LicenceKey

    @property
    def core_feature_code_in_use(self) -> 'str':
        '''str: 'CoreFeatureCodeInUse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CoreFeatureCodeInUse

    @property
    def core_feature_expiry(self) -> 'str':
        '''str: 'CoreFeatureExpiry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CoreFeatureExpiry

    @property
    def masta_version(self) -> 'str':
        '''str: 'MASTAVersion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MASTAVersion

    @property
    def build_date(self) -> 'str':
        '''str: 'BuildDate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BuildDate

    @property
    def build_date_and_age(self) -> 'str':
        '''str: 'BuildDateAndAge' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BuildDateAndAge

    @property
    def date_time_iso8601(self) -> 'str':
        '''str: 'DateTimeISO8601' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DateTimeISO8601

    @property
    def date_time_local_format(self) -> 'str':
        '''str: 'DateTimeLocalFormat' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DateTimeLocalFormat

    @property
    def start_date_time_and_age(self) -> 'str':
        '''str: 'StartDateTimeAndAge' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StartDateTimeAndAge

    @property
    def executable_directory(self) -> 'str':
        '''str: 'ExecutableDirectory' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExecutableDirectory

    @property
    def executable_directory_is_network_path(self) -> 'bool':
        '''bool: 'ExecutableDirectoryIsNetworkPath' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExecutableDirectoryIsNetworkPath

    @property
    def copy(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Copy' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Copy

    @property
    def dispatcher_information(self) -> 'str':
        '''str: 'DispatcherInformation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DispatcherInformation

    @property
    def current_culture(self) -> '_1270.NumberFormatInfoSummary':
        '''NumberFormatInfoSummary: 'CurrentCulture' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1270.NumberFormatInfoSummary)(self.wrapped.CurrentCulture) if self.wrapped.CurrentCulture else None

    @property
    def dispatchers(self) -> 'List[_1260.DispatcherHelper]':
        '''List[DispatcherHelper]: 'Dispatchers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Dispatchers, constructor.new(_1260.DispatcherHelper))
        return value
