'''_1423.py

DynamicCustomReportItem
'''


from mastapy._internal import constructor
from mastapy.utility.report import (
    _1406, _1404, _1398, _1401,
    _1417, _1399, _1414, _1390,
    _1405, _1416, _1419, _1421,
    _1395, _1397, _1413
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.parametric_study_tools import _1645
from mastapy.bearings.bearing_results import _1520
from mastapy._internal.python_net import python_net_import

_DYNAMIC_CUSTOM_REPORT_ITEM = python_net_import('SMT.MastaAPI.Utility.Report', 'DynamicCustomReportItem')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicCustomReportItem',)


class DynamicCustomReportItem(_1413.CustomReportNameableItem):
    '''DynamicCustomReportItem

    This is a mastapy class.
    '''

    TYPE = _DYNAMIC_CUSTOM_REPORT_ITEM
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DynamicCustomReportItem.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def is_main_report_item(self) -> 'bool':
        '''bool: 'IsMainReportItem' is the original name of this property.'''

        return self.wrapped.IsMainReportItem

    @is_main_report_item.setter
    def is_main_report_item(self, value: 'bool'):
        self.wrapped.IsMainReportItem = bool(value) if value else False

    @property
    def inner_item(self) -> '_1406.CustomReportItem':
        '''CustomReportItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1406.CustomReportItem)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_horizontal_line(self) -> '_1404.CustomReportHorizontalLine':
        '''CustomReportHorizontalLine: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.InnerItem.__class__.__qualname__ != 'CustomReportHorizontalLine':
            raise CastException('Failed to cast inner_item to CustomReportHorizontalLine. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1404.CustomReportHorizontalLine)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report(self) -> '_1398.CustomReport':
        '''CustomReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.InnerItem.__class__.__qualname__ != 'CustomReport':
            raise CastException('Failed to cast inner_item to CustomReport. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1398.CustomReport)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_column(self) -> '_1401.CustomReportColumn':
        '''CustomReportColumn: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.InnerItem.__class__.__qualname__ != 'CustomReportColumn':
            raise CastException('Failed to cast inner_item to CustomReportColumn. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1401.CustomReportColumn)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_tab(self) -> '_1417.CustomReportTab':
        '''CustomReportTab: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.InnerItem.__class__.__qualname__ != 'CustomReportTab':
            raise CastException('Failed to cast inner_item to CustomReportTab. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1417.CustomReportTab)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_cad_drawing(self) -> '_1399.CustomReportCadDrawing':
        '''CustomReportCadDrawing: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.InnerItem.__class__.__qualname__ != 'CustomReportCadDrawing':
            raise CastException('Failed to cast inner_item to CustomReportCadDrawing. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1399.CustomReportCadDrawing)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_named_item(self) -> '_1414.CustomReportNamedItem':
        '''CustomReportNamedItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.InnerItem.__class__.__qualname__ != 'CustomReportNamedItem':
            raise CastException('Failed to cast inner_item to CustomReportNamedItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1414.CustomReportNamedItem)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_dynamic_custom_report_item(self) -> 'DynamicCustomReportItem':
        '''DynamicCustomReportItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.InnerItem.__class__.__qualname__ != 'DynamicCustomReportItem':
            raise CastException('Failed to cast inner_item to DynamicCustomReportItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(DynamicCustomReportItem)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_ad_hoc_custom_table(self) -> '_1390.AdHocCustomTable':
        '''AdHocCustomTable: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.InnerItem.__class__.__qualname__ != 'AdHocCustomTable':
            raise CastException('Failed to cast inner_item to AdHocCustomTable. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1390.AdHocCustomTable)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_html_item(self) -> '_1405.CustomReportHtmlItem':
        '''CustomReportHtmlItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.InnerItem.__class__.__qualname__ != 'CustomReportHtmlItem':
            raise CastException('Failed to cast inner_item to CustomReportHtmlItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1405.CustomReportHtmlItem)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_status_item(self) -> '_1416.CustomReportStatusItem':
        '''CustomReportStatusItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.InnerItem.__class__.__qualname__ != 'CustomReportStatusItem':
            raise CastException('Failed to cast inner_item to CustomReportStatusItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1416.CustomReportStatusItem)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_text(self) -> '_1419.CustomReportText':
        '''CustomReportText: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.InnerItem.__class__.__qualname__ != 'CustomReportText':
            raise CastException('Failed to cast inner_item to CustomReportText. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1419.CustomReportText)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_sub_report(self) -> '_1421.CustomSubReport':
        '''CustomSubReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.InnerItem.__class__.__qualname__ != 'CustomSubReport':
            raise CastException('Failed to cast inner_item to CustomSubReport. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1421.CustomSubReport)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_parametric_study_histogram(self) -> '_1645.ParametricStudyHistogram':
        '''ParametricStudyHistogram: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.InnerItem.__class__.__qualname__ != 'ParametricStudyHistogram':
            raise CastException('Failed to cast inner_item to ParametricStudyHistogram. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1645.ParametricStudyHistogram)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_chart(self) -> '_1395.CustomChart':
        '''CustomChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.InnerItem.__class__.__qualname__ != 'CustomChart':
            raise CastException('Failed to cast inner_item to CustomChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1395.CustomChart)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_image(self) -> '_1397.CustomImage':
        '''CustomImage: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.InnerItem.__class__.__qualname__ != 'CustomImage':
            raise CastException('Failed to cast inner_item to CustomImage. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1397.CustomImage)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_loaded_bearing_chart_reporter(self) -> '_1520.LoadedBearingChartReporter':
        '''LoadedBearingChartReporter: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.InnerItem.__class__.__qualname__ != 'LoadedBearingChartReporter':
            raise CastException('Failed to cast inner_item to LoadedBearingChartReporter. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1520.LoadedBearingChartReporter)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None
