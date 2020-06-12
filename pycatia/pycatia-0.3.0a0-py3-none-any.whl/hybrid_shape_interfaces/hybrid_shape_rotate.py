#! usr/bin/python3.6
"""
    Module initially auto generated using V5Automation files from CATIA V5 R28 on 2020-06-11 12:40:47.360445

    .. warning::
        The notes denoted "CAA V5 Visual Basic Help" are to be used as reference only.
        They are there as a guide as to how the visual basic / catscript functions work
        and thus help debugging in pycatia.
        
"""

from pycatia.in_interfaces.reference import Reference
from pycatia.knowledge_interfaces.angle import Angle
from pycatia.mec_mod_interfaces.hybrid_shape import HybridShape


class HybridShapeRotate(HybridShape):

    """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)

                | System.IUnknown
                |     System.IDispatch
                |         System.CATBaseUnknown
                |             System.CATBaseDispatch
                |                 System.AnyObject
                |                     MecModInterfaces.HybridShape
                |                         HybridShapeRotate
                | 
                | Represents the hybrid shape rotate feature object.
                | Role: To access the data of the hybrid shape rotate feature object. This data
                | includes:
                | 
                |     The element to be rotated
                |     The rotation axis
                |     The angle and its value
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
        self.hybrid_shape_rotate = com_object

    @property
    def angle(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property Angle() As Angle (Read Only)
                | 
                |     Returns the rotation angle.

        :return: Angle
        """

        return Angle(self.hybrid_shape_rotate.Angle)

    @property
    def angle_value(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property AngleValue() As double
                | 
                |     Returns or sets the rotation angle value.
                | 
                |     Example: This example retrieves in AngleValue the angle value for the
                |     Rotate hybrid shape feature.
                | 
                |      Dim AngleValue As double
                |      Set AngleValue = Rotate.AngleValue

        :return: float
        """

        return self.hybrid_shape_rotate.AngleValue

    @angle_value.setter
    def angle_value(self, value):
        """
        :param float value:
        """

        self.hybrid_shape_rotate.AngleValue = value

    @property
    def axis(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property Axis() As Reference
                | 
                |     Returns or sets the rotation axis.
                |     Sub-element(s) supported (see Boundary object): Edge.
                | 
                |     Example: This example retrieves in RotationAxis the rotation axis for the
                |     Rotate hybrid shape feature.
                | 
                |      Dim RotationAxis As Reference
                |      Set RotationAxis = Rotate.Axis

        :return: Reference
        """

        return Reference(self.hybrid_shape_rotate.Axis)

    @axis.setter
    def axis(self, value):
        """
        :param Reference value:
        """

        self.hybrid_shape_rotate.Axis = value

    @property
    def elem_to_rotate(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property ElemToRotate() As Reference
                | 
                |     Returns or sets the element to be rotated.
                | 
                |     Example: This example retrieves in Elem the element to be rotated for the
                |     Rotate hybrid shape feature.
                | 
                |      Dim Elem As Reference
                |      Set Elem = Rotate.ElemToRotate

        :return: Reference
        """

        return Reference(self.hybrid_shape_rotate.ElemToRotate)

    @elem_to_rotate.setter
    def elem_to_rotate(self, value):
        """
        :param Reference value:
        """

        self.hybrid_shape_rotate.ElemToRotate = value

    @property
    def first_element(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property FirstElement() As Reference
                | 
                |     Returns or sets the first element defining the rotation angle.

        :return: Reference
        """

        return Reference(self.hybrid_shape_rotate.FirstElement)

    @first_element.setter
    def first_element(self, value):
        """
        :param Reference value:
        """

        self.hybrid_shape_rotate.FirstElement = value

    @property
    def first_point(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property FirstPoint() As Reference
                | 
                |     Returns or sets the first point defining the rotation.

        :return: Reference
        """

        return Reference(self.hybrid_shape_rotate.FirstPoint)

    @first_point.setter
    def first_point(self, value):
        """
        :param Reference value:
        """

        self.hybrid_shape_rotate.FirstPoint = value

    @property
    def orientation_of_first_element(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property OrientationOfFirstElement() As boolean
                | 
                |     Returns or sets the orientation of the first element defining the rotation
                |     angle.
                |     This applies in case of line or plane element.

        :return: bool
        """

        return self.hybrid_shape_rotate.OrientationOfFirstElement

    @orientation_of_first_element.setter
    def orientation_of_first_element(self, value):
        """
        :param bool value:
        """

        self.hybrid_shape_rotate.OrientationOfFirstElement = value

    @property
    def orientation_of_second_element(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property OrientationOfSecondElement() As boolean
                | 
                |     Returns or sets the orientation of the second element defining the rotation
                |     angle.
                |     This applies in case of line or plane element.

        :return: bool
        """

        return self.hybrid_shape_rotate.OrientationOfSecondElement

    @orientation_of_second_element.setter
    def orientation_of_second_element(self, value):
        """
        :param bool value:
        """

        self.hybrid_shape_rotate.OrientationOfSecondElement = value

    @property
    def rotation_type(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property RotationType() As long
                | 
                |     Returns or sets the type of the rotation definition.
                | 
                |         0= Axis + angle
                |         1= Axis + two elements
                |         2= Three Points
                |         3= Unknown type

        :return: int
        """

        return self.hybrid_shape_rotate.RotationType

    @rotation_type.setter
    def rotation_type(self, value):
        """
        :param int value:
        """

        self.hybrid_shape_rotate.RotationType = value

    @property
    def second_element(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property SecondElement() As Reference
                | 
                |     Returns or sets the second element defining the rotation angle.

        :return: Reference
        """

        return Reference(self.hybrid_shape_rotate.SecondElement)

    @second_element.setter
    def second_element(self, value):
        """
        :param Reference value:
        """

        self.hybrid_shape_rotate.SecondElement = value

    @property
    def second_point(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property SecondPoint() As Reference
                | 
                |     Returns or sets the second point defining the rotation.

        :return: Reference
        """

        return Reference(self.hybrid_shape_rotate.SecondPoint)

    @second_point.setter
    def second_point(self, value):
        """
        :param Reference value:
        """

        self.hybrid_shape_rotate.SecondPoint = value

    @property
    def third_point(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property ThirdPoint() As Reference
                | 
                |     Returns or sets the third point defining the rotation.

        :return: Reference
        """

        return Reference(self.hybrid_shape_rotate.ThirdPoint)

    @third_point.setter
    def third_point(self, value):
        """
        :param Reference value:
        """

        self.hybrid_shape_rotate.ThirdPoint = value

    @property
    def volume_result(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property VolumeResult() As boolean
                | 
                |     Returns or sets the volume result.
                |     Legal values: True if the result of Rotate is required as volume (option is
                |     effective only in case of volumes,requires GSO License) and False if it is
                |     needed as surface .
                | 
                |     Example:
                | 
                |           This example sets that the result of
                |          the hybShpRotate hybrid shape rotate is volume.
                |          
                | 
                |          hybShpRotate.VolumeResult = True

        :return: bool
        """

        return self.hybrid_shape_rotate.VolumeResult

    @volume_result.setter
    def volume_result(self, value):
        """
        :param bool value:
        """

        self.hybrid_shape_rotate.VolumeResult = value

    def get_creation_mode(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445))
                | o Func GetCreationMode() As long
                | 
                |     Gets the creation mode.
                |     Legal values:
                | 
                |     0
                |         CATGSMTransfoModeUnset. Default behavior: creation mode by default for
                |         all features, modification mode for axis system
                |     1
                |         CATGSMTransfoModeCreation. Creation mode. 
                |     2
                |         CATGSMTransfoModeModification. Modification mode. 
                | 
                | Example:
                |     This example retrieves in oCreation the creation mode for the hybShpRotate
                |     hybrid shape feature.
                | 
                |      oCreation = hybShpRotate.GetCreationMode

        :return: int
        """
        return self.hybrid_shape_rotate.GetCreationMode()

    def set_creation_mode(self, i_creation):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445))
                | o Sub SetCreationMode(boolean iCreation)
                | 
                |     Sets the creation mode(creation or modification).
                |     Legal values: True if the result is a creation feature and False if the
                |     result is a modification feature.
                | 
                |     Example:
                | 
                |           This example sets that the mode of
                |          the hybShpRotate hybrid shape rotate to creation
                |          
                | 
                |          hybShpRotate.SetCreationMode True

        :param bool i_creation:
        :return: None
        """
        return self.hybrid_shape_rotate.SetCreationMode(i_creation)
        # # # # Autogenerated comment: 
        # # some methods require a system service call as the methods expects a vb array object
        # # passed to it and there is no way to do this directly with python. In those cases the following code
        # # should be uncommented and edited accordingly. Otherwise completely remove all this.
        # # vba_function_name = 'set_creation_mode'
        # # vba_code = """
        # # Public Function set_creation_mode(hybrid_shape_rotate)
        # #     Dim iCreation (2)
        # #     hybrid_shape_rotate.SetCreationMode iCreation
        # #     set_creation_mode = iCreation
        # # End Function
        # # """

        # # system_service = SystemService(self.application.SystemService)
        # # return system_service.evaluate(vba_code, 0, vba_function_name, [self.com_object])

    def __repr__(self):
        return f'HybridShapeRotate(name="{ self.name }")'
