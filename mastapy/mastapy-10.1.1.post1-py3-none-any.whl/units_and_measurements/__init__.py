'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._6502 import MeasurementType
    from ._6503 import MeasurementTypeExtensions
