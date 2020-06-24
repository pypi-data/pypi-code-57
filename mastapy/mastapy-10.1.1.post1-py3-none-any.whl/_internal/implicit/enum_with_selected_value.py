'''enum_with_selected_value.py

Implementations of 'EnumWithSelectedValue' in Python.
As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
'''


from enum import Enum
from typing import List

from mastapy._internal import (
    mixins, enum_with_selected_value_runtime, constructor, conversion
)
from mastapy.shafts import _33, _42
from mastapy._internal.python_net import python_net_import
from mastapy.materials import _68, _72, _57
from mastapy.gears import _139, _137, _140
from mastapy.math_utility import (
    _1072, _1061, _1060, _1071,
    _1070, _1068
)
from mastapy.gears.micro_geometry import (
    _360, _359, _358, _357
)
from mastapy.gears.manufacturing.cylindrical import (
    _408, _407, _411, _393
)
from mastapy.gears.manufacturing.cylindrical.plunge_shaving import _430, _429, _427
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _442
from mastapy.geometry.twod.curves import _115
from mastapy.gears.gear_designs.cylindrical import _828, _805, _821
from mastapy.gears.gear_designs.conical import _892, _891, _903
from mastapy.gears.gear_set_pareto_optimiser import _671
from mastapy.utility.model_validation import _1310, _1313
from mastapy.gears.ltca import _609
from mastapy.nodal_analysis import (
    _1390, _1377, _1394, _1383,
    _1362
)
from mastapy.gears.gear_designs.creation_options import _880
from mastapy.gears.gear_designs.bevel import _924, _913
from mastapy.bearings.tolerances import (
    _1539, _1549, _1533, _1534,
    _1532
)
from mastapy.detailed_rigid_connectors.splines import (
    _977, _1000, _986, _987,
    _995, _1001, _978
)
from mastapy.detailed_rigid_connectors.interference_fits import _1031
from mastapy.utility import _1129
from mastapy.utility.report import _1270
from mastapy.nodal_analysis.varying_input_components import _1401
from mastapy.bearings import (
    _1523, _1516, _1524, _1527,
    _1504, _1505, _1529, _1511
)
from mastapy.system_model.part_model import _2016
from mastapy.system_model.imported_fes import (
    _1956, _1918, _1948, _1972
)
from mastapy.system_model import (
    _1796, _1807, _1803, _1805
)
from mastapy.utility.enums import _1337
from mastapy.nodal_analysis.fe_export_utility import _1449, _1450
from mastapy.bearings.bearing_results import _1582, _1584, _1583
from mastapy.system_model.part_model.couplings import _2129, _2125, _2128
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3510
from mastapy.system_model.analyses_and_results.static_loads import (
    _6052, _6203, _6132, _6125,
    _6165, _6204
)
from mastapy.system_model.analyses_and_results.mbd_analyses import (
    _4974, _5021, _5066, _5091
)
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5323
from mastapy.bearings.bearing_results.rolling.iso_rating_results import _1718
from mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition import _6218

_ENUM_WITH_SELECTED_VALUE = python_net_import('SMT.MastaAPI.Utility.Property', 'EnumWithSelectedValue')


__docformat__ = 'restructuredtext en'
__all__ = (
    'EnumWithSelectedValue_ShaftRatingMethod', 'EnumWithSelectedValue_SurfaceFinishes',
    'EnumWithSelectedValue_LubricantDefinition', 'EnumWithSelectedValue_LubricantViscosityClassISO',
    'EnumWithSelectedValue_MicroGeometryModel', 'EnumWithSelectedValue_ExtrapolationOptions',
    'EnumWithSelectedValue_CylindricalGearRatingMethods', 'EnumWithSelectedValue_LocationOfTipReliefEvaluation',
    'EnumWithSelectedValue_LocationOfRootReliefEvaluation', 'EnumWithSelectedValue_LocationOfEvaluationUpperLimit',
    'EnumWithSelectedValue_LocationOfEvaluationLowerLimit', 'EnumWithSelectedValue_CylindricalMftRoughingMethods',
    'EnumWithSelectedValue_CylindricalMftFinishingMethods', 'EnumWithSelectedValue_MicroGeometryDefinitionType',
    'EnumWithSelectedValue_MicroGeometryDefinitionMethod', 'EnumWithSelectedValue_ChartType',
    'EnumWithSelectedValue_Flank', 'EnumWithSelectedValue_ActiveProcessMethod',
    'EnumWithSelectedValue_CutterFlankSections', 'EnumWithSelectedValue_BasicCurveTypes',
    'EnumWithSelectedValue_ThicknessType', 'EnumWithSelectedValue_ConicalManufactureMethods',
    'EnumWithSelectedValue_ConicalMachineSettingCalculationMethods', 'EnumWithSelectedValue_CandidateDisplayChoice',
    'EnumWithSelectedValue_Severity', 'EnumWithSelectedValue_GeometrySpecificationType',
    'EnumWithSelectedValue_StatusItemSeverity', 'EnumWithSelectedValue_LubricationMethods',
    'EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod', 'EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods',
    'EnumWithSelectedValue_ContactResultType', 'EnumWithSelectedValue_StressResultsType',
    'EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption', 'EnumWithSelectedValue_ToothThicknessSpecificationMethod',
    'EnumWithSelectedValue_LoadDistributionFactorMethods', 'EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods',
    'EnumWithSelectedValue_ITDesignation', 'EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption',
    'EnumWithSelectedValue_SplineRatingTypes', 'EnumWithSelectedValue_Modules',
    'EnumWithSelectedValue_PressureAngleTypes', 'EnumWithSelectedValue_SplineFitClassType',
    'EnumWithSelectedValue_SplineToleranceClassTypes', 'EnumWithSelectedValue_Table4JointInterfaceTypes',
    'EnumWithSelectedValue_ExecutableDirectoryCopier_Option', 'EnumWithSelectedValue_CadPageOrientation',
    'EnumWithSelectedValue_IntegrationMethod', 'EnumWithSelectedValue_ValueInputOption',
    'EnumWithSelectedValue_SinglePointSelectionMethod', 'EnumWithSelectedValue_ModeInputType',
    'EnumWithSelectedValue_RollerBearingProfileTypes', 'EnumWithSelectedValue_FluidFilmTemperatureOptions',
    'EnumWithSelectedValue_SupportToleranceLocationDesignation', 'EnumWithSelectedValue_RollingBearingArrangement',
    'EnumWithSelectedValue_RollingBearingRaceType', 'EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod',
    'EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod', 'EnumWithSelectedValue_RotationalDirections',
    'EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing', 'EnumWithSelectedValue_LinkNodeSource',
    'EnumWithSelectedValue_ComponentOrientationOption', 'EnumWithSelectedValue_Axis',
    'EnumWithSelectedValue_AlignmentAxis', 'EnumWithSelectedValue_DesignEntityId',
    'EnumWithSelectedValue_ImportedFEType', 'EnumWithSelectedValue_ThermalExpansionOption',
    'EnumWithSelectedValue_ThreeDViewContourOption', 'EnumWithSelectedValue_BoundaryConditionType',
    'EnumWithSelectedValue_FEExportFormat', 'EnumWithSelectedValue_BearingToleranceClass',
    'EnumWithSelectedValue_BearingModel', 'EnumWithSelectedValue_PreloadType',
    'EnumWithSelectedValue_RaceRadialMountingType', 'EnumWithSelectedValue_RaceAxialMountingType',
    'EnumWithSelectedValue_BearingToleranceDefinitionOptions', 'EnumWithSelectedValue_InternalClearanceClass',
    'EnumWithSelectedValue_PowerLoadType', 'EnumWithSelectedValue_RigidConnectorTypes',
    'EnumWithSelectedValue_RigidConnectorStiffnessType', 'EnumWithSelectedValue_FitTypes',
    'EnumWithSelectedValue_RigidConnectorToothSpacingType', 'EnumWithSelectedValue_DoeValueSpecificationOption',
    'EnumWithSelectedValue_AnalysisType', 'EnumWithSelectedValue_BarModelExportType',
    'EnumWithSelectedValue_DynamicsResponseType', 'EnumWithSelectedValue_DynamicsResponseScaling',
    'EnumWithSelectedValue_BearingStiffnessModel', 'EnumWithSelectedValue_GearMeshStiffnessModel',
    'EnumWithSelectedValue_ShaftAndHousingFlexibilityOption', 'EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ExportOutputType',
    'EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ComplexNumberOutput', 'EnumWithSelectedValue_StressConcentrationMethod',
    'EnumWithSelectedValue_MeshStiffnessModel', 'EnumWithSelectedValue_TorqueRippleInputType',
    'EnumWithSelectedValue_HarmonicLoadDataType', 'EnumWithSelectedValue_HarmonicExcitationType',
    'EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification', 'EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod',
    'EnumWithSelectedValue_TorqueSpecificationForSystemDeflection', 'EnumWithSelectedValue_TorqueConverterLockupRule',
    'EnumWithSelectedValue_DegreesOfFreedom', 'EnumWithSelectedValue_DestinationDesignState'
)


