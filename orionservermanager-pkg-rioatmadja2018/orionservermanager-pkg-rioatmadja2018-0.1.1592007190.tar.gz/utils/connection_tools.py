#!/usr/bin/env python
"""
Name: Rio Atmadja
Date: 02 April 2020
Description: The program is a helper for the ssh connection
"""
def check_connection(**connections):
    """
    This function will validate ssh connection
    :param connections: kwargs arguments
    :return:
    """
    err_msg = connections.get('err_msg')
    conn = connections.get('connection')

    if not err_msg and not conn:
        raise ValueError(f"connection and err_msg must be supplied")

    try:
        return conn
    except ConnectionError as e:
        raise ConnectionError(err_msg) from e



