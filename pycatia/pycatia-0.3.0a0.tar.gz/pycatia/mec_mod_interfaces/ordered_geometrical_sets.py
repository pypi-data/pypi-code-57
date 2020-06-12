#! /usr/bin/python3.6
# module initially auto generated using V5Automation.chm from CATIA R25

from pycatia.system_interfaces.collection import Collection
from .ordered_geometrical_set import OrderedGeometricalSet


class OrderedGeometricalSets(Collection):
    """
        .. note::
            CAA V5 Visual Basic help

                | A collection of the OrderedGeometricalSet objects.

    """

    def __init__(self, collection_com_object):
        super().__init__(collection_com_object, child_object=OrderedGeometricalSet)
        self.ordered_geometrical_sets = collection_com_object

    def add(self):
        """
        .. note::
            CAA V5 Visual Basic help

                | Add
                | o Func Add() As
                | 
                | Creates a new ordered geometrical set and adds it to the
                | OrderedGeometricalSets collection. This ordered geometrical set becomes
                | the current one  Returns:  The created ordered geometrical set
                |
                | Example:
                | The following example creates a ordered geometrical set named
                | newOrderedGeometricalSet in the ordered geometrical set collection of
                | the rootPart part in the partDoc part document. NewPartBody becomes
                | the in work object of partDoc.
                | Set NewPartBody = rootPart.OrderedGeometricalSets.Add()

        """
        return self.child_object(self.ordered_geometrical_sets.Add())

    def item(self, i_index):
        """
        .. note::
            CAA V5 Visual Basic help

                | Item
                | o Func Item(iIndex) As OrderedGeometricalSet
                | 
                | Returns a ordered geometrical set using its index or its name from the
                | ordered geometrical set collection.


                | Parameters:
                | iIndex
                |    The index or the name of the ordered geometrical set to retrieve from
                |    the collection of ordered geometrical sets.
                |    As a numeric, this index is the rank of the ordered geometrical set
                |    in the collection.
                |    The index of the first ordered geometrical set in the collection is 1, and
                |    the index of the last ordered geometrical set is Count.
                |    As a string, it is the name you assigned to the ordered geometrical set using
                |    the 
                | 
                |  property. 
                |    Returns:
                |   The retrieved ordered geometrical set


                | Examples:
                | 
                | 
                | This example retrieves in ThisOrderedGeometricalSet the fifth ordered geometrical set
                | in the collection and in ThatOrderedGeometricalSet the ordered geometrical set
                | named MyOrderedGeometricalSet in the ordered geometrical set collection of the partDoc
                | part document.
                | 
                | Set orderedGeometricalSetColl = partDoc.Part.OrderedGeometricalSets
                | Set ThisOrderedGeometricalSet = orderedGeometricalSetColl.Item(5)
                | Set ThatOrderedGeometricalSet = orderedGeometricalSetColl.Item("MyOrderedGeometricalSet")

        :return: OrderedGeometricalSet()
        """
        return self.child_object(self.ordered_geometrical_sets.Item(i_index))

    def __repr__(self):
        return f'OrderedGeometricalSets(name="{self.name}")'
