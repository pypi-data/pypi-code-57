#! usr/bin/python3.6
"""
    Module initially auto generated using V5Automation files from CATIA V5 R28 on 2020-06-11 12:40:47.360445

    .. warning::
        The notes denoted "CAA V5 Visual Basic Help" are to be used as reference only.
        They are there as a guide as to how the visual basic / catscript functions work
        and thus help debugging in pycatia.
        
"""

from pycatia.hybrid_shape_interfaces.hybrid_shape_direction import HybridShapeDirection
from pycatia.in_interfaces.reference import Reference
from pycatia.knowledge_interfaces.length import Length
from pycatia.mec_mod_interfaces.hybrid_shape import HybridShape


class HybridShapeTranslate(HybridShape):

    """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)

                | System.IUnknown
                |     System.IDispatch
                |         System.CATBaseUnknown
                |             System.CATBaseDispatch
                |                 System.AnyObject
                |                     MecModInterfaces.HybridShape
                |                         HybridShapeTranslate
                | 
                | Represents the hybrid shape translate feature object.
                | Role: To access the data of the hybrid shape translate feature object. This
                | data includes:
                | 
                |     The element to translate
                |     The translation direction
                |     The translation distance and its value
                | 
                | LICENSING INFORMATION: Creation of volume result requires GSO
                | License
                | if GSO License is not granted , setting of Volume context has not
                | effect
                | 
                | Use the CATIAHybridShapeFactory to create HybridShapeFeature
                | object.
                | 
                | See also:
                |     HybridShapeFactory
    
    """

    def __init__(self, com_object):
        super().__init__(com_object)
        self.hybrid_shape_translate = com_object

    @property
    def coord_x_value(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property CoordXValue() As double
                | 
                |     Returns or sets the translate X coordinate value.

        :return: float
        """

        return self.hybrid_shape_translate.CoordXValue

    @coord_x_value.setter
    def coord_x_value(self, value):
        """
        :param float value:
        """

        self.hybrid_shape_translate.CoordXValue = value

    @property
    def coord_y_value(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property CoordYValue() As double
                | 
                |     Returns or sets the translate Y coordinate value.

        :return: float
        """

        return self.hybrid_shape_translate.CoordYValue

    @coord_y_value.setter
    def coord_y_value(self, value):
        """
        :param float value:
        """

        self.hybrid_shape_translate.CoordYValue = value

    @property
    def coord_z_value(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property CoordZValue() As double
                | 
                |     Returns or sets the translate Z coordinate value.

        :return: float
        """

        return self.hybrid_shape_translate.CoordZValue

    @coord_z_value.setter
    def coord_z_value(self, value):
        """
        :param float value:
        """

        self.hybrid_shape_translate.CoordZValue = value

    @property
    def direction(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property Direction() As HybridShapeDirection
                | 
                |     Returns or sets the translate direction.
                | 
                |     Example
                |         This example retrieves in Dir the translation direction for the
                |         Translate hybrid shape feature.
                | 
                |          Dim Dir As CATIAHybridShapeDirection
                |          Set Dir=Translate.Direction

        :return: HybridShapeDirection
        """

        return HybridShapeDirection(self.hybrid_shape_translate.Direction)

    @direction.setter
    def direction(self, value):
        """
        :param HybridShapeDirection value:
        """

        self.hybrid_shape_translate.Direction = value

    @property
    def distance(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property Distance() As Length (Read Only)
                | 
                |     Returns the translate distance.

        :return: Length
        """

        return Length(self.hybrid_shape_translate.Distance)

    @property
    def distance_value(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property DistanceValue() As double
                | 
                |     Returns or sets the translate distance value.
                | 
                |     Example
                |         This example retrieves in DistVal the translation distance value for
                |         the Translate hybrid shape feature.
                | 
                |          Dim DistVal As double
                |          Set DistVal =Translate.DistanceValue

        :return: float
        """

        return self.hybrid_shape_translate.DistanceValue

    @distance_value.setter
    def distance_value(self, value):
        """
        :param float value:
        """

        self.hybrid_shape_translate.DistanceValue = value

    @property
    def elem_to_translate(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property ElemToTranslate() As Reference
                | 
                |     Returns or sets the element to translate.
                | 
                |     Example
                |         This example retrieves in Element the element to be translated for the
                |         Translate hybrid shape feature.
                | 
                |          Dim Element As Reference
                |          Set Element=Translate.ElemToTranslate

        :return: Reference
        """

        return Reference(self.hybrid_shape_translate.ElemToTranslate)

    @elem_to_translate.setter
    def elem_to_translate(self, value):
        """
        :param Reference value:
        """

        self.hybrid_shape_translate.ElemToTranslate = value

    @property
    def first_point(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property FirstPoint() As Reference
                | 
                |     Returns or sets the first point defining the translation.

        :return: Reference
        """

        return Reference(self.hybrid_shape_translate.FirstPoint)

    @first_point.setter
    def first_point(self, value):
        """
        :param Reference value:
        """

        self.hybrid_shape_translate.FirstPoint = value

    @property
    def ref_axis_system(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property RefAxisSystem() As Reference
                | 
                |     Returns or Sets the reference Axis System for Translate
                |     feature.
                |     This data is not mandatory, if element is null, the absolute axis system is
                |     taken.
                |     When an element is given, X, Y and Z are considered in this Axis system.
                |     
                | Example
                | :
                |     This example retrieves in oRefAxis the reference Axis System for Translate
                |     feature.
                | 
                |      Dim oRefAxis As CATIAReference
                |      Set oRefAxis  = Translate.RefAxisSystem

        :return: Reference
        """

        return Reference(self.hybrid_shape_translate.RefAxisSystem)

    @ref_axis_system.setter
    def ref_axis_system(self, value):
        """
        :param Reference value:
        """

        self.hybrid_shape_translate.RefAxisSystem = value

    @property
    def second_point(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property SecondPoint() As Reference
                | 
                |     Returns or sets the second point defining the translation.

        :return: Reference
        """

        return Reference(self.hybrid_shape_translate.SecondPoint)

    @second_point.setter
    def second_point(self, value):
        """
        :param Reference value:
        """

        self.hybrid_shape_translate.SecondPoint = value

    @property
    def vector_type(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property VectorType() As long
                | 
                |     Returns or sets the way the translation vector is defined.
                | 
                |         0= Direction + distance
                |         1= point + points
                |         2= coordinates
                |         3= Unknown type

        :return: int
        """

        return self.hybrid_shape_translate.VectorType

    @vector_type.setter
    def vector_type(self, value):
        """
        :param int value:
        """

        self.hybrid_shape_translate.VectorType = value

    @property
    def volume_result(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)
                | o Property VolumeResult() As boolean
                | 
                |     Returns or sets the volume result.
                |     Legal values: True if the result of translation is required as volume
                |     (option is effective only in case of volumes,requires GSO License) and False if
                |     it is needed as surface .
                | 
                |     Example:
                | 
                |           This example sets that the result of
                |          the hybShpTranslate hybrid shape translate is volume.
                |          
                | 
                |          hybShpTranslate.VolumeResult = True

        :return: bool
        """

        return self.hybrid_shape_translate.VolumeResult

    @volume_result.setter
    def volume_result(self, value):
        """
        :param bool value:
        """

        self.hybrid_shape_translate.VolumeResult = value

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
                |     This example retrieves in oCreation the creation mode for the
                |     hybShpTranslate hybrid shape feature.
                | 
                |      oCreation = hybShpTranslate.GetCreationMode

        :return: int
        """
        return self.hybrid_shape_translate.GetCreationMode()

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
                |          the hybShpTranslate hybrid shape translate to
                |          creation
                |          
                | 
                |          hybShpTranslate.SetCreationMode True

        :param bool i_creation:
        :return: None
        """
        return self.hybrid_shape_translate.SetCreationMode(i_creation)
        # # # # Autogenerated comment: 
        # # some methods require a system service call as the methods expects a vb array object
        # # passed to it and there is no way to do this directly with python. In those cases the following code
        # # should be uncommented and edited accordingly. Otherwise completely remove all this.
        # # vba_function_name = 'set_creation_mode'
        # # vba_code = """
        # # Public Function set_creation_mode(hybrid_shape_translate)
        # #     Dim iCreation (2)
        # #     hybrid_shape_translate.SetCreationMode iCreation
        # #     set_creation_mode = iCreation
        # # End Function
        # # """

        # # system_service = SystemService(self.application.SystemService)
        # # return system_service.evaluate(vba_code, 0, vba_function_name, [self.com_object])

    def __repr__(self):
        return f'HybridShapeTranslate(name="{ self.name }")'