class EnumWithSelectedValue_ShaftRatingMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ShaftRatingMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ShaftRatingMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'ShaftRatingMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_33.ShaftRatingMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _33.ShaftRatingMethod

    @classmethod
    def implicit_type(cls) -> '_33.ShaftRatingMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _33.ShaftRatingMethod.type_()

    @property
    def selected_value(self) -> '_33.ShaftRatingMethod':
        '''ShaftRatingMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_33.ShaftRatingMethod]':
        '''List[ShaftRatingMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SurfaceFinishes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SurfaceFinishes

    A specific implementation of 'EnumWithSelectedValue' for 'SurfaceFinishes' types.
    '''

    __hash__ = None
    __qualname__ = 'SurfaceFinishes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_42.SurfaceFinishes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _42.SurfaceFinishes

    @classmethod
    def implicit_type(cls) -> '_42.SurfaceFinishes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _42.SurfaceFinishes.type_()

    @property
    def selected_value(self) -> '_42.SurfaceFinishes':
        '''SurfaceFinishes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_42.SurfaceFinishes]':
        '''List[SurfaceFinishes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LubricantDefinition(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LubricantDefinition

    A specific implementation of 'EnumWithSelectedValue' for 'LubricantDefinition' types.
    '''

    __hash__ = None
    __qualname__ = 'LubricantDefinition'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_68.LubricantDefinition':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _68.LubricantDefinition

    @classmethod
    def implicit_type(cls) -> '_68.LubricantDefinition.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _68.LubricantDefinition.type_()

    @property
    def selected_value(self) -> '_68.LubricantDefinition':
        '''LubricantDefinition: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_68.LubricantDefinition]':
        '''List[LubricantDefinition]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LubricantViscosityClassISO(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LubricantViscosityClassISO

    A specific implementation of 'EnumWithSelectedValue' for 'LubricantViscosityClassISO' types.
    '''

    __hash__ = None
    __qualname__ = 'LubricantViscosityClassISO'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_72.LubricantViscosityClassISO':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _72.LubricantViscosityClassISO

    @classmethod
    def implicit_type(cls) -> '_72.LubricantViscosityClassISO.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _72.LubricantViscosityClassISO.type_()

    @property
    def selected_value(self) -> '_72.LubricantViscosityClassISO':
        '''LubricantViscosityClassISO: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_72.LubricantViscosityClassISO]':
        '''List[LubricantViscosityClassISO]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_MicroGeometryModel(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_MicroGeometryModel

    A specific implementation of 'EnumWithSelectedValue' for 'MicroGeometryModel' types.
    '''

    __hash__ = None
    __qualname__ = 'MicroGeometryModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_139.MicroGeometryModel':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _139.MicroGeometryModel

    @classmethod
    def implicit_type(cls) -> '_139.MicroGeometryModel.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _139.MicroGeometryModel.type_()

    @property
    def selected_value(self) -> '_139.MicroGeometryModel':
        '''MicroGeometryModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_139.MicroGeometryModel]':
        '''List[MicroGeometryModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ExtrapolationOptions(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ExtrapolationOptions

    A specific implementation of 'EnumWithSelectedValue' for 'ExtrapolationOptions' types.
    '''

    __hash__ = None
    __qualname__ = 'ExtrapolationOptions'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1072.ExtrapolationOptions':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1072.ExtrapolationOptions

    @classmethod
    def implicit_type(cls) -> '_1072.ExtrapolationOptions.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1072.ExtrapolationOptions.type_()

    @property
    def selected_value(self) -> '_1072.ExtrapolationOptions':
        '''ExtrapolationOptions: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1072.ExtrapolationOptions]':
        '''List[ExtrapolationOptions]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CylindricalGearRatingMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CylindricalGearRatingMethods

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalGearRatingMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearRatingMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_57.CylindricalGearRatingMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _57.CylindricalGearRatingMethods

    @classmethod
    def implicit_type(cls) -> '_57.CylindricalGearRatingMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _57.CylindricalGearRatingMethods.type_()

    @property
    def selected_value(self) -> '_57.CylindricalGearRatingMethods':
        '''CylindricalGearRatingMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_57.CylindricalGearRatingMethods]':
        '''List[CylindricalGearRatingMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LocationOfTipReliefEvaluation(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LocationOfTipReliefEvaluation

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfTipReliefEvaluation' types.
    '''

    __hash__ = None
    __qualname__ = 'LocationOfTipReliefEvaluation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_360.LocationOfTipReliefEvaluation':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _360.LocationOfTipReliefEvaluation

    @classmethod
    def implicit_type(cls) -> '_360.LocationOfTipReliefEvaluation.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _360.LocationOfTipReliefEvaluation.type_()

    @property
    def selected_value(self) -> '_360.LocationOfTipReliefEvaluation':
        '''LocationOfTipReliefEvaluation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_360.LocationOfTipReliefEvaluation]':
        '''List[LocationOfTipReliefEvaluation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LocationOfRootReliefEvaluation(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LocationOfRootReliefEvaluation

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfRootReliefEvaluation' types.
    '''

    __hash__ = None
    __qualname__ = 'LocationOfRootReliefEvaluation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_359.LocationOfRootReliefEvaluation':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _359.LocationOfRootReliefEvaluation

    @classmethod
    def implicit_type(cls) -> '_359.LocationOfRootReliefEvaluation.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _359.LocationOfRootReliefEvaluation.type_()

    @property
    def selected_value(self) -> '_359.LocationOfRootReliefEvaluation':
        '''LocationOfRootReliefEvaluation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_359.LocationOfRootReliefEvaluation]':
        '''List[LocationOfRootReliefEvaluation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LocationOfEvaluationUpperLimit(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LocationOfEvaluationUpperLimit

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfEvaluationUpperLimit' types.
    '''

    __hash__ = None
    __qualname__ = 'LocationOfEvaluationUpperLimit'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_358.LocationOfEvaluationUpperLimit':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _358.LocationOfEvaluationUpperLimit

    @classmethod
    def implicit_type(cls) -> '_358.LocationOfEvaluationUpperLimit.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _358.LocationOfEvaluationUpperLimit.type_()

    @property
    def selected_value(self) -> '_358.LocationOfEvaluationUpperLimit':
        '''LocationOfEvaluationUpperLimit: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_358.LocationOfEvaluationUpperLimit]':
        '''List[LocationOfEvaluationUpperLimit]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LocationOfEvaluationLowerLimit(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LocationOfEvaluationLowerLimit

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfEvaluationLowerLimit' types.
    '''

    __hash__ = None
    __qualname__ = 'LocationOfEvaluationLowerLimit'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_357.LocationOfEvaluationLowerLimit':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _357.LocationOfEvaluationLowerLimit

    @classmethod
    def implicit_type(cls) -> '_357.LocationOfEvaluationLowerLimit.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _357.LocationOfEvaluationLowerLimit.type_()

    @property
    def selected_value(self) -> '_357.LocationOfEvaluationLowerLimit':
        '''LocationOfEvaluationLowerLimit: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_357.LocationOfEvaluationLowerLimit]':
        '''List[LocationOfEvaluationLowerLimit]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CylindricalMftRoughingMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CylindricalMftRoughingMethods

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalMftRoughingMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalMftRoughingMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_408.CylindricalMftRoughingMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _408.CylindricalMftRoughingMethods

    @classmethod
    def implicit_type(cls) -> '_408.CylindricalMftRoughingMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _408.CylindricalMftRoughingMethods.type_()

    @property
    def selected_value(self) -> '_408.CylindricalMftRoughingMethods':
        '''CylindricalMftRoughingMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_408.CylindricalMftRoughingMethods]':
        '''List[CylindricalMftRoughingMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CylindricalMftFinishingMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CylindricalMftFinishingMethods

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalMftFinishingMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalMftFinishingMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_407.CylindricalMftFinishingMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _407.CylindricalMftFinishingMethods

    @classmethod
    def implicit_type(cls) -> '_407.CylindricalMftFinishingMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _407.CylindricalMftFinishingMethods.type_()

    @property
    def selected_value(self) -> '_407.CylindricalMftFinishingMethods':
        '''CylindricalMftFinishingMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_407.CylindricalMftFinishingMethods]':
        '''List[CylindricalMftFinishingMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_MicroGeometryDefinitionType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_MicroGeometryDefinitionType

    A specific implementation of 'EnumWithSelectedValue' for 'MicroGeometryDefinitionType' types.
    '''

    __hash__ = None
    __qualname__ = 'MicroGeometryDefinitionType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_430.MicroGeometryDefinitionType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _430.MicroGeometryDefinitionType

    @classmethod
    def implicit_type(cls) -> '_430.MicroGeometryDefinitionType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _430.MicroGeometryDefinitionType.type_()

    @property
    def selected_value(self) -> '_430.MicroGeometryDefinitionType':
        '''MicroGeometryDefinitionType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_430.MicroGeometryDefinitionType]':
        '''List[MicroGeometryDefinitionType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_MicroGeometryDefinitionMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_MicroGeometryDefinitionMethod

    A specific implementation of 'EnumWithSelectedValue' for 'MicroGeometryDefinitionMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'MicroGeometryDefinitionMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_429.MicroGeometryDefinitionMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _429.MicroGeometryDefinitionMethod

    @classmethod
    def implicit_type(cls) -> '_429.MicroGeometryDefinitionMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _429.MicroGeometryDefinitionMethod.type_()

    @property
    def selected_value(self) -> '_429.MicroGeometryDefinitionMethod':
        '''MicroGeometryDefinitionMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_429.MicroGeometryDefinitionMethod]':
        '''List[MicroGeometryDefinitionMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ChartType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ChartType

    A specific implementation of 'EnumWithSelectedValue' for 'ChartType' types.
    '''

    __hash__ = None
    __qualname__ = 'ChartType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_427.ChartType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _427.ChartType

    @classmethod
    def implicit_type(cls) -> '_427.ChartType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _427.ChartType.type_()

    @property
    def selected_value(self) -> '_427.ChartType':
        '''ChartType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_427.ChartType]':
        '''List[ChartType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_Flank(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_Flank

    A specific implementation of 'EnumWithSelectedValue' for 'Flank' types.
    '''

    __hash__ = None
    __qualname__ = 'Flank'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_411.Flank':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _411.Flank

    @classmethod
    def implicit_type(cls) -> '_411.Flank.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _411.Flank.type_()

    @property
    def selected_value(self) -> '_411.Flank':
        '''Flank: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_411.Flank]':
        '''List[Flank]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ActiveProcessMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ActiveProcessMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ActiveProcessMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'ActiveProcessMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_442.ActiveProcessMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _442.ActiveProcessMethod

    @classmethod
    def implicit_type(cls) -> '_442.ActiveProcessMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _442.ActiveProcessMethod.type_()

    @property
    def selected_value(self) -> '_442.ActiveProcessMethod':
        '''ActiveProcessMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_442.ActiveProcessMethod]':
        '''List[ActiveProcessMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CutterFlankSections(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CutterFlankSections

    A specific implementation of 'EnumWithSelectedValue' for 'CutterFlankSections' types.
    '''

    __hash__ = None
    __qualname__ = 'CutterFlankSections'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_393.CutterFlankSections':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _393.CutterFlankSections

    @classmethod
    def implicit_type(cls) -> '_393.CutterFlankSections.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _393.CutterFlankSections.type_()

    @property
    def selected_value(self) -> '_393.CutterFlankSections':
        '''CutterFlankSections: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_393.CutterFlankSections]':
        '''List[CutterFlankSections]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BasicCurveTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BasicCurveTypes

    A specific implementation of 'EnumWithSelectedValue' for 'BasicCurveTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'BasicCurveTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_115.BasicCurveTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _115.BasicCurveTypes

    @classmethod
    def implicit_type(cls) -> '_115.BasicCurveTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _115.BasicCurveTypes.type_()

    @property
    def selected_value(self) -> '_115.BasicCurveTypes':
        '''BasicCurveTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_115.BasicCurveTypes]':
        '''List[BasicCurveTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ThicknessType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ThicknessType

    A specific implementation of 'EnumWithSelectedValue' for 'ThicknessType' types.
    '''

    __hash__ = None
    __qualname__ = 'ThicknessType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_828.ThicknessType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _828.ThicknessType

    @classmethod
    def implicit_type(cls) -> '_828.ThicknessType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _828.ThicknessType.type_()

    @property
    def selected_value(self) -> '_828.ThicknessType':
        '''ThicknessType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_828.ThicknessType]':
        '''List[ThicknessType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ConicalManufactureMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ConicalManufactureMethods

    A specific implementation of 'EnumWithSelectedValue' for 'ConicalManufactureMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'ConicalManufactureMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_892.ConicalManufactureMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _892.ConicalManufactureMethods

    @classmethod
    def implicit_type(cls) -> '_892.ConicalManufactureMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _892.ConicalManufactureMethods.type_()

    @property
    def selected_value(self) -> '_892.ConicalManufactureMethods':
        '''ConicalManufactureMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_892.ConicalManufactureMethods]':
        '''List[ConicalManufactureMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ConicalMachineSettingCalculationMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ConicalMachineSettingCalculationMethods

    A specific implementation of 'EnumWithSelectedValue' for 'ConicalMachineSettingCalculationMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'ConicalMachineSettingCalculationMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_891.ConicalMachineSettingCalculationMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _891.ConicalMachineSettingCalculationMethods

    @classmethod
    def implicit_type(cls) -> '_891.ConicalMachineSettingCalculationMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _891.ConicalMachineSettingCalculationMethods.type_()

    @property
    def selected_value(self) -> '_891.ConicalMachineSettingCalculationMethods':
        '''ConicalMachineSettingCalculationMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_891.ConicalMachineSettingCalculationMethods]':
        '''List[ConicalMachineSettingCalculationMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CandidateDisplayChoice(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CandidateDisplayChoice

    A specific implementation of 'EnumWithSelectedValue' for 'CandidateDisplayChoice' types.
    '''

    __hash__ = None
    __qualname__ = 'CandidateDisplayChoice'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_671.CandidateDisplayChoice':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _671.CandidateDisplayChoice

    @classmethod
    def implicit_type(cls) -> '_671.CandidateDisplayChoice.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _671.CandidateDisplayChoice.type_()

    @property
    def selected_value(self) -> '_671.CandidateDisplayChoice':
        '''CandidateDisplayChoice: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_671.CandidateDisplayChoice]':
        '''List[CandidateDisplayChoice]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_Severity(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_Severity

    A specific implementation of 'EnumWithSelectedValue' for 'Severity' types.
    '''

    __hash__ = None
    __qualname__ = 'Severity'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1310.Severity':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1310.Severity

    @classmethod
    def implicit_type(cls) -> '_1310.Severity.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1310.Severity.type_()

    @property
    def selected_value(self) -> '_1310.Severity':
        '''Severity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1310.Severity]':
        '''List[Severity]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_GeometrySpecificationType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_GeometrySpecificationType

    A specific implementation of 'EnumWithSelectedValue' for 'GeometrySpecificationType' types.
    '''

    __hash__ = None
    __qualname__ = 'GeometrySpecificationType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_805.GeometrySpecificationType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _805.GeometrySpecificationType

    @classmethod
    def implicit_type(cls) -> '_805.GeometrySpecificationType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _805.GeometrySpecificationType.type_()

    @property
    def selected_value(self) -> '_805.GeometrySpecificationType':
        '''GeometrySpecificationType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_805.GeometrySpecificationType]':
        '''List[GeometrySpecificationType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_StatusItemSeverity(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_StatusItemSeverity

    A specific implementation of 'EnumWithSelectedValue' for 'StatusItemSeverity' types.
    '''

    __hash__ = None
    __qualname__ = 'StatusItemSeverity'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1313.StatusItemSeverity':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1313.StatusItemSeverity

    @classmethod
    def implicit_type(cls) -> '_1313.StatusItemSeverity.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1313.StatusItemSeverity.type_()

    @property
    def selected_value(self) -> '_1313.StatusItemSeverity':
        '''StatusItemSeverity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1313.StatusItemSeverity]':
        '''List[StatusItemSeverity]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LubricationMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LubricationMethods

    A specific implementation of 'EnumWithSelectedValue' for 'LubricationMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'LubricationMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_137.LubricationMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _137.LubricationMethods

    @classmethod
    def implicit_type(cls) -> '_137.LubricationMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _137.LubricationMethods.type_()

    @property
    def selected_value(self) -> '_137.LubricationMethods':
        '''LubricationMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_137.LubricationMethods]':
        '''List[LubricationMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'MicropittingCoefficientOfFrictionCalculationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'MicropittingCoefficientOfFrictionCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_140.MicropittingCoefficientOfFrictionCalculationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _140.MicropittingCoefficientOfFrictionCalculationMethod

    @classmethod
    def implicit_type(cls) -> '_140.MicropittingCoefficientOfFrictionCalculationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _140.MicropittingCoefficientOfFrictionCalculationMethod.type_()

    @property
    def selected_value(self) -> '_140.MicropittingCoefficientOfFrictionCalculationMethod':
        '''MicropittingCoefficientOfFrictionCalculationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_140.MicropittingCoefficientOfFrictionCalculationMethod]':
        '''List[MicropittingCoefficientOfFrictionCalculationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods

    A specific implementation of 'EnumWithSelectedValue' for 'ScuffingCoefficientOfFrictionMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'ScuffingCoefficientOfFrictionMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_821.ScuffingCoefficientOfFrictionMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _821.ScuffingCoefficientOfFrictionMethods

    @classmethod
    def implicit_type(cls) -> '_821.ScuffingCoefficientOfFrictionMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _821.ScuffingCoefficientOfFrictionMethods.type_()

    @property
    def selected_value(self) -> '_821.ScuffingCoefficientOfFrictionMethods':
        '''ScuffingCoefficientOfFrictionMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_821.ScuffingCoefficientOfFrictionMethods]':
        '''List[ScuffingCoefficientOfFrictionMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ContactResultType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ContactResultType

    A specific implementation of 'EnumWithSelectedValue' for 'ContactResultType' types.
    '''

    __hash__ = None
    __qualname__ = 'ContactResultType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_609.ContactResultType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _609.ContactResultType

    @classmethod
    def implicit_type(cls) -> '_609.ContactResultType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _609.ContactResultType.type_()

    @property
    def selected_value(self) -> '_609.ContactResultType':
        '''ContactResultType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_609.ContactResultType]':
        '''List[ContactResultType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_StressResultsType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_StressResultsType

    A specific implementation of 'EnumWithSelectedValue' for 'StressResultsType' types.
    '''

    __hash__ = None
    __qualname__ = 'StressResultsType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1390.StressResultsType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1390.StressResultsType

    @classmethod
    def implicit_type(cls) -> '_1390.StressResultsType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1390.StressResultsType.type_()

    @property
    def selected_value(self) -> '_1390.StressResultsType':
        '''StressResultsType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1390.StressResultsType]':
        '''List[StressResultsType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalGearPairCreationOptions.DerivedParameterOption' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearPairCreationOptions.DerivedParameterOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_880.CylindricalGearPairCreationOptions.DerivedParameterOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _880.CylindricalGearPairCreationOptions.DerivedParameterOption

    @classmethod
    def implicit_type(cls) -> '_880.CylindricalGearPairCreationOptions.DerivedParameterOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _880.CylindricalGearPairCreationOptions.DerivedParameterOption.type_()

    @property
    def selected_value(self) -> '_880.CylindricalGearPairCreationOptions.DerivedParameterOption':
        '''CylindricalGearPairCreationOptions.DerivedParameterOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_880.CylindricalGearPairCreationOptions.DerivedParameterOption]':
        '''List[CylindricalGearPairCreationOptions.DerivedParameterOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ToothThicknessSpecificationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ToothThicknessSpecificationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ToothThicknessSpecificationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'ToothThicknessSpecificationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_924.ToothThicknessSpecificationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _924.ToothThicknessSpecificationMethod

    @classmethod
    def implicit_type(cls) -> '_924.ToothThicknessSpecificationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _924.ToothThicknessSpecificationMethod.type_()

    @property
    def selected_value(self) -> '_924.ToothThicknessSpecificationMethod':
        '''ToothThicknessSpecificationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_924.ToothThicknessSpecificationMethod]':
        '''List[ToothThicknessSpecificationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LoadDistributionFactorMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LoadDistributionFactorMethods

    A specific implementation of 'EnumWithSelectedValue' for 'LoadDistributionFactorMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'LoadDistributionFactorMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_903.LoadDistributionFactorMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _903.LoadDistributionFactorMethods

    @classmethod
    def implicit_type(cls) -> '_903.LoadDistributionFactorMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _903.LoadDistributionFactorMethods.type_()

    @property
    def selected_value(self) -> '_903.LoadDistributionFactorMethods':
        '''LoadDistributionFactorMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_903.LoadDistributionFactorMethods]':
        '''List[LoadDistributionFactorMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods

    A specific implementation of 'EnumWithSelectedValue' for 'AGMAGleasonConicalGearGeometryMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'AGMAGleasonConicalGearGeometryMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_913.AGMAGleasonConicalGearGeometryMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _913.AGMAGleasonConicalGearGeometryMethods

    @classmethod
    def implicit_type(cls) -> '_913.AGMAGleasonConicalGearGeometryMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _913.AGMAGleasonConicalGearGeometryMethods.type_()

    @property
    def selected_value(self) -> '_913.AGMAGleasonConicalGearGeometryMethods':
        '''AGMAGleasonConicalGearGeometryMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_913.AGMAGleasonConicalGearGeometryMethods]':
        '''List[AGMAGleasonConicalGearGeometryMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ITDesignation(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ITDesignation

    A specific implementation of 'EnumWithSelectedValue' for 'ITDesignation' types.
    '''

    __hash__ = None
    __qualname__ = 'ITDesignation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1539.ITDesignation':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1539.ITDesignation

    @classmethod
    def implicit_type(cls) -> '_1539.ITDesignation.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1539.ITDesignation.type_()

    @property
    def selected_value(self) -> '_1539.ITDesignation':
        '''ITDesignation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1539.ITDesignation]':
        '''List[ITDesignation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption

    A specific implementation of 'EnumWithSelectedValue' for 'DudleyEffectiveLengthApproximationOption' types.
    '''

    __hash__ = None
    __qualname__ = 'DudleyEffectiveLengthApproximationOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_977.DudleyEffectiveLengthApproximationOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _977.DudleyEffectiveLengthApproximationOption

    @classmethod
    def implicit_type(cls) -> '_977.DudleyEffectiveLengthApproximationOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _977.DudleyEffectiveLengthApproximationOption.type_()

    @property
    def selected_value(self) -> '_977.DudleyEffectiveLengthApproximationOption':
        '''DudleyEffectiveLengthApproximationOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_977.DudleyEffectiveLengthApproximationOption]':
        '''List[DudleyEffectiveLengthApproximationOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SplineRatingTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SplineRatingTypes

    A specific implementation of 'EnumWithSelectedValue' for 'SplineRatingTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'SplineRatingTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1000.SplineRatingTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1000.SplineRatingTypes

    @classmethod
    def implicit_type(cls) -> '_1000.SplineRatingTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1000.SplineRatingTypes.type_()

    @property
    def selected_value(self) -> '_1000.SplineRatingTypes':
        '''SplineRatingTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1000.SplineRatingTypes]':
        '''List[SplineRatingTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_Modules(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_Modules

    A specific implementation of 'EnumWithSelectedValue' for 'Modules' types.
    '''

    __hash__ = None
    __qualname__ = 'Modules'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_986.Modules':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _986.Modules

    @classmethod
    def implicit_type(cls) -> '_986.Modules.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _986.Modules.type_()

    @property
    def selected_value(self) -> '_986.Modules':
        '''Modules: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_986.Modules]':
        '''List[Modules]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_PressureAngleTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_PressureAngleTypes

    A specific implementation of 'EnumWithSelectedValue' for 'PressureAngleTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'PressureAngleTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_987.PressureAngleTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _987.PressureAngleTypes

    @classmethod
    def implicit_type(cls) -> '_987.PressureAngleTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _987.PressureAngleTypes.type_()

    @property
    def selected_value(self) -> '_987.PressureAngleTypes':
        '''PressureAngleTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_987.PressureAngleTypes]':
        '''List[PressureAngleTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SplineFitClassType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SplineFitClassType

    A specific implementation of 'EnumWithSelectedValue' for 'SplineFitClassType' types.
    '''

    __hash__ = None
    __qualname__ = 'SplineFitClassType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_995.SplineFitClassType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _995.SplineFitClassType

    @classmethod
    def implicit_type(cls) -> '_995.SplineFitClassType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _995.SplineFitClassType.type_()

    @property
    def selected_value(self) -> '_995.SplineFitClassType':
        '''SplineFitClassType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_995.SplineFitClassType]':
        '''List[SplineFitClassType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SplineToleranceClassTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SplineToleranceClassTypes

    A specific implementation of 'EnumWithSelectedValue' for 'SplineToleranceClassTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'SplineToleranceClassTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1001.SplineToleranceClassTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1001.SplineToleranceClassTypes

    @classmethod
    def implicit_type(cls) -> '_1001.SplineToleranceClassTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1001.SplineToleranceClassTypes.type_()

    @property
    def selected_value(self) -> '_1001.SplineToleranceClassTypes':
        '''SplineToleranceClassTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1001.SplineToleranceClassTypes]':
        '''List[SplineToleranceClassTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_Table4JointInterfaceTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_Table4JointInterfaceTypes

    A specific implementation of 'EnumWithSelectedValue' for 'Table4JointInterfaceTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'Table4JointInterfaceTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1031.Table4JointInterfaceTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1031.Table4JointInterfaceTypes

    @classmethod
    def implicit_type(cls) -> '_1031.Table4JointInterfaceTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1031.Table4JointInterfaceTypes.type_()

    @property
    def selected_value(self) -> '_1031.Table4JointInterfaceTypes':
        '''Table4JointInterfaceTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1031.Table4JointInterfaceTypes]':
        '''List[Table4JointInterfaceTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ExecutableDirectoryCopier_Option(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ExecutableDirectoryCopier_Option

    A specific implementation of 'EnumWithSelectedValue' for 'ExecutableDirectoryCopier.Option' types.
    '''

    __hash__ = None
    __qualname__ = 'ExecutableDirectoryCopier.Option'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1129.ExecutableDirectoryCopier.Option':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1129.ExecutableDirectoryCopier.Option

    @classmethod
    def implicit_type(cls) -> '_1129.ExecutableDirectoryCopier.Option.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1129.ExecutableDirectoryCopier.Option.type_()

    @property
    def selected_value(self) -> '_1129.ExecutableDirectoryCopier.Option':
        '''ExecutableDirectoryCopier.Option: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1129.ExecutableDirectoryCopier.Option]':
        '''List[ExecutableDirectoryCopier.Option]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CadPageOrientation(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CadPageOrientation

    A specific implementation of 'EnumWithSelectedValue' for 'CadPageOrientation' types.
    '''

    __hash__ = None
    __qualname__ = 'CadPageOrientation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1270.CadPageOrientation':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1270.CadPageOrientation

    @classmethod
    def implicit_type(cls) -> '_1270.CadPageOrientation.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1270.CadPageOrientation.type_()

    @property
    def selected_value(self) -> '_1270.CadPageOrientation':
        '''CadPageOrientation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1270.CadPageOrientation]':
        '''List[CadPageOrientation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_IntegrationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_IntegrationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'IntegrationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'IntegrationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1377.IntegrationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1377.IntegrationMethod

    @classmethod
    def implicit_type(cls) -> '_1377.IntegrationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1377.IntegrationMethod.type_()

    @property
    def selected_value(self) -> '_1377.IntegrationMethod':
        '''IntegrationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1377.IntegrationMethod]':
        '''List[IntegrationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ValueInputOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ValueInputOption

    A specific implementation of 'EnumWithSelectedValue' for 'ValueInputOption' types.
    '''

    __hash__ = None
    __qualname__ = 'ValueInputOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1394.ValueInputOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1394.ValueInputOption

    @classmethod
    def implicit_type(cls) -> '_1394.ValueInputOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1394.ValueInputOption.type_()

    @property
    def selected_value(self) -> '_1394.ValueInputOption':
        '''ValueInputOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1394.ValueInputOption]':
        '''List[ValueInputOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SinglePointSelectionMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SinglePointSelectionMethod

    A specific implementation of 'EnumWithSelectedValue' for 'SinglePointSelectionMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'SinglePointSelectionMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1401.SinglePointSelectionMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1401.SinglePointSelectionMethod

    @classmethod
    def implicit_type(cls) -> '_1401.SinglePointSelectionMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1401.SinglePointSelectionMethod.type_()

    @property
    def selected_value(self) -> '_1401.SinglePointSelectionMethod':
        '''SinglePointSelectionMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1401.SinglePointSelectionMethod]':
        '''List[SinglePointSelectionMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ModeInputType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ModeInputType

    A specific implementation of 'EnumWithSelectedValue' for 'ModeInputType' types.
    '''

    __hash__ = None
    __qualname__ = 'ModeInputType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1383.ModeInputType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1383.ModeInputType

    @classmethod
    def implicit_type(cls) -> '_1383.ModeInputType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1383.ModeInputType.type_()

    @property
    def selected_value(self) -> '_1383.ModeInputType':
        '''ModeInputType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1383.ModeInputType]':
        '''List[ModeInputType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RollerBearingProfileTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RollerBearingProfileTypes

    A specific implementation of 'EnumWithSelectedValue' for 'RollerBearingProfileTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'RollerBearingProfileTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1523.RollerBearingProfileTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1523.RollerBearingProfileTypes

    @classmethod
    def implicit_type(cls) -> '_1523.RollerBearingProfileTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1523.RollerBearingProfileTypes.type_()

    @property
    def selected_value(self) -> '_1523.RollerBearingProfileTypes':
        '''RollerBearingProfileTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1523.RollerBearingProfileTypes]':
        '''List[RollerBearingProfileTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_FluidFilmTemperatureOptions(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_FluidFilmTemperatureOptions

    A specific implementation of 'EnumWithSelectedValue' for 'FluidFilmTemperatureOptions' types.
    '''

    __hash__ = None
    __qualname__ = 'FluidFilmTemperatureOptions'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1516.FluidFilmTemperatureOptions':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1516.FluidFilmTemperatureOptions

    @classmethod
    def implicit_type(cls) -> '_1516.FluidFilmTemperatureOptions.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1516.FluidFilmTemperatureOptions.type_()

    @property
    def selected_value(self) -> '_1516.FluidFilmTemperatureOptions':
        '''FluidFilmTemperatureOptions: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1516.FluidFilmTemperatureOptions]':
        '''List[FluidFilmTemperatureOptions]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SupportToleranceLocationDesignation(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SupportToleranceLocationDesignation

    A specific implementation of 'EnumWithSelectedValue' for 'SupportToleranceLocationDesignation' types.
    '''

    __hash__ = None
    __qualname__ = 'SupportToleranceLocationDesignation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1549.SupportToleranceLocationDesignation':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1549.SupportToleranceLocationDesignation

    @classmethod
    def implicit_type(cls) -> '_1549.SupportToleranceLocationDesignation.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1549.SupportToleranceLocationDesignation.type_()

    @property
    def selected_value(self) -> '_1549.SupportToleranceLocationDesignation':
        '''SupportToleranceLocationDesignation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1549.SupportToleranceLocationDesignation]':
        '''List[SupportToleranceLocationDesignation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RollingBearingArrangement(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RollingBearingArrangement

    A specific implementation of 'EnumWithSelectedValue' for 'RollingBearingArrangement' types.
    '''

    __hash__ = None
    __qualname__ = 'RollingBearingArrangement'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1524.RollingBearingArrangement':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1524.RollingBearingArrangement

    @classmethod
    def implicit_type(cls) -> '_1524.RollingBearingArrangement.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1524.RollingBearingArrangement.type_()

    @property
    def selected_value(self) -> '_1524.RollingBearingArrangement':
        '''RollingBearingArrangement: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1524.RollingBearingArrangement]':
        '''List[RollingBearingArrangement]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RollingBearingRaceType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RollingBearingRaceType

    A specific implementation of 'EnumWithSelectedValue' for 'RollingBearingRaceType' types.
    '''

    __hash__ = None
    __qualname__ = 'RollingBearingRaceType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1527.RollingBearingRaceType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1527.RollingBearingRaceType

    @classmethod
    def implicit_type(cls) -> '_1527.RollingBearingRaceType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1527.RollingBearingRaceType.type_()

    @property
    def selected_value(self) -> '_1527.RollingBearingRaceType':
        '''RollingBearingRaceType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1527.RollingBearingRaceType]':
        '''List[RollingBearingRaceType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'BasicDynamicLoadRatingCalculationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'BasicDynamicLoadRatingCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1504.BasicDynamicLoadRatingCalculationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1504.BasicDynamicLoadRatingCalculationMethod

    @classmethod
    def implicit_type(cls) -> '_1504.BasicDynamicLoadRatingCalculationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1504.BasicDynamicLoadRatingCalculationMethod.type_()

    @property
    def selected_value(self) -> '_1504.BasicDynamicLoadRatingCalculationMethod':
        '''BasicDynamicLoadRatingCalculationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1504.BasicDynamicLoadRatingCalculationMethod]':
        '''List[BasicDynamicLoadRatingCalculationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'BasicStaticLoadRatingCalculationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'BasicStaticLoadRatingCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1505.BasicStaticLoadRatingCalculationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1505.BasicStaticLoadRatingCalculationMethod

    @classmethod
    def implicit_type(cls) -> '_1505.BasicStaticLoadRatingCalculationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1505.BasicStaticLoadRatingCalculationMethod.type_()

    @property
    def selected_value(self) -> '_1505.BasicStaticLoadRatingCalculationMethod':
        '''BasicStaticLoadRatingCalculationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1505.BasicStaticLoadRatingCalculationMethod]':
        '''List[BasicStaticLoadRatingCalculationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RotationalDirections(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RotationalDirections

    A specific implementation of 'EnumWithSelectedValue' for 'RotationalDirections' types.
    '''

    __hash__ = None
    __qualname__ = 'RotationalDirections'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1529.RotationalDirections':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1529.RotationalDirections

    @classmethod
    def implicit_type(cls) -> '_1529.RotationalDirections.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1529.RotationalDirections.type_()

    @property
    def selected_value(self) -> '_1529.RotationalDirections':
        '''RotationalDirections: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1529.RotationalDirections]':
        '''List[RotationalDirections]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing

    A specific implementation of 'EnumWithSelectedValue' for 'ShaftDiameterModificationDueToRollingBearingRing' types.
    '''

    __hash__ = None
    __qualname__ = 'ShaftDiameterModificationDueToRollingBearingRing'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2016.ShaftDiameterModificationDueToRollingBearingRing':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2016.ShaftDiameterModificationDueToRollingBearingRing

    @classmethod
    def implicit_type(cls) -> '_2016.ShaftDiameterModificationDueToRollingBearingRing.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2016.ShaftDiameterModificationDueToRollingBearingRing.type_()

    @property
    def selected_value(self) -> '_2016.ShaftDiameterModificationDueToRollingBearingRing':
        '''ShaftDiameterModificationDueToRollingBearingRing: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2016.ShaftDiameterModificationDueToRollingBearingRing]':
        '''List[ShaftDiameterModificationDueToRollingBearingRing]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LinkNodeSource(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LinkNodeSource

    A specific implementation of 'EnumWithSelectedValue' for 'LinkNodeSource' types.
    '''

    __hash__ = None
    __qualname__ = 'LinkNodeSource'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1956.LinkNodeSource':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1956.LinkNodeSource

    @classmethod
    def implicit_type(cls) -> '_1956.LinkNodeSource.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1956.LinkNodeSource.type_()

    @property
    def selected_value(self) -> '_1956.LinkNodeSource':
        '''LinkNodeSource: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1956.LinkNodeSource]':
        '''List[LinkNodeSource]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ComponentOrientationOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ComponentOrientationOption

    A specific implementation of 'EnumWithSelectedValue' for 'ComponentOrientationOption' types.
    '''

    __hash__ = None
    __qualname__ = 'ComponentOrientationOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1918.ComponentOrientationOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1918.ComponentOrientationOption

    @classmethod
    def implicit_type(cls) -> '_1918.ComponentOrientationOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1918.ComponentOrientationOption.type_()

    @property
    def selected_value(self) -> '_1918.ComponentOrientationOption':
        '''ComponentOrientationOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1918.ComponentOrientationOption]':
        '''List[ComponentOrientationOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_Axis(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_Axis

    A specific implementation of 'EnumWithSelectedValue' for 'Axis' types.
    '''

    __hash__ = None
    __qualname__ = 'Axis'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1061.Axis':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1061.Axis

    @classmethod
    def implicit_type(cls) -> '_1061.Axis.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1061.Axis.type_()

    @property
    def selected_value(self) -> '_1061.Axis':
        '''Axis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1061.Axis]':
        '''List[Axis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_AlignmentAxis(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_AlignmentAxis

    A specific implementation of 'EnumWithSelectedValue' for 'AlignmentAxis' types.
    '''

    __hash__ = None
    __qualname__ = 'AlignmentAxis'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1060.AlignmentAxis':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1060.AlignmentAxis

    @classmethod
    def implicit_type(cls) -> '_1060.AlignmentAxis.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1060.AlignmentAxis.type_()

    @property
    def selected_value(self) -> '_1060.AlignmentAxis':
        '''AlignmentAxis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1060.AlignmentAxis]':
        '''List[AlignmentAxis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DesignEntityId(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DesignEntityId

    A specific implementation of 'EnumWithSelectedValue' for 'DesignEntityId' types.
    '''

    __hash__ = None
    __qualname__ = 'DesignEntityId'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1796.DesignEntityId':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1796.DesignEntityId

    @classmethod
    def implicit_type(cls) -> '_1796.DesignEntityId.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1796.DesignEntityId.type_()

    @property
    def selected_value(self) -> '_1796.DesignEntityId':
        '''DesignEntityId: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1796.DesignEntityId]':
        '''List[DesignEntityId]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ImportedFEType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ImportedFEType

    A specific implementation of 'EnumWithSelectedValue' for 'ImportedFEType' types.
    '''

    __hash__ = None
    __qualname__ = 'ImportedFEType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1948.ImportedFEType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1948.ImportedFEType

    @classmethod
    def implicit_type(cls) -> '_1948.ImportedFEType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1948.ImportedFEType.type_()

    @property
    def selected_value(self) -> '_1948.ImportedFEType':
        '''ImportedFEType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1948.ImportedFEType]':
        '''List[ImportedFEType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ThermalExpansionOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ThermalExpansionOption

    A specific implementation of 'EnumWithSelectedValue' for 'ThermalExpansionOption' types.
    '''

    __hash__ = None
    __qualname__ = 'ThermalExpansionOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1972.ThermalExpansionOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1972.ThermalExpansionOption

    @classmethod
    def implicit_type(cls) -> '_1972.ThermalExpansionOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1972.ThermalExpansionOption.type_()

    @property
    def selected_value(self) -> '_1972.ThermalExpansionOption':
        '''ThermalExpansionOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1972.ThermalExpansionOption]':
        '''List[ThermalExpansionOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ThreeDViewContourOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ThreeDViewContourOption

    A specific implementation of 'EnumWithSelectedValue' for 'ThreeDViewContourOption' types.
    '''

    __hash__ = None
    __qualname__ = 'ThreeDViewContourOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1337.ThreeDViewContourOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1337.ThreeDViewContourOption

    @classmethod
    def implicit_type(cls) -> '_1337.ThreeDViewContourOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1337.ThreeDViewContourOption.type_()

    @property
    def selected_value(self) -> '_1337.ThreeDViewContourOption':
        '''ThreeDViewContourOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1337.ThreeDViewContourOption]':
        '''List[ThreeDViewContourOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BoundaryConditionType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BoundaryConditionType

    A specific implementation of 'EnumWithSelectedValue' for 'BoundaryConditionType' types.
    '''

    __hash__ = None
    __qualname__ = 'BoundaryConditionType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1449.BoundaryConditionType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1449.BoundaryConditionType

    @classmethod
    def implicit_type(cls) -> '_1449.BoundaryConditionType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1449.BoundaryConditionType.type_()

    @property
    def selected_value(self) -> '_1449.BoundaryConditionType':
        '''BoundaryConditionType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1449.BoundaryConditionType]':
        '''List[BoundaryConditionType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_FEExportFormat(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_FEExportFormat

    A specific implementation of 'EnumWithSelectedValue' for 'FEExportFormat' types.
    '''

    __hash__ = None
    __qualname__ = 'FEExportFormat'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1450.FEExportFormat':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1450.FEExportFormat

    @classmethod
    def implicit_type(cls) -> '_1450.FEExportFormat.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1450.FEExportFormat.type_()

    @property
    def selected_value(self) -> '_1450.FEExportFormat':
        '''FEExportFormat: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1450.FEExportFormat]':
        '''List[FEExportFormat]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BearingToleranceClass(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BearingToleranceClass

    A specific implementation of 'EnumWithSelectedValue' for 'BearingToleranceClass' types.
    '''

    __hash__ = None
    __qualname__ = 'BearingToleranceClass'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1533.BearingToleranceClass':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1533.BearingToleranceClass

    @classmethod
    def implicit_type(cls) -> '_1533.BearingToleranceClass.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1533.BearingToleranceClass.type_()

    @property
    def selected_value(self) -> '_1533.BearingToleranceClass':
        '''BearingToleranceClass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1533.BearingToleranceClass]':
        '''List[BearingToleranceClass]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BearingModel(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BearingModel

    A specific implementation of 'EnumWithSelectedValue' for 'BearingModel' types.
    '''

    __hash__ = None
    __qualname__ = 'BearingModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1511.BearingModel':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1511.BearingModel

    @classmethod
    def implicit_type(cls) -> '_1511.BearingModel.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1511.BearingModel.type_()

    @property
    def selected_value(self) -> '_1511.BearingModel':
        '''BearingModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1511.BearingModel]':
        '''List[BearingModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_PreloadType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_PreloadType

    A specific implementation of 'EnumWithSelectedValue' for 'PreloadType' types.
    '''

    __hash__ = None
    __qualname__ = 'PreloadType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1582.PreloadType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1582.PreloadType

    @classmethod
    def implicit_type(cls) -> '_1582.PreloadType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1582.PreloadType.type_()

    @property
    def selected_value(self) -> '_1582.PreloadType':
        '''PreloadType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1582.PreloadType]':
        '''List[PreloadType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RaceRadialMountingType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RaceRadialMountingType

    A specific implementation of 'EnumWithSelectedValue' for 'RaceRadialMountingType' types.
    '''

    __hash__ = None
    __qualname__ = 'RaceRadialMountingType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1584.RaceRadialMountingType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1584.RaceRadialMountingType

    @classmethod
    def implicit_type(cls) -> '_1584.RaceRadialMountingType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1584.RaceRadialMountingType.type_()

    @property
    def selected_value(self) -> '_1584.RaceRadialMountingType':
        '''RaceRadialMountingType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1584.RaceRadialMountingType]':
        '''List[RaceRadialMountingType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RaceAxialMountingType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RaceAxialMountingType

    A specific implementation of 'EnumWithSelectedValue' for 'RaceAxialMountingType' types.
    '''

    __hash__ = None
    __qualname__ = 'RaceAxialMountingType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1583.RaceAxialMountingType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1583.RaceAxialMountingType

    @classmethod
    def implicit_type(cls) -> '_1583.RaceAxialMountingType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1583.RaceAxialMountingType.type_()

    @property
    def selected_value(self) -> '_1583.RaceAxialMountingType':
        '''RaceAxialMountingType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1583.RaceAxialMountingType]':
        '''List[RaceAxialMountingType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BearingToleranceDefinitionOptions(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BearingToleranceDefinitionOptions

    A specific implementation of 'EnumWithSelectedValue' for 'BearingToleranceDefinitionOptions' types.
    '''

    __hash__ = None
    __qualname__ = 'BearingToleranceDefinitionOptions'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1534.BearingToleranceDefinitionOptions':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1534.BearingToleranceDefinitionOptions

    @classmethod
    def implicit_type(cls) -> '_1534.BearingToleranceDefinitionOptions.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1534.BearingToleranceDefinitionOptions.type_()

    @property
    def selected_value(self) -> '_1534.BearingToleranceDefinitionOptions':
        '''BearingToleranceDefinitionOptions: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1534.BearingToleranceDefinitionOptions]':
        '''List[BearingToleranceDefinitionOptions]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_InternalClearanceClass(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_InternalClearanceClass

    A specific implementation of 'EnumWithSelectedValue' for 'InternalClearanceClass' types.
    '''

    __hash__ = None
    __qualname__ = 'InternalClearanceClass'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1532.InternalClearanceClass':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1532.InternalClearanceClass

    @classmethod
    def implicit_type(cls) -> '_1532.InternalClearanceClass.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1532.InternalClearanceClass.type_()

    @property
    def selected_value(self) -> '_1532.InternalClearanceClass':
        '''InternalClearanceClass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1532.InternalClearanceClass]':
        '''List[InternalClearanceClass]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_PowerLoadType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_PowerLoadType

    A specific implementation of 'EnumWithSelectedValue' for 'PowerLoadType' types.
    '''

    __hash__ = None
    __qualname__ = 'PowerLoadType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1807.PowerLoadType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1807.PowerLoadType

    @classmethod
    def implicit_type(cls) -> '_1807.PowerLoadType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1807.PowerLoadType.type_()

    @property
    def selected_value(self) -> '_1807.PowerLoadType':
        '''PowerLoadType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1807.PowerLoadType]':
        '''List[PowerLoadType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RigidConnectorTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RigidConnectorTypes

    A specific implementation of 'EnumWithSelectedValue' for 'RigidConnectorTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'RigidConnectorTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2129.RigidConnectorTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2129.RigidConnectorTypes

    @classmethod
    def implicit_type(cls) -> '_2129.RigidConnectorTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2129.RigidConnectorTypes.type_()

    @property
    def selected_value(self) -> '_2129.RigidConnectorTypes':
        '''RigidConnectorTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2129.RigidConnectorTypes]':
        '''List[RigidConnectorTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RigidConnectorStiffnessType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RigidConnectorStiffnessType

    A specific implementation of 'EnumWithSelectedValue' for 'RigidConnectorStiffnessType' types.
    '''

    __hash__ = None
    __qualname__ = 'RigidConnectorStiffnessType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2125.RigidConnectorStiffnessType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2125.RigidConnectorStiffnessType

    @classmethod
    def implicit_type(cls) -> '_2125.RigidConnectorStiffnessType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2125.RigidConnectorStiffnessType.type_()

    @property
    def selected_value(self) -> '_2125.RigidConnectorStiffnessType':
        '''RigidConnectorStiffnessType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2125.RigidConnectorStiffnessType]':
        '''List[RigidConnectorStiffnessType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_FitTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_FitTypes

    A specific implementation of 'EnumWithSelectedValue' for 'FitTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'FitTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_978.FitTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _978.FitTypes

    @classmethod
    def implicit_type(cls) -> '_978.FitTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _978.FitTypes.type_()

    @property
    def selected_value(self) -> '_978.FitTypes':
        '''FitTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_978.FitTypes]':
        '''List[FitTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RigidConnectorToothSpacingType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RigidConnectorToothSpacingType

    A specific implementation of 'EnumWithSelectedValue' for 'RigidConnectorToothSpacingType' types.
    '''

    __hash__ = None
    __qualname__ = 'RigidConnectorToothSpacingType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2128.RigidConnectorToothSpacingType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2128.RigidConnectorToothSpacingType

    @classmethod
    def implicit_type(cls) -> '_2128.RigidConnectorToothSpacingType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2128.RigidConnectorToothSpacingType.type_()

    @property
    def selected_value(self) -> '_2128.RigidConnectorToothSpacingType':
        '''RigidConnectorToothSpacingType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2128.RigidConnectorToothSpacingType]':
        '''List[RigidConnectorToothSpacingType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DoeValueSpecificationOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DoeValueSpecificationOption

    A specific implementation of 'EnumWithSelectedValue' for 'DoeValueSpecificationOption' types.
    '''

    __hash__ = None
    __qualname__ = 'DoeValueSpecificationOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_3510.DoeValueSpecificationOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _3510.DoeValueSpecificationOption

    @classmethod
    def implicit_type(cls) -> '_3510.DoeValueSpecificationOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _3510.DoeValueSpecificationOption.type_()

    @property
    def selected_value(self) -> '_3510.DoeValueSpecificationOption':
        '''DoeValueSpecificationOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_3510.DoeValueSpecificationOption]':
        '''List[DoeValueSpecificationOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_AnalysisType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_AnalysisType

    A specific implementation of 'EnumWithSelectedValue' for 'AnalysisType' types.
    '''

    __hash__ = None
    __qualname__ = 'AnalysisType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6052.AnalysisType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6052.AnalysisType

    @classmethod
    def implicit_type(cls) -> '_6052.AnalysisType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6052.AnalysisType.type_()

    @property
    def selected_value(self) -> '_6052.AnalysisType':
        '''AnalysisType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6052.AnalysisType]':
        '''List[AnalysisType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BarModelExportType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BarModelExportType

    A specific implementation of 'EnumWithSelectedValue' for 'BarModelExportType' types.
    '''

    __hash__ = None
    __qualname__ = 'BarModelExportType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1362.BarModelExportType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1362.BarModelExportType

    @classmethod
    def implicit_type(cls) -> '_1362.BarModelExportType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1362.BarModelExportType.type_()

    @property
    def selected_value(self) -> '_1362.BarModelExportType':
        '''BarModelExportType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1362.BarModelExportType]':
        '''List[BarModelExportType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DynamicsResponseType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DynamicsResponseType

    A specific implementation of 'EnumWithSelectedValue' for 'DynamicsResponseType' types.
    '''

    __hash__ = None
    __qualname__ = 'DynamicsResponseType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1071.DynamicsResponseType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1071.DynamicsResponseType

    @classmethod
    def implicit_type(cls) -> '_1071.DynamicsResponseType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1071.DynamicsResponseType.type_()

    @property
    def selected_value(self) -> '_1071.DynamicsResponseType':
        '''DynamicsResponseType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1071.DynamicsResponseType]':
        '''List[DynamicsResponseType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DynamicsResponseScaling(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DynamicsResponseScaling

    A specific implementation of 'EnumWithSelectedValue' for 'DynamicsResponseScaling' types.
    '''

    __hash__ = None
    __qualname__ = 'DynamicsResponseScaling'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1070.DynamicsResponseScaling':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1070.DynamicsResponseScaling

    @classmethod
    def implicit_type(cls) -> '_1070.DynamicsResponseScaling.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1070.DynamicsResponseScaling.type_()

    @property
    def selected_value(self) -> '_1070.DynamicsResponseScaling':
        '''DynamicsResponseScaling: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1070.DynamicsResponseScaling]':
        '''List[DynamicsResponseScaling]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BearingStiffnessModel(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BearingStiffnessModel

    A specific implementation of 'EnumWithSelectedValue' for 'BearingStiffnessModel' types.
    '''

    __hash__ = None
    __qualname__ = 'BearingStiffnessModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_4974.BearingStiffnessModel':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _4974.BearingStiffnessModel

    @classmethod
    def implicit_type(cls) -> '_4974.BearingStiffnessModel.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _4974.BearingStiffnessModel.type_()

    @property
    def selected_value(self) -> '_4974.BearingStiffnessModel':
        '''BearingStiffnessModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_4974.BearingStiffnessModel]':
        '''List[BearingStiffnessModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_GearMeshStiffnessModel(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_GearMeshStiffnessModel

    A specific implementation of 'EnumWithSelectedValue' for 'GearMeshStiffnessModel' types.
    '''

    __hash__ = None
    __qualname__ = 'GearMeshStiffnessModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5021.GearMeshStiffnessModel':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _5021.GearMeshStiffnessModel

    @classmethod
    def implicit_type(cls) -> '_5021.GearMeshStiffnessModel.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5021.GearMeshStiffnessModel.type_()

    @property
    def selected_value(self) -> '_5021.GearMeshStiffnessModel':
        '''GearMeshStiffnessModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_5021.GearMeshStiffnessModel]':
        '''List[GearMeshStiffnessModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ShaftAndHousingFlexibilityOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ShaftAndHousingFlexibilityOption

    A specific implementation of 'EnumWithSelectedValue' for 'ShaftAndHousingFlexibilityOption' types.
    '''

    __hash__ = None
    __qualname__ = 'ShaftAndHousingFlexibilityOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5066.ShaftAndHousingFlexibilityOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _5066.ShaftAndHousingFlexibilityOption

    @classmethod
    def implicit_type(cls) -> '_5066.ShaftAndHousingFlexibilityOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5066.ShaftAndHousingFlexibilityOption.type_()

    @property
    def selected_value(self) -> '_5066.ShaftAndHousingFlexibilityOption':
        '''ShaftAndHousingFlexibilityOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_5066.ShaftAndHousingFlexibilityOption]':
        '''List[ShaftAndHousingFlexibilityOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ExportOutputType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ExportOutputType

    A specific implementation of 'EnumWithSelectedValue' for 'GearWhineAnalysisFEExportOptions.ExportOutputType' types.
    '''

    __hash__ = None
    __qualname__ = 'GearWhineAnalysisFEExportOptions.ExportOutputType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5323.GearWhineAnalysisFEExportOptions.ExportOutputType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _5323.GearWhineAnalysisFEExportOptions.ExportOutputType

    @classmethod
    def implicit_type(cls) -> '_5323.GearWhineAnalysisFEExportOptions.ExportOutputType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5323.GearWhineAnalysisFEExportOptions.ExportOutputType.type_()

    @property
    def selected_value(self) -> '_5323.GearWhineAnalysisFEExportOptions.ExportOutputType':
        '''GearWhineAnalysisFEExportOptions.ExportOutputType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_5323.GearWhineAnalysisFEExportOptions.ExportOutputType]':
        '''List[GearWhineAnalysisFEExportOptions.ExportOutputType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ComplexNumberOutput(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ComplexNumberOutput

    A specific implementation of 'EnumWithSelectedValue' for 'GearWhineAnalysisFEExportOptions.ComplexNumberOutput' types.
    '''

    __hash__ = None
    __qualname__ = 'GearWhineAnalysisFEExportOptions.ComplexNumberOutput'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5323.GearWhineAnalysisFEExportOptions.ComplexNumberOutput':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _5323.GearWhineAnalysisFEExportOptions.ComplexNumberOutput

    @classmethod
    def implicit_type(cls) -> '_5323.GearWhineAnalysisFEExportOptions.ComplexNumberOutput.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5323.GearWhineAnalysisFEExportOptions.ComplexNumberOutput.type_()

    @property
    def selected_value(self) -> '_5323.GearWhineAnalysisFEExportOptions.ComplexNumberOutput':
        '''GearWhineAnalysisFEExportOptions.ComplexNumberOutput: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_5323.GearWhineAnalysisFEExportOptions.ComplexNumberOutput]':
        '''List[GearWhineAnalysisFEExportOptions.ComplexNumberOutput]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_StressConcentrationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_StressConcentrationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'StressConcentrationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'StressConcentrationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1718.StressConcentrationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1718.StressConcentrationMethod

    @classmethod
    def implicit_type(cls) -> '_1718.StressConcentrationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1718.StressConcentrationMethod.type_()

    @property
    def selected_value(self) -> '_1718.StressConcentrationMethod':
        '''StressConcentrationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1718.StressConcentrationMethod]':
        '''List[StressConcentrationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_MeshStiffnessModel(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_MeshStiffnessModel

    A specific implementation of 'EnumWithSelectedValue' for 'MeshStiffnessModel' types.
    '''

    __hash__ = None
    __qualname__ = 'MeshStiffnessModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1803.MeshStiffnessModel':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1803.MeshStiffnessModel

    @classmethod
    def implicit_type(cls) -> '_1803.MeshStiffnessModel.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1803.MeshStiffnessModel.type_()

    @property
    def selected_value(self) -> '_1803.MeshStiffnessModel':
        '''MeshStiffnessModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1803.MeshStiffnessModel]':
        '''List[MeshStiffnessModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_TorqueRippleInputType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_TorqueRippleInputType

    A specific implementation of 'EnumWithSelectedValue' for 'TorqueRippleInputType' types.
    '''

    __hash__ = None
    __qualname__ = 'TorqueRippleInputType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6203.TorqueRippleInputType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6203.TorqueRippleInputType

    @classmethod
    def implicit_type(cls) -> '_6203.TorqueRippleInputType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6203.TorqueRippleInputType.type_()

    @property
    def selected_value(self) -> '_6203.TorqueRippleInputType':
        '''TorqueRippleInputType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6203.TorqueRippleInputType]':
        '''List[TorqueRippleInputType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_HarmonicLoadDataType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_HarmonicLoadDataType

    A specific implementation of 'EnumWithSelectedValue' for 'HarmonicLoadDataType' types.
    '''

    __hash__ = None
    __qualname__ = 'HarmonicLoadDataType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6132.HarmonicLoadDataType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6132.HarmonicLoadDataType

    @classmethod
    def implicit_type(cls) -> '_6132.HarmonicLoadDataType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6132.HarmonicLoadDataType.type_()

    @property
    def selected_value(self) -> '_6132.HarmonicLoadDataType':
        '''HarmonicLoadDataType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6132.HarmonicLoadDataType]':
        '''List[HarmonicLoadDataType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_HarmonicExcitationType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_HarmonicExcitationType

    A specific implementation of 'EnumWithSelectedValue' for 'HarmonicExcitationType' types.
    '''

    __hash__ = None
    __qualname__ = 'HarmonicExcitationType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6125.HarmonicExcitationType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6125.HarmonicExcitationType

    @classmethod
    def implicit_type(cls) -> '_6125.HarmonicExcitationType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6125.HarmonicExcitationType.type_()

    @property
    def selected_value(self) -> '_6125.HarmonicExcitationType':
        '''HarmonicExcitationType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6125.HarmonicExcitationType]':
        '''List[HarmonicExcitationType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification

    A specific implementation of 'EnumWithSelectedValue' for 'PointLoadLoadCase.ForceSpecification' types.
    '''

    __hash__ = None
    __qualname__ = 'PointLoadLoadCase.ForceSpecification'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6165.PointLoadLoadCase.ForceSpecification':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6165.PointLoadLoadCase.ForceSpecification

    @classmethod
    def implicit_type(cls) -> '_6165.PointLoadLoadCase.ForceSpecification.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6165.PointLoadLoadCase.ForceSpecification.type_()

    @property
    def selected_value(self) -> '_6165.PointLoadLoadCase.ForceSpecification':
        '''PointLoadLoadCase.ForceSpecification: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6165.PointLoadLoadCase.ForceSpecification]':
        '''List[PointLoadLoadCase.ForceSpecification]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'PowerLoadInputTorqueSpecificationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'PowerLoadInputTorqueSpecificationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1805.PowerLoadInputTorqueSpecificationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1805.PowerLoadInputTorqueSpecificationMethod

    @classmethod
    def implicit_type(cls) -> '_1805.PowerLoadInputTorqueSpecificationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1805.PowerLoadInputTorqueSpecificationMethod.type_()

    @property
    def selected_value(self) -> '_1805.PowerLoadInputTorqueSpecificationMethod':
        '''PowerLoadInputTorqueSpecificationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1805.PowerLoadInputTorqueSpecificationMethod]':
        '''List[PowerLoadInputTorqueSpecificationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_TorqueSpecificationForSystemDeflection(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_TorqueSpecificationForSystemDeflection

    A specific implementation of 'EnumWithSelectedValue' for 'TorqueSpecificationForSystemDeflection' types.
    '''

    __hash__ = None
    __qualname__ = 'TorqueSpecificationForSystemDeflection'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6204.TorqueSpecificationForSystemDeflection':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6204.TorqueSpecificationForSystemDeflection

    @classmethod
    def implicit_type(cls) -> '_6204.TorqueSpecificationForSystemDeflection.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6204.TorqueSpecificationForSystemDeflection.type_()

    @property
    def selected_value(self) -> '_6204.TorqueSpecificationForSystemDeflection':
        '''TorqueSpecificationForSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6204.TorqueSpecificationForSystemDeflection]':
        '''List[TorqueSpecificationForSystemDeflection]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_TorqueConverterLockupRule(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_TorqueConverterLockupRule

    A specific implementation of 'EnumWithSelectedValue' for 'TorqueConverterLockupRule' types.
    '''

    __hash__ = None
    __qualname__ = 'TorqueConverterLockupRule'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5091.TorqueConverterLockupRule':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _5091.TorqueConverterLockupRule

    @classmethod
    def implicit_type(cls) -> '_5091.TorqueConverterLockupRule.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5091.TorqueConverterLockupRule.type_()

    @property
    def selected_value(self) -> '_5091.TorqueConverterLockupRule':
        '''TorqueConverterLockupRule: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_5091.TorqueConverterLockupRule]':
        '''List[TorqueConverterLockupRule]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DegreesOfFreedom(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DegreesOfFreedom

    A specific implementation of 'EnumWithSelectedValue' for 'DegreesOfFreedom' types.
    '''

    __hash__ = None
    __qualname__ = 'DegreesOfFreedom'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1068.DegreesOfFreedom':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1068.DegreesOfFreedom

    @classmethod
    def implicit_type(cls) -> '_1068.DegreesOfFreedom.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1068.DegreesOfFreedom.type_()

    @property
    def selected_value(self) -> '_1068.DegreesOfFreedom':
        '''DegreesOfFreedom: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1068.DegreesOfFreedom]':
        '''List[DegreesOfFreedom]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DestinationDesignState(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DestinationDesignState

    A specific implementation of 'EnumWithSelectedValue' for 'DestinationDesignState' types.
    '''

    __hash__ = None
    __qualname__ = 'DestinationDesignState'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6218.DestinationDesignState':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6218.DestinationDesignState

    @classmethod
    def implicit_type(cls) -> '_6218.DestinationDesignState.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6218.DestinationDesignState.type_()

    @property
    def selected_value(self) -> '_6218.DestinationDesignState':
        '''DestinationDesignState: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6218.DestinationDesignState]':
        '''List[DestinationDesignState]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None
