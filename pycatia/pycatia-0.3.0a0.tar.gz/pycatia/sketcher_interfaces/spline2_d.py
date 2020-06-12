#! usr/bin/python3.6
"""
    Module initially auto generated using V5Automation files from CATIA V5 R28 on 2020-06-11 12:40:47.360445

    .. warning::
        The notes denoted "CAA V5 Visual Basic Help" are to be used as reference only.
        They are there as a guide as to how the visual basic / catscript functions work
        and thus help debugging in pycatia.
        
"""
from pycatia.sketcher_interfaces.curve2_d import Curve2D


class Spline2D(Curve2D):
    """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445)

                | System.IUnknown
                |     System.IDispatch
                |         System.CATBaseUnknown
                |             System.CATBaseDispatch
                |                 System.AnyObject
                |                     SketcherInterfaces.GeometricElement
                |                         SketcherInterfaces.Geometry2D
                |                             SketcherInterfaces.Curve2D
                |                                 Spline2D
                | 
                | Class defining a spline in 2D Space.
                | A 2D spline is defined by its constituting control points.
    
    """

    def __init__(self, com_object):
        super().__init__(com_object)
        self.spline2_d = com_object

    def get_control_points(self, o_ctrl_points):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445))
                | o Sub GetControlPoints(CATSafeArrayVariant oCtrlPoints)
                | 
                |     Returns the control points making up the spline.
                | 
                |     Parameters:
                | 
                |         oCtrlPoints
                |             The control points of the spline
                | 
                |             Example:
                |                 The following example fetches the list of control points
                |                 defining the
                |                 splinemySpline:
                | 
                |                  mySpline.GetControlPoints ControlPoints

        :param tuple o_ctrl_points:
        :return: None
        """
        return self.spline2_d.GetControlPoints(o_ctrl_points)
        # # # # Autogenerated comment: 
        # # some methods require a system service call as the methods expects a vb array object
        # # passed to it and there is no way to do this directly with python. In those cases the following code
        # # should be uncommented and edited accordingly. Otherwise completely remove all this.
        # # vba_function_name = 'get_control_points'
        # # vba_code = """
        # # Public Function get_control_points(spline2_d)
        # #     Dim oCtrlPoints (2)
        # #     spline2_d.GetControlPoints oCtrlPoints
        # #     get_control_points = oCtrlPoints
        # # End Function
        # # """

        # # system_service = SystemService(self.application.SystemService)
        # # return system_service.evaluate(vba_code, 0, vba_function_name, [self.com_object])

    def get_number_of_control_points(self):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445))
                | o Func GetNumberOfControlPoints() As double
                | 
                |     Returns the number of Control Points of the Spline
                | 
                |     Parameters:
                | 
                |         oNumber
                |             The number of control points*

        :return: float
        """
        return self.spline2_d.GetNumberOfControlPoints()

    def insert_control_point_after(self, i_ctrl_point, i_position):
        """
        .. note::
            CAA V5 Visual Basic Help (2020-06-11 12:40:47.360445))
                | o Sub InsertControlPointAfter(Point2D iCtrlPoint,
                | long iPosition)
                | 
                |     Inserts control points in the spline. If a 2D point is given (and not a
                |     control
                |     point), a new control point is created and aggregated in the
                |     spline.
                | 
                |     Parameters:
                | 
                |         iCtrlPoint
                |             The new point to be inserted. (@see CATIAPoint2D and
                |             CATIAControlPoint2D
                |             for more information). 
                |         iPosition
                |             The position at which to insert the point.
                |             To insert a new control point as the first element, set iPosition
                |             to 0.
                | 
                |             Example:
                |                 The following example inserts a control point myCtrlPoint as
                |                 the second
                |                 element of the splinemySpline:
                | 
                |                  call mySpline.InsertControlPointAfter (myCtrlPoint,
                |                  1)

        :param Point2D i_ctrl_point:
        :param int i_position:
        :return: None
        """
        return self.spline2_d.InsertControlPointAfter(i_ctrl_point.com_object, i_position)
        # # # # Autogenerated comment: 
        # # some methods require a system service call as the methods expects a vb array object
        # # passed to it and there is no way to do this directly with python. In those cases the following code
        # # should be uncommented and edited accordingly. Otherwise completely remove all this.
        # # vba_function_name = 'insert_control_point_after'
        # # vba_code = """
        # # Public Function insert_control_point_after(spline2_d)
        # #     Dim iCtrlPoint (2)
        # #     spline2_d.InsertControlPointAfter iCtrlPoint
        # #     insert_control_point_after = iCtrlPoint
        # # End Function
        # # """

        # # system_service = SystemService(self.application.SystemService)
        # # return system_service.evaluate(vba_code, 0, vba_function_name, [self.com_object])

    def __repr__(self):
        return f'Spline2D(name="{self.name}")'
