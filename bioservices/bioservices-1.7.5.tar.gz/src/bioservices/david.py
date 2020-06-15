#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
#$Id$

from bioservices import WSDLService
from bioservices import logger
logger.name = __name__


class David(WSDLService):
    _url = "https://david.ncifcrf.gov/webservice/services/DAVIDWebService?wsdl"
    def __init__(self, verbose=False):
        """.. rubric:: Constructor

        :param bool verbose:

        """
        super(David, self).__init__(name="David", url=David._url,
            verbose=verbose)

    def getCompleteEntity(self):
        res = self.serv.getConversionTypes()
        return res
















