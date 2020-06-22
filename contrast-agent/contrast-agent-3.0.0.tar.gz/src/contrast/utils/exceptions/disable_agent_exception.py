# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
class DisableAgentException(Exception):
    def __init__(self):
        message = "Contrast Agent is turning off."
        super(DisableAgentException, self).__init__(message)
