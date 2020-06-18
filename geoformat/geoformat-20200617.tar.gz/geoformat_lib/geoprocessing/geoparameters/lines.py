

def line_parameters(segment):
    """
    Deduces from a segment lines (slope and  intercept) parameters passing through this segment

    :param segment: input segment
    :return: a dict with two linears parameters : slope AND y_intercept
    """

    ((x_a, y_a), (x_b, y_b)) = segment
    if x_b != x_a:
        a = (y_b - y_a) / (x_b - x_a)
        b = y_a - (x_a * a)
    else:
        a = 'VERTICAL'
        b = x_a

    return {'slope': a, 'intercept': b}


def perpendicular_line_parameters_at_point(line_parameters, point):
    """
    Gives perpendicular lines parameters of a line passing through a point from an original line parameters

    :param line_parameters: original line parameter
    :param point: point of origin which serves as a pivot for calculating the parameters of perpendicular lines
    :return:
    """

    a = line_parameters['slope']

    x_a, y_a = point
    if a == 0.:
        a_bis = 'VERTICAL'
        b_bis = x_a
    elif a == 'VERTICAL':
        a_bis = 0.
        b_bis = y_a
    else:
        a_bis = -1 / a
        b_bis = y_a - (x_a * a_bis)

    return {"slope": a_bis, 'intercept': b_bis}


def point_at_distance_with_line_parameters(start_point, line_parameters, distance, offset_distance=None):
    """
    Returns a point at distance to a input_point with a direction define by line parameters.
    Distance can be negative.
    optional: add an offset distance (perpendicular to line_parameters value)

    :param start_point: input start_point
    :param line_parameters: line parameter that define direction to the new start_point
    :param distance: distance between input start_point to output start_point
    :param offset_distance: in option you can add a perpendicular offset input start_point
    :return: output start_point
    """

    a = line_parameters['slope']
    b = line_parameters['intercept']

    x_a, y_a = start_point
    if a == 'VERTICAL':
        x_b = x_a
        y_b = y_a + distance
    else:
        x_b = x_a + (distance / ((1 + a ** 2) ** 0.5))
        y_b = a * x_b + b

    ouput_point = x_b, y_b

    if offset_distance:
        perpendicular_parameter = perpendicular_line_parameters_at_point(line_parameters, ouput_point)
        offset_x, offset_y = point_at_distance_with_line_parameters(ouput_point, perpendicular_parameter,
                                                                    distance=offset_distance, offset_distance=None)
        ouput_point = offset_x, offset_y

    return ouput_point


def crossing_point_from_lines_parameters(line_parameter_a, line_parameter_b):
    """
    Return point coordinates that crossing two lines (if possible: slope must be different).
    If lines are parallel the function returns None

    :param line_parameter_a: parameters for line a
    :param line_parameter_b: parameters for line b
    :return: intersecting point between two lines
    """
    # slope must be different
    if line_parameter_a['slope'] != line_parameter_b['slope']:
        # define x
        if line_parameter_a['slope'] == 'VERTICAL':
            point_x = line_parameter_a['intercept']
        elif line_parameter_b['slope'] == 'VERTICAL':
            point_x = line_parameter_b['intercept']
        else:
            point_x = (line_parameter_a['intercept'] - line_parameter_b['intercept']) / (line_parameter_b['slope'] - line_parameter_a['slope'])

        # define y
        if line_parameter_a['slope'] == 'VERTICAL':
            point_y = line_parameter_b['slope'] * point_x + line_parameter_b['intercept']
        else:
            point_y = line_parameter_a['slope'] * point_x + line_parameter_a['intercept']

        return point_x, point_y
