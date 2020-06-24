'''_1257.py

GaussKronrodOptions
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GAUSS_KRONROD_OPTIONS = python_net_import('SMT.MastaAPI.MathUtility.Integration', 'GaussKronrodOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('GaussKronrodOptions',)


class GaussKronrodOptions(_1.APIBase):
    '''GaussKronrodOptions

    This is a mastapy class.
    '''

    TYPE = _GAUSS_KRONROD_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GaussKronrodOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def use_advanced_zero_region_detection_when_subdividing_domains(self) -> 'bool':
        '''bool: 'UseAdvancedZeroRegionDetectionWhenSubdividingDomains' is the original name of this property.'''

        return self.wrapped.UseAdvancedZeroRegionDetectionWhenSubdividingDomains

    @use_advanced_zero_region_detection_when_subdividing_domains.setter
    def use_advanced_zero_region_detection_when_subdividing_domains(self, value: 'bool'):
        self.wrapped.UseAdvancedZeroRegionDetectionWhenSubdividingDomains = bool(value) if value else False

    @property
    def pre_scan_domains_for_endpoint_zero_regions(self) -> 'bool':
        '''bool: 'PreScanDomainsForEndpointZeroRegions' is the original name of this property.'''

        return self.wrapped.PreScanDomainsForEndpointZeroRegions

    @pre_scan_domains_for_endpoint_zero_regions.setter
    def pre_scan_domains_for_endpoint_zero_regions(self, value: 'bool'):
        self.wrapped.PreScanDomainsForEndpointZeroRegions = bool(value) if value else False

    @property
    def number_of_sample_points_when_finding_zero_regions(self) -> 'int':
        '''int: 'NumberOfSamplePointsWhenFindingZeroRegions' is the original name of this property.'''

        return self.wrapped.NumberOfSamplePointsWhenFindingZeroRegions

    @number_of_sample_points_when_finding_zero_regions.setter
    def number_of_sample_points_when_finding_zero_regions(self, value: 'int'):
        self.wrapped.NumberOfSamplePointsWhenFindingZeroRegions = int(value) if value else 0

    @property
    def precision_for_refining_zero_regions(self) -> 'float':
        '''float: 'PrecisionForRefiningZeroRegions' is the original name of this property.'''

        return self.wrapped.PrecisionForRefiningZeroRegions

    @precision_for_refining_zero_regions.setter
    def precision_for_refining_zero_regions(self, value: 'float'):
        self.wrapped.PrecisionForRefiningZeroRegions = float(value) if value else 0.0
