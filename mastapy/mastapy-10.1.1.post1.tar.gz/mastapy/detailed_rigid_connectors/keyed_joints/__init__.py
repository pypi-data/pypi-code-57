'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1020 import KeyedJointDesign
    from ._1021 import KeyTypes
    from ._1022 import KeywayJointHalfDesign
    from ._1023 import NumberOfKeys
