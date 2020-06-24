'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2094 import BoostPressureInputOptions
    from ._2095 import InputPowerInputOptions
    from ._2096 import PressureRatioInputOptions
    from ._2097 import RotorSetDataInputFileOptions
    from ._2098 import RotorSetMeasuredPoint
    from ._2099 import RotorSpeedInputOptions
    from ._2100 import SuperchargerMap
    from ._2101 import SuperchargerMaps
    from ._2102 import SuperchargerRotorSet
    from ._2103 import SuperchargerRotorSetDatabase
    from ._2104 import YVariableForImportedData
