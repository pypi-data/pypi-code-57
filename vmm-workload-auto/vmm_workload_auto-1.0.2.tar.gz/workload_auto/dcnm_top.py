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
DCNM Top level class that instantiates the vSphere class based on the config
file. Also, instantiates the DCNM helper classes.
'''

import sys
from workload_auto import logger
from workload_auto import dcnm_helper
from workload_auto import vsph_handler
from workload_auto import utils
from workload_auto import rest

LOG = logger.get_logging(__name__)

class DcnmTop:
    '''
    Top level DCNM class that instantiates other classes.
    '''
    def __init__(self, conf_dict):
        '''
        Init function to instantiate all vsphere classes and calls configure
        in vsphere class that reads the spec file and attaches the networks.
        Finally, it calls the rest initialization routine.
        '''
        LOG.info("Initializing DCNM Top class conf is %s", conf_dict)
        self.conf_dict = conf_dict
        self.dcnm_vsph_dict = {}
        self.auto_deploy = self.conf_dict.get('AutoDeploy')
        if self.auto_deploy is None:
            self.auto_deploy = False
        #self.auto_deploy = auto_deploy_str == "True"
        try:
            ret = self.instantiate_all()
            if not ret:
                return
            # Need to find the right place to put this
            self.init_cfg_all()
            port = self.conf_dict.get('ListenPort')
            rest.rest_init(port, self.rest_handler)
        except Exception as exc:
            LOG.error("Exception raised in DCNM top. Instantiation failed "
                      "with %s", exc)
            return

    def rest_handler(self, op_type, data):
        '''
        Top Level Rest handler to call the appropriate routine based on the
        type.
        '''
        LOG.info("op is %s data %s", op_type, data)
        if op_type == "CLEAN":
            self.cleanup()
        elif op_type == "REFRESH":
            self.refresh()
        elif op_type == "RESYNC":
            self.resync()

    def check_dcnm_cfg(self, nwk_mgr_dict):
        '''
        Function to check if DCNM config has all the mandatory keys.
        '''
        if nwk_mgr_dict.get('Ip') is None or (
                nwk_mgr_dict.get('User') is None) or (
                    nwk_mgr_dict.get('Password') is None) or (
                        nwk_mgr_dict.get('CsvFile') is None):
            return False
        return True

    def check_vsph_cfg(self, vsph_dict):
        '''
        Function to check if vsphere config has all the mandatory keys.
        '''
        if vsph_dict.get('Ip') is None or (
                vsph_dict.get('User') is None) or (
                    vsph_dict.get('Password') is None):
            return False
        return True

    def validate_csv_values(self, csv_list):
        '''
        Validate the contents of CSV file.
        '''
        mand_set = set(['vCenter', 'Fabric', 'Network', 'Dvs', 'Dvs_pg',
                        'Host', 'Host_pg'])
        for csv_dict in csv_list:
            csv_keys = csv_dict.keys()
            if not mand_set.issubset(csv_keys):
                LOG.exception("Mandatory keys %s not present in CSV file",
                              mand_set)
                return False
            vcntr_ip = csv_dict.get('vCenter')
            if not vcntr_ip:
                LOG.exception("vCenter IP is empty in csv file")
                return False
            fabric = csv_dict.get('Fabric')
            if not fabric:
                LOG.exception("Fabric Name is empty in csv file")
                return False
            nwk_name = csv_dict.get('Network')
            if not nwk_name:
                LOG.exception("DCNM Nwk Name is empty in csv file")
                return False
            dvs_name = csv_dict.get('Dvs')
            dvs_pg = csv_dict.get('Dvs_pg')
            host_name = csv_dict.get('Host')
            host_pg = csv_dict.get('Host_pg')
            if not dvs_name and not host_name:
                LOG.exception("Both DVS and Host name is missing")
                return False
            if dvs_name:
                if not dvs_pg:
                    LOG.exception("Invalid DVS PG for DVS %s", dvs_name)
                    return False
            else:
                if not host_pg:
                    LOG.exception("Invalid Host PG for host %s", host_name)
                    return False
        return True

    def validate_cfg(self):
        '''
        Function to validate the config and CSV file. Exit, if error.
        '''
        dcnm_nwk_dict = {}
        for dcnm_ip, dcnm_dict in self.dcnm_vsph_dict.items():
            vsph_dict = dcnm_dict.get('vsph_dict')
            csv_file = dcnm_dict.get('csv_file')
            csv_list, exc = utils.csv_file_read(csv_file)
            if not csv_list:
                LOG.exception("Exception in CSV file read, %s", exc)
                sys.exit(1)
            if not self.validate_csv_values(csv_list):
                LOG.exception("Exception in CSV file contents")
                sys.exit(1)
            for csv_map in csv_list:
                nwk = csv_map.get('Network')
                fabric = csv_map.get('Fabric')
                vsph_dict = dcnm_dict.get('vsph_dict')
                if nwk not in dcnm_nwk_dict.keys():
                    if not dcnm_dict.get('obj').is_nwk_exist(fabric, nwk):
                        LOG.exception("DCNM Network %s unavailable for fab %s",
                                      nwk, fabric)
                        sys.exit(1)
                    dcnm_nwk_dict.update({nwk: True})
            for vsph_ip, vsph_obj in vsph_dict.items():
                if not vsph_obj.validate_cfg(csv_list):
                    LOG.exception("Validate vsphere cfg returned false "
                                  "for %s", vsph_ip)
                    sys.exit(1)
            self.dcnm_vsph_dict[dcnm_ip].update({'csv_list': csv_list})

    def cfg_all(self, read_cfg=False, enable=True):
        '''
        Function that reads the spec file and calls each vsphere object
        to configure the network in DCNM based on the contents of the csv file.
        '''
        if read_cfg:
            self.validate_cfg()
            LOG.info("Config file validation is successful")
        try:
            for dcnm_ip, dcnm_dict in self.dcnm_vsph_dict.items():
                vsph_dict = dcnm_dict.get('vsph_dict')

                for vsph_ip, vsph_obj in vsph_dict.items():
                    LOG.info("Going to configure for %(vsphere)s %(dcnm)s",
                             {'vsphere': vsph_ip, 'dcnm': dcnm_ip})
                    # This is supposed to goto queue
                    vsph_obj.configure(read_cfg=read_cfg, enable=enable,
                                       auto_deploy=self.auto_deploy,
                                       csv_list=dcnm_dict.get('csv_list'))
        except Exception as exc:
            LOG.error("DCNM Top: Exception in cfg all is %s", exc)

    def init_cfg_all(self):
        '''
        Wrapper for the cfg_all function called by the init routine.
        '''
        self.cfg_all(read_cfg=True, enable=True)

    def cleanup(self):
        '''
        Cleanup handler, which will call the routine to unconfig the networks.
        '''
        LOG.info("In cleanup handler")
        self.cfg_all(enable=False)

    def refresh(self):
        '''
        Refresh handler, which will call the routine to re-read the spec file
        and perform the config operation again.
        '''
        LOG.info("In refresh handler")
        self.cfg_all(read_cfg=True, enable=True)

    def resync(self):
        '''
        Resync handler, which will call the routine to perform the config
        operation again if certain parameters like the neighbour's networks
        have changed.
        '''
        LOG.info("In resync handler")
        self.cfg_all(enable=True)

    def instantiate_all(self):
        '''
        Function that instantiates all the vsphere objects and DCNM helper
        objects.
        '''
        nwk_mgr_list = self.conf_dict.get('NwkMgr')
        flag = False
        if nwk_mgr_list is None:
            LOG.error("Incorrect yaml format, NwkMgr key not present")
            return flag
        for nwk_mgr_dict in nwk_mgr_list:
            LOG.info("In Instantiate, nwk_mgr_dict is %s", nwk_mgr_dict)
            ret = self.check_dcnm_cfg(nwk_mgr_dict)
            if not ret:
                LOG.error("Invalid Ip or User or Pwd in yaml file, dict")
                continue
            dcnm_ip = nwk_mgr_dict.get("Ip")
            LOG.info("DCNM IP is %s", dcnm_ip)
            dcnm_obj = dcnm_helper.DcnmHelper(ip=dcnm_ip,
                                              user=nwk_mgr_dict.get("User"),
                                              pwd=nwk_mgr_dict.get("Password"))
            csv_file = nwk_mgr_dict.get("CsvFile")
            vsph_list = nwk_mgr_dict.get('ServerCntrlr')
            if vsph_list is None:
                LOG.error("Incorrect yaml, ServerCntrlr key not present")
                continue
            self.dcnm_vsph_dict.update({dcnm_ip: {'obj': dcnm_obj,
                                                  'csv_file': csv_file,
                                                  'vsph_dict': {}}})
            for vsph_dict in vsph_list:
                ret = self.check_vsph_cfg(vsph_dict)
                if not ret:
                    LOG.error("Invalid values for server ctrlr in yaml file %s",
                              vsph_dict)
                    continue
                vsph_ip = vsph_dict.get("Ip")
                vsph_obj = vsph_handler.VsphHandler(vsph_dict=vsph_dict,
                                                    dcnm_obj=dcnm_obj)
                self.dcnm_vsph_dict[dcnm_ip]['vsph_dict'].update(
                    {vsph_ip: vsph_obj})
                flag = True
        LOG.info("Instantiated successfully, dict is %s", self.dcnm_vsph_dict)
        return flag
