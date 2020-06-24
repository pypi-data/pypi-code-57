'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._318 import DIN3990GearSingleFlankRating
    from ._319 import DIN3990MeshSingleFlankRating
