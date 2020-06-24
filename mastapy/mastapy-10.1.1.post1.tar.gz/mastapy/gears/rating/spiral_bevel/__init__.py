'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._204 import SpiralBevelGearMeshRating
    from ._205 import SpiralBevelGearRating
    from ._206 import SpiralBevelGearSetRating
