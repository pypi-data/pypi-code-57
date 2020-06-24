'''_3598.py

GearCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3570
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'GearCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCompoundParametricStudyTool',)


class GearCompoundParametricStudyTool(_3570.MountableComponentCompoundParametricStudyTool):
    '''GearCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
