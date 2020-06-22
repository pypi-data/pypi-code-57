#!/usr/bin/env python

# (C) Copyright 2018 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import cdsapi

c = cdsapi.Client()

c.retrieve("reanalysis-era5-complete",
           {

               'class': 'ea',
               'expver': '5',
               'stream': 'oper',
               'type': 'fc',
               'step': '3/to/12/by/3',
               'param': '130.128',
               'levtype': 'ml',
               'levelist': '1/10/50/100',
               'date': '2020-06-01',
               'time': '06/18',
               'area': '80/-50/-25/0',  # North, West, South, East. Default: global
               'grid': '1.0/1.0',  # Latitude/longitude grid: east-west (longitude) and north-south resolution (latitude). Default: reduced Gaussian grid
           },
           'x.grib')
