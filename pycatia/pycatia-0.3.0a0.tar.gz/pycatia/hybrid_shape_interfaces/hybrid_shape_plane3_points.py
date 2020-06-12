#! usr/bin/python3.6
"""
    Module initially auto generated using V5Automation files from CATIA V5 R28 on 2020-06-11 12:40:47.360445

    .. warning::
        The notes denoted "CAA V5 Visual Basic Help" are to be used as reference only.
        They are there as a guide as to how the visual basic / catscript functions work
        and thus help debugging in pycatia.
        
"""

from pycatia.hybrid_shape_interfaces.plane import Plane
from pycatia.in_interfaces.reference import Reference


class HybridShapePlane3Points(Plane):

    """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)

                | System.IUnknown
                |     System.IDispatch
                |         System.CATBaseUnknown
                |             System.CATBaseDispatch
                |                 System.AnyObject
                |                     MecModInterfaces.HybridShape
                |                         CATGSMIDLItf.Plane
                |                             HybridShapePlane3Points
                | 
                | Represents the hybrid shape plane through three points feature
                | object.
                | Role: Allows to access data of the plane feature passing though three points.
                | This data includes:
                | 
                |     The first point
                |     The second point
                |     The third point
                | 
                | Use the CATIAHybridShapeFactory to create HybridShapeFeature
                | object.
                | 
                | See also:
                |     HybridShapeFactory
    
    """

    def __init__(self, com_object):
        super().__init__(com_object)
        self.hybrid_shape_plane3_points = com_object

    @property
    def first(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property First() As Reference
                | 
                |     Returns or sets the first point.
                |     Sub-element(s) supported (see Boundary object): Vertex.
                | 
                |     Example: This example retrieves in FirstPoint the first point for the Plane
                |     passing through three points hybrid shape feature.
                | 
                |      Dim FirstPoint As Reference
                |      Set FirstPoint = Plane3Points.First

        :return: Reference
        """

        return Reference(self.hybrid_shape_plane3_points.First)

    @first.setter
    def first(self, value):
        """
        :param Reference value:
        """

        self.hybrid_shape_plane3_points.First = value

    @property
    def second(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property Second() As Reference
                | 
                |     Returns or sets the second point.
                |     Sub-element(s) supported (see Boundary object): Vertex.
                | 
                |     Example: This example retrieves in SecondPoint the second point for the
                |     Plane passing through three points hybrid shape feature.
                | 
                |      Dim SecondPoint As Reference
                |      Set SecondPoint = Plane3Points.Second

        :return: Reference
        """

        return Reference(self.hybrid_shape_plane3_points.Second)

    @second.setter
    def second(self, value):
        """
        :param Reference value:
        """

        self.hybrid_shape_plane3_points.Second = value

    @property
    def third(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property Third() As Reference
                | 
                |     Returns or sets the third point.
                |     Sub-element(s) supported (see Boundary object): Vertex.
                | 
                |     Example: This example retrieves in ThirdPoint the third point for the Plane
                |     passing through three points hybrid shape feature.
                | 
                |      Dim ThridPoint As Reference
                |      Set ThirdPoint = Plane3Points.Third

        :return: Reference
        """

        return Reference(self.hybrid_shape_plane3_points.Third)

    @third.setter
    def third(self, value):
        """
        :param Reference value:
        """

        self.hybrid_shape_plane3_points.Third = value

    def __repr__(self):
        return f'HybridShapePlane3Points(name="{ self.name }")'
