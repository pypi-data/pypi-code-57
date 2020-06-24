'''_4967.py

AbstractShaftOrHousingMultiBodyDynamicsAnalysis
'''


from mastapy._internal import constructor
from mastapy.system_model.part_model import _1982, _2001
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _2022
from mastapy.system_model.analyses_and_results.mbd_analyses import _4992
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_OR_HOUSING_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'AbstractShaftOrHousingMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftOrHousingMultiBodyDynamicsAnalysis',)


class AbstractShaftOrHousingMultiBodyDynamicsAnalysis(_4992.ComponentMultiBodyDynamicsAnalysis):
    '''AbstractShaftOrHousingMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_OR_HOUSING_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftOrHousingMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def number_of_rigid_body_degrees_of_freedom(self) -> 'int':
        '''int: 'NumberOfRigidBodyDegreesOfFreedom' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfRigidBodyDegreesOfFreedom

    @property
    def component_design(self) -> '_1982.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1982.AbstractShaftOrHousing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_imported_fe_component(self) -> '_2001.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2001.ImportedFEComponent.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ImportedFEComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2001.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft(self) -> '_2022.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2022.Shaft.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Shaft. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2022.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
