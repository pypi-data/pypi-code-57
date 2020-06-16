def pages_screens_compass(rows):
    """
    Keep pages, screens and compass events
    :param rows:
    :return:
    """
    rows = [row for row in rows
            if (
                row.get('type', '') == 'page'
                or row.get('type', '') == 'screen'
                or row.get('type', '') == 'compass'
            )
            ]
    return rows


def pages_screens(rows):
    """
    Keep pages and screens events
    :param rows:
    :return:
    """
    rows = [row for row in rows
            if (
                row.get('type', '') == 'page'
                or row.get('type', '') == 'screen'
            )
            ]
    return rows
