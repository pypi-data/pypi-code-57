#! usr/bin/python3.6
"""
    Module initially auto generated using V5Automation files from CATIA V5 R28 on 2020-06-11 12:40:47.360445

    .. warning::
        The notes denoted "CAA V5 Visual Basic Help" are to be used as reference only.
        They are there as a guide as to how the visual basic / catscript functions work
        and thus help debugging in pycatia.
        
"""

from pycatia.part_interfaces.defeaturing_filter import DefeaturingFilter
from pycatia.system_interfaces.collection import Collection


class DefeaturingFilters(Collection):
    """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)

                | System.IUnknown
                |     System.IDispatch
                |         System.CATBaseUnknown
                |             System.CATBaseDispatch
                |                 System.Collection
                |                     DefeaturingFilters
                | 
                | Represents the filter collection of a defeaturing object.
    
    """

    def __init__(self, com_object):
        super().__init__(com_object)
        self.defeaturing_filters = com_object

    def add(self, i_filter_type_to_add):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445))
                | o Func Add(CATBSTR iFilterTypeToAdd) As long
                | 
                |     Creates a new filter and adds it to the Defeaturing filters
                |     collection.
                | 
                |     Parameters:
                | 
                |         iFilterTypeToAdd
                |             The type of the new filter to add among : - "DefeaturingFilletFilter" -
                |             "DefeaturingHoleFilter" - or any user-defined filter's type
                | 
                |     Returns:
                |         oAddedFilterIndex The added filter's index - equals to 0 if
                |         FAILED
                | 
                |         Example:
                |             The following example adds a new filter of type theFilterType to
                |             defeaturing colelction firstDefeaturingFilters and returns the index theIndex
                |             of the new filter
                | 
                |              Set theIndex = firstDefeaturingFilters.Add(theFilterType)

        :param str i_filter_type_to_add:
        :return: int
        """
        return self.defeaturing_filters.Add(i_filter_type_to_add)

    def item(self, i_filter_id):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445))
                | o Func Item(CATVariant iFilterId) As DefeaturingFilter
                | 
                |     Returns the filter of the Defeaturing filters collection using its index or
                |     its name.
                | 
                |     Parameters:
                | 
                |         iFilterId
                |             The index or the name of the filter to retrieve As a numerics, must
                |             be in [1;Count]) 
                | 
                |     Returns:
                |         oFilter The filter (see DefeaturingFilter for list of possible
                |         actions)
                | 
                |         Example:
                |             The following example returns in myFilter the filter number
                |             theIndex of Defeaturing collection
                |             firstDefeaturingFilters:
                | 
                |              Set myFilter = firstDefeaturingFilters.Item(theIndex)

        :param CATVariant i_filter_id:
        :return: DefeaturingFilter
        """
        return DefeaturingFilter(self.defeaturing_filters.Item(i_filter_id.com_object))

    def remove(self, i_filter_id):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445))
                | o Sub Remove(CATVariant iFilterId)
                | 
                |     Removes a filter from the Defeaturing filters collection and deletes it,
                |     using its index or its name.
                | 
                |     Parameters:
                | 
                |         iFilterId
                |             The index or the name of the filter to retrieve As a numerics, must
                |             be in [1;Count])
                | 
                |             Example:
                |                 The two following examples remove the filter number theIndex
                |                 from Defeaturing collection
                |                 firstDefeaturingFilters:
                | 
                |                  Call firstDefeaturingFilters.Remove(theIndex)
                |                  firstDefeaturingFilters.Remove theIndex

        :param CATVariant i_filter_id:
        :return: None
        """
        return self.defeaturing_filters.Remove(i_filter_id.com_object)
        # # # # Autogenerated comment: 
        # # some methods require a system service call as the methods expects a vb array object
        # # passed to it and there is no way to do this directly with python. In those cases the following code
        # # should be uncommented and edited accordingly. Otherwise completely remove all this.
        # # vba_function_name = 'remove'
        # # vba_code = """
        # # Public Function remove(defeaturing_filters)
        # #     Dim iFilterId (2)
        # #     defeaturing_filters.Remove iFilterId
        # #     remove = iFilterId
        # # End Function
        # # """

        # # system_service = SystemService(self.application.SystemService)
        # # return system_service.evaluate(vba_code, 0, vba_function_name, [self.com_object])

    def __repr__(self):
        return f'DefeaturingFilters(name="{self.name}")'
