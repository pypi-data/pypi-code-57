'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._664 import BevelLoadCase
    from ._665 import BevelMeshLoadCase
    from ._666 import BevelSetLoadCase
