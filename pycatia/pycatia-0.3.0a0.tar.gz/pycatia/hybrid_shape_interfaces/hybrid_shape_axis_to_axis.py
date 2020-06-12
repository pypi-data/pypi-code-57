#! usr/bin/python3.6
"""
    Module initially auto generated using V5Automation files from CATIA V5 R28 on 2020-06-11 12:40:47.360445

    .. warning::
        The notes denoted "CAA V5 Visual Basic Help" are to be used as reference only.
        They are there as a guide as to how the visual basic / catscript functions work
        and thus help debugging in pycatia.
        
"""

from pycatia.in_interfaces.reference import Reference
from pycatia.mec_mod_interfaces.hybrid_shape import HybridShape


class HybridShapeAxisToAxis(HybridShape):

    """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)

                | System.IUnknown
                |     System.IDispatch
                |         System.CATBaseUnknown
                |             System.CATBaseDispatch
                |                 System.AnyObject
                |                     MecModInterfaces.HybridShape
                |                         HybridShapeAxisToAxis
                | 
                | Represents the hybrid shape axis to axis transformation feature
                | object.
                | Role: To access the data of the axis to axis transformation shape feature
                | object. The data includes:
                | 
                |     The element to be transformed
                |     The reference axis system
                |     The target axis system
                | 
                | LICENSING INFORMATION: Creation of volume result requires GSO
                | License
                | if GSO License is not granted , setting of Volume context has not
                | effect
                | Use the CATIAHybridShapeFactory to create HybridShapeFeature
                | object.
                | 
                | See also:
                |     HybridShapeFactory
    
    """

    def __init__(self, com_object):
        super().__init__(com_object)
        self.hybrid_shape_axis_to_axis = com_object

    @property
    def creation_mode(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property CreationMode() As boolean
                | 
                |     Returns or sets the creation mode(creation or
                |     modification).
                |     Legal values: True if the result is a creation feature and False if the
                |     result is a modification feature.
                | 
                |     Example:
                | 
                |           This example sets that the mode of
                |          the hybShpAxisToAxis hybrid shape axis to axis to
                |          creation
                |          
                | 
                |          hybShpAxisToAxis.CreationMode = True

        :return: bool
        """

        return self.hybrid_shape_axis_to_axis.CreationMode

    @creation_mode.setter
    def creation_mode(self, value):
        """
        :param bool value:
        """

        self.hybrid_shape_axis_to_axis.CreationMode = value

    @property
    def elem_to_transform(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property ElemToTransform() As Reference
                | 
                |     Returns or sets the element to transform.
                | 
                |     Example:
                |         This example retrieves in Elem the element to transform for the
                |         AxisToAxis hybrid shape feature.
                | 
                |          Dim Elem As Reference
                |          Set Elem = AxisToAxis.ElemToTransform

        :return: Reference
        """

        return Reference(self.hybrid_shape_axis_to_axis.ElemToTransform)

    @elem_to_transform.setter
    def elem_to_transform(self, value):
        """
        :param Reference value:
        """

        self.hybrid_shape_axis_to_axis.ElemToTransform = value

    @property
    def reference_axis(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property ReferenceAxis() As Reference
                | 
                |     Returns or sets the reference axis.
                | 
                |     Example:
                |         This example retrieves in Ref the reference axis for the AxisToAxis
                |         hybrid shape feature.
                | 
                |          Dim Ref As Reference
                |          Set Ref = AxisToAxis.ReferenceAxis

        :return: Reference
        """

        return Reference(self.hybrid_shape_axis_to_axis.ReferenceAxis)

    @reference_axis.setter
    def reference_axis(self, value):
        """
        :param Reference value:
        """

        self.hybrid_shape_axis_to_axis.ReferenceAxis = value

    @property
    def target_axis(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property TargetAxis() As Reference
                | 
                |     Returns or sets the target axis.
                | 
                |     Example:
                |         This example retrieves in Ref the target axis for the AxisToAxis hybrid
                |         shape feature.
                | 
                |          Dim Ref As Reference
                |          Set Ref = AxisToAxis.ReferenceAxis

        :return: Reference
        """

        return Reference(self.hybrid_shape_axis_to_axis.TargetAxis)

    @target_axis.setter
    def target_axis(self, value):
        """
        :param Reference value:
        """

        self.hybrid_shape_axis_to_axis.TargetAxis = value

    @property
    def volume_result(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property VolumeResult() As boolean
                | 
                |     Returns or sets the volume result.
                |     Legal values: True if the result of axis to axis transformation is required
                |     as volume (option is effective only in case of volumes,requires GSO License))
                |     and False if it is needed as surface .
                | 
                |     Example:
                | 
                |           This example sets that the result of
                |          the hybShpAxisToAxis hybrid shape AxisToAxis is
                |          volume.
                |          
                | 
                |          hybShpAxisToAxis.VolumeResult = True

        :return: bool
        """

        return self.hybrid_shape_axis_to_axis.VolumeResult

    @volume_result.setter
    def volume_result(self, value):
        """
        :param bool value:
        """

        self.hybrid_shape_axis_to_axis.VolumeResult = value

    def __repr__(self):
        return f'HybridShapeAxisToAxis(name="{ self.name }")'
