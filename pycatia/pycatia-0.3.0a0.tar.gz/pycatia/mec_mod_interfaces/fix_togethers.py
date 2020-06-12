#! /usr/bin/python3.6
# module initially auto generated using V5Automation.chm from CATIA R25 on 2020-05-18 10:56:40.651039

from pycatia.system_interfaces.collection import Collection
from .fix_together import FixTogether


class FixTogethers(Collection):
    """
        .. note::
            CAA V5 Visual Basic help

                | A collection of all the FixTogether objects contained in the product.

    """

    def __init__(self, com_object):
        super().__init__(com_object, child_object=FixTogether)
        self.fix_togethers = com_object

    def add(self):
        """
        .. note::
            CAA V5 Visual Basic help

                | Add
                | o Func Add() As
                | 
                | Creates a new FixTogether and adds it to the FixTogethers
                | collection. Returns: The created FixTogether
                |
                | Example:
                | The following example creates a FixTogether newFixTogether in
                | the FixTogether collection.
                | Set newFixTogether = fixTogethers.Add

        :return: FixTogether()
        """
        return self.child_object(self.fix_togethers.Add())

    def item(self, i_index):
        """
        .. note::
            CAA V5 Visual Basic help

                | Item
                | o Func Item(iIndex) As
                | 
                | Returns a FixTogether using its index or its name from the
                | FixTogethers collection.
                |
                | Parameters:
                | iIndex
                |    The index or the name of the FixTogether to retrieve from
                |    the collection of FixTogether.
                |    As a numerics, this index is the rank of the FixTogether
                |    in the collection.
                |    The index of the first FixTogether in the collection is 1, and
                |    the index of the last FixTogether is Count.
                |    As a string, it is the name you assigned to the FixTogether using
                |    the property.
                | Returns:
                |    The retrieved FixTogether
                |
                | Examples:
                | This example retrieves in thisFixTogether the fifth
                | FixTogether in the collection and in thatFixTogether the
                | FixTogether named MyFixTogether in the FixTogether
                | collection of the product product.
                | Set fixTogetherColl = product.FixTogethers
                | Set thisFixTogether = fixTogetherColl.Item(5)
                | Set thatFixTogether = fixTogetherColl.Item("MyFixTogether")

        :param int i_index:
        :return: FixTogether()
        """
        return self.child_object(self.fix_togethers.Item(i_index))

    def remove(self, i_index):
        """
        .. note::
            CAA V5 Visual Basic help

                | Remove
                | o Sub Remove(iIndex)
                | 
                | Removes a FixTogether from the FixTogethers collection.
                |
                | Parameters:
                | iIndex
                |    The index or the name of the FixTogether to remove from the FixTogethers
                |    collection.
                |    As a numerics, this index is the rank of the FixTogether
                |    in the collection.
                |    The index of the first FixTogether in the collection is 1, and
                |    the index of the last FixTogether is Count.
                |    As a string, it is the name you assigned to the FixTogether using
                |    the property.
                |
                | Examples:
                | This example removes the last FixTogether in the collection.
                | fixTogetherColl.Remove(fixTogetherColl.Count)

        :param int i_index:
        :return:
        """

        self.fix_togethers.Remove(i_index)

    def __repr__(self):
        return f'FixTogethers(name="{self.name}")'
