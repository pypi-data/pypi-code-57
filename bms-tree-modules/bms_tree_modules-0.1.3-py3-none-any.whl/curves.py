from typing import Callable


class CurveConfig(object):
    CONST_CURVES = "curve_assignments"
    CONST_SLOT_KEY = "curve_slot_key"
    CONST_CURVE = "curve_assigned"
    CONST_COEFFICIENTS = "coefficients"

    def __init__(self, period_input):
        # initialize curves
        self.curves: dict = {}

        # process period_input and convert into objects
        self.__check_input(period_input)

    def __check_input(self, period_input):
        if isinstance(period_input, dict):
            if self.CONST_CURVES not in period_input.keys():
                raise AttributeError(
                    "period_input <class 'dict'> has not attribute '{0}'".format(
                        self.CONST_CURVES
                    )
                )

            for curve in period_input[self.CONST_CURVES]:
                keys = curve.keys()

                if self.CONST_SLOT_KEY not in keys:
                    raise AttributeError(
                        "curve_input <class 'dict has not attribute '{0}'".format(  # noqa: E501
                            self.CONST_SLOT_KEY
                        )
                    )

                if self.CONST_CURVE not in keys:
                    raise AttributeError(
                        "curve_input <class 'dict has not attribute '{0}'".format(  # noqa: E501
                            self.CONST_CURVE
                        )
                    )

                curve_assigned_keys = curve[self.CONST_CURVE].keys()
                if self.CONST_COEFFICIENTS not in curve_assigned_keys:
                    raise AttributeError(
                        "curve_assigned_input <class 'dict has not attribute '{0}'".format(  # noqa: E501
                            self.CONST_COEFFICIENTS
                        )
                    )

            self.from_dict(period_input)

    def from_dict(self, period_input: dict):
        for curve in period_input[self.CONST_CURVES]:
            # the name of the curve in the Python Model i.e. the curve slot key
            curve_name = curve[self.CONST_SLOT_KEY]

            # the function coefficients as array (e.g., [1, 0, 2])
            coefficients = curve[self.CONST_CURVE][self.CONST_COEFFICIENTS]

            # the create lambda function
            self.curves[curve_name] = self.coefficients_to_lambda_function(coefficients)

    def coefficients_to_lambda_function(self, coefficients) -> Callable:
        """Create a lambda function given a curve configuration.

        Parameters:
        - coefficients: an array of coefficients (e.g., [2,3,4])

        Returns: a lambda function representing the curve

        Example: lambda x: 2 + 3*x + 4*x**2
        """
        return lambda x: sum(
            coefficient * x ** index for index, coefficient in enumerate(coefficients)
        )
