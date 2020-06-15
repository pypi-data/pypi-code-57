from ika.magnetic_stirrer import *
import warnings


class CMAGHS7Interface(MagneticStirrer):
    def __init__(self,
                 device_port: str,
                 save_folder:Path = None,
                 datetime_format: str = datetimeManager._default_datetime_format,
                 ):
        super().__init__(device_port=device_port,
                         save_folder=save_folder,
                         datetime_format=datetime_format,
                         )
        warnings.warn(
            'use ika.magnetic_stirrer.MagneticStirrer instead',
            DeprecationWarning,
            stacklevel=2,
        )


class CMAGHS7InterfaceVisual(MagneticStirrerVisual):
    def __init__(self,
                 device_port: str,
                 save_folder:Path = None,
                 datetime_format: str = datetimeManager._default_datetime_format,
                 ):
        super().__init__(device_port=device_port,
                         save_folder=save_folder,
                         datetime_format=datetime_format,
                         )
        warnings.warn(
            'use ika.magnetic_stirrer.MagneticStirrerVisual instead',
            DeprecationWarning,
            stacklevel=2,
        )


class MockCMAGHS7Interface(MockMagneticStirrer):
    def __init__(self):
        super().__init__()
        warnings.warn(
            'use ika.magnetic_stirrer.MockMagneticStirrer instead',
            DeprecationWarning,
            stacklevel=2,
        )