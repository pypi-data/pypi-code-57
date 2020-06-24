'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1026 import AssemblyMethods
    from ._1027 import CalculationMethods
    from ._1028 import InterferenceFitDesign
    from ._1029 import InterferenceFitHalfDesign
    from ._1030 import StressRegions
    from ._1031 import Table4JointInterfaceTypes
