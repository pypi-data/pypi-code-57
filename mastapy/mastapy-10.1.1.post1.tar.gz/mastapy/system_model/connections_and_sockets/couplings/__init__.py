'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1894 import ClutchConnection
    from ._1895 import ClutchSocket
    from ._1896 import ConceptCouplingConnection
    from ._1897 import ConceptCouplingSocket
    from ._1898 import CouplingConnection
    from ._1899 import CouplingSocket
    from ._1900 import PartToPartShearCouplingConnection
    from ._1901 import PartToPartShearCouplingSocket
    from ._1902 import SpringDamperConnection
    from ._1903 import SpringDamperSocket
    from ._1904 import TorqueConverterConnection
    from ._1905 import TorqueConverterPumpSocket
    from ._1906 import TorqueConverterTurbineSocket
