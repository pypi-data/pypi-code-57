# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import abc

from contrast.extern import six


@six.add_metaclass(abc.ABCMeta)
class BaseResponseWrapper(object):
    @abc.abstractmethod
    def set_status(self):
        pass

    @abc.abstractmethod
    def set_code(self):
        pass

    @abc.abstractmethod
    def set_body(self):
        pass

    @abc.abstractmethod
    def set_header(self):
        pass
