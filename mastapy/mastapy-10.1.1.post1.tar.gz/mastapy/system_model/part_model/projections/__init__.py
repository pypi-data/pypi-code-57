'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2024 import SpecifiedConcentricPartGroupDrawingOrder
    from ._2025 import SpecifiedParallelPartGroupDrawingOrder
