'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._652 import FaceGearLoadCase
    from ._653 import FaceGearSetLoadCase
    from ._654 import FaceMeshLoadCase
