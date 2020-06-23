# Copyright 2020 Cisco Systems, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

'''

File containing general utility functions.
'''
import csv
import yaml
from workload_auto import logger

LOG = logger.get_logging(__name__)

def csv_file_read(filename):
    '''
    Function to read the CSV file.
    '''
    try:
        with open(filename, newline='') as csvfile:
            csvfile.seek(0)
            reader = csv.DictReader(csvfile)
            csv_list = []
            for row in reader:
                csv_map = {}
                for key, val in row.items():
                    csv_map.update({key.strip(): val.strip()})
                csv_list.append(csv_map)
            return csv_list, None
    except Exception as exc:
        LOG.error("CSV file read exception %s", exc)
        return [], exc

def yml_file_read(filename):
    '''
    Function to read the YML file.
    '''
    try:
        with open(filename, 'r') as file_desc:
            file_dict = yaml.full_load(file_desc)
            return file_dict, None
    except Exception as exc:
        LOG.error("YML file read exception %s", exc)
        return {}, exc
