'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1264 import ScriptingSetup
    from ._1265 import UserDefinedPropertyKey
