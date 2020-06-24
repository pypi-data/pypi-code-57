'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._742 import KlingelnbergCycloPalloidHypoidGearDesign
    from ._743 import KlingelnbergCycloPalloidHypoidGearMeshDesign
    from ._744 import KlingelnbergCycloPalloidHypoidGearSetDesign
    from ._745 import KlingelnbergCycloPalloidHypoidMeshedGearDesign
