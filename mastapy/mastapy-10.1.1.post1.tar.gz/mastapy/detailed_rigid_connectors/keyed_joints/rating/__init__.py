'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1024 import KeywayHalfRating
    from ._1025 import KeywayRating
