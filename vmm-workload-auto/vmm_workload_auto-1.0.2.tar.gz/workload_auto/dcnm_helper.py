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

# pylint: disable=no-member
'''
DCNM helper module. This module interacts with DCNM.
'''

from functools import wraps
import json
import requests
from requests.exceptions import HTTPError
from workload_auto import logger

LOG = logger.get_logging(__name__)
ADD = "ADD"
DELETE_ADD = "DELETE_ADD"
NOOP = "NOOP"

class DcnmHelper:
    '''
    DCNM helper class.
    '''
    def __init__(self, **kwargs):
        '''
        Init routine that initializes the URL's, user, pws etc.
        '''
        self._ip = kwargs['ip']
        self._user = kwargs['user']
        self._pwd = kwargs['pwd']
        self._timeout_resp = 10
        self._req_headers = {'Accept': 'application/json',
                             'Content-Type': 'application/json; charset=UTF-8'}
        self._resp_ok = (requests.codes.ok, requests.codes.created,
                         requests.codes.accepted)
        self._expiration_time = 100000
        self._protocol_host_url = "https://" + self._ip + "/"
        self._base_url = "rest/top-down/fabrics/"
        self._attach_url = "networks/attachments"
        self._nwk_get_url = "rest/top-down/fabrics/"
        self._deploy_url = "networks/deployments"
        self._inventory_url = "rest/control/fabrics/"
        self._get_fab_association_url = "rest/control/fabrics/msd/fabric-associations/"
        self._get_pc_id_url = "rest/interface/pcid"
        LOG.info("Initialized DCNM helper class")

    def _build_url(self, remaining_url):
        '''
        Appends the base URL with the passing URL.
        '''
        return self._protocol_host_url + remaining_url

    def http_exc_handler(http_func):
        '''
        Decorator function for catching exceptions.
        '''
        @wraps(http_func)
        def exc_handler_int(*args):
            try:
                fn_name = http_func.__name__
                return http_func(*args)
            except HTTPError as http_err:
                LOG.error("HTTP error during call to %(func)s, %(err)s",
                          {'func': fn_name, 'err': http_err})
        return exc_handler_int

    @http_exc_handler
    def login(self):
        '''
        Function for login to DCNM.
        '''
        login_url = self._build_url('rest/logon')
        payload = {'expirationTime': self._expiration_time}
        res = requests.post(login_url, data=json.dumps(payload),
                            headers=self._req_headers,
                            auth=(self._user, self._pwd),
                            timeout=self._timeout_resp, verify=False)
        session_id = ""
        if res and res.status_code in self._resp_ok:
            session_id = res.json().get('Dcnm-Token')
            self._req_headers.update({'Dcnm-Token': session_id})
            return True
        LOG.error("Login failed with status %(status)s",
                  {'status': res.status_code})
        return False

    @http_exc_handler
    def logout(self):
        '''
        Function for logoff from DCNM.
        '''
        logout_url = self._build_url('rest/logout')
        requests.post(logout_url, headers=self._req_headers,
                      timeout=self._timeout_resp, verify=False)

    def _get_snum_from_name(self, name, data):
        '''
        Returns the serial number from the name
        '''
        for sw_info in data:
            if sw_info.get('logicalName') == name:
                return sw_info.get('serialNumber')
        LOG.error("Unable to get snum for switch %(name)s", {'name': name})
        return None

    @http_exc_handler
    def _get_switches(self, fabric):
        '''
        Function for retrieving the switch list from DCNM, given the fabric.
        '''
        sw_map = {}
        url = self._build_url(self._inventory_url) + fabric + "/inventory/"
        res = requests.get(url, headers=self._req_headers,
                           timeout=self._timeout_resp, verify=False)
        if res and res.status_code in self._resp_ok:
            data = res.json()
            for sw_info in data:
                if 'serialNumber' in sw_info:
                    snum = sw_info.get('serialNumber')
                    name = sw_info.get('logicalName')
                    is_vpc = sw_info.get('isVpcConfigured')
                    peer = ""
                    peer_snum = ""
                    if is_vpc is None or not is_vpc:
                        is_vpc = False
                    else:
                        peer = sw_info.get('peer')
                        peer_snum = self._get_snum_from_name(peer, data)
                    vpc_map = {'name': name, 'is_vpc': is_vpc, 'peer': peer,
                               'peer_snum': peer_snum}
                    sw_map.update({snum: vpc_map})
        else:
            LOG.error("invalid result for get_switches status %(status)s",
                      {'status': res.status_code})
        return sw_map

    def get_switches(self, fabric):
        '''
        Top level function for retrieving the switches.
        '''
        sw_info = []
        try:
            ret = self.login()
            if ret:
                sw_info = self._get_switches(fabric)
                self.logout()
        except Exception as exc:
            LOG.error("Exception in get_switches, %(exc)s", {exc:exc})
        return sw_info

    @http_exc_handler
    def _get_portchannel_id(self, snum, intf):
        '''
        Retrieve the PO-ID associated with the interface, if any.
        '''
        url = self._build_url(self._get_pc_id_url) + "?serialNumber=" + (
            snum + "&ifName=" + intf)
        res = requests.get(url, headers=self._req_headers,
                           timeout=self._timeout_resp, verify=False)
        data = None
        if res and res.status_code in self._resp_ok:
            if len(res.content) != 0:
                data = res.json()
        else:
            LOG.error("invalid result for get_pc_id status %(status)s",
                      {'status': res.status_code})
        return data

    def get_portchannel_id(self, snum, intf):
        '''
        Top level function for retrieving the PO id.
        '''
        try:
            ret = self.login()
            if ret:
                pc_id = self._get_portchannel_id(snum, intf)
                self.logout()
        except Exception as exc:
            LOG.error("Exception in get_pc_id, %(exc)s", {exc:exc})
        return pc_id

    @http_exc_handler
    def _get_all_fabric_associations(self):
        '''
        Retrieve the parent fabric in case of MSD's.
        '''
        url = self._build_url(self._get_fab_association_url)
        res = requests.get(url, headers=self._req_headers,
                           timeout=self._timeout_resp, verify=False)
        if res and res.status_code in self._resp_ok:
            data = res.json()
            fab_dict = {}
            for fab_elem in data:
                par = fab_elem.get('fabricParent')
                if par is not None and par != 'None':
                    fab_dict.update({fab_elem.get('fabricName'): fab_elem.get(
                                                'fabricParent')})
        else:
            LOG.error("invalid result for get_fabric_assoc status %(status)s",
                      {'status': res.status_code})
        return fab_dict

    def get_all_fabric_associations(self):
        '''
        Top level function to get the parent fabric in MSD.
        '''
        fab_parent = None
        try:
            ret = self.login()
            if ret:
                fab_parent = self._get_all_fabric_associations()
                self.logout()
        except Exception as exc:
            LOG.error("Exception in get_fabric_associations, %(exc)s",
                      {exc:exc})
        return fab_parent

    @http_exc_handler
    def _get_attachments(self, fabric, nwk_name):
        '''
        Retrieve the network attachment given the fabric and network.
        '''
        url = self._build_url(self._base_url) + fabric + "/" + (
            self._attach_url + "?network-names=" + nwk_name)
        res = requests.get(url, headers=self._req_headers,
                           timeout=self._timeout_resp, verify=False)
        if res and res.status_code in self._resp_ok:
            data = res.json()
            return data
        LOG.error("invalid result for get_attachments status %(status)s",
                  {'status': res.status_code})
        return None

    @http_exc_handler
    def _attach_network(self, fab_parent, nwk_name, lan_attach_list):
        '''
        Function to attach the network.
        '''
        url = self._build_url(self._base_url) + fab_parent + "/" + (
            self._attach_url)
        payload_list = []
        payload = {'networkName' : nwk_name,
                   'lanAttachList': lan_attach_list}
        payload_list.append(payload)
        data = json.dumps(payload_list)
        res = requests.post(url, data=data,
                            headers=self._req_headers,
                            timeout=self._timeout_resp, verify=False)
        LOG.info("attach network url %(url)s res is %(res)s, text is %(text)s, "
                 "reason %(reason)s, data %(data)s",
                 {'url': url, 'res': res, 'text': res.text,
                  'reason': res.reason, 'data': data})
        if res and res.status_code in self._resp_ok:
            LOG.info("attach network successful")
        else:
            LOG.info("attach network failed with status %s, res %s",
                     res.status_code, res.json())

    @http_exc_handler
    def _is_nwk_exist(self, fabric, nwk):
        '''
        Function that returns if the network for the fabric exists
        in DCNM.
        '''
        url = self._build_url(self._nwk_get_url) + fabric + "/networks/" + nwk
        res = requests.get(url, headers=self._req_headers,
                           timeout=self._timeout_resp, verify=False)
        if res and res.status_code in self._resp_ok:
            data = res.json()
            nwk_val = data.get('networkName')
            if nwk_val is None:
                return False
            return nwk_val == nwk
        LOG.error("invalid result for is_nwk_exist for fabric %s nwk %s",
                  fabric, nwk)
        return False

    def is_nwk_exist(self, fabric, nwk):
        '''
        Function that returns if the network for the fabric exists
        in DCNM.
        '''
        try:
            ret = self.login()
            if not ret:
                LOG.error("Failed to login to DCNM")
                return False
            ret = self._is_nwk_exist(fabric, nwk)
            self.logout()
            return ret
        except Exception as exc:
            LOG.error("Exception raised in is_nwk_exist %s", exc)
            return False

    def _compare_exist_cfg_sw(self, exist_cfg_elem, new_cfg, enable):
        '''
        Function to compare the existing attachment config in DCNM
        with the passed config and decide whether to:
        1. Attach/configure => ADD
        2. Don't do anythong => NOOP
        3. unattach followed by attach => DELETE_ADD
        '''
        lan_attach = exist_cfg_elem.get('isLanAttached')
        if enable:
            # Config is not attached, so add everything.
            if not lan_attach:
                return ADD
        else:
            # config is not attached, so nothing to disable.
            if not lan_attach:
                return NOOP
            # No need to perform the remaining checks for disable.
            # ADD refers to proceeding with the operation.
            return ADD

        # 1. When the new config has switches, that is not in the existing
        # config then it can either be a new switch add belonging to an existing
        # network or a change in the neighbor switch itself. This is the case of
        # ADD.
        # 2. When the existing config has switches, that is not in the new
        # config then it is a case of a change in the neighbor switch itself.
        # Should we remove the attachment from the removed switch?? TODO
        #
        # Ideally 1. should be a ADD and 2 should be a DELETE.
        # For now, case 1. is handled in the calling function itself.
        # case 2 is not handled here and a NOOP is returned.
        exist_snum = exist_cfg_elem.get('switchSerialNo')
        new_sw_vlan_intf_info = new_cfg.get('snum_vlan_intf_dict')
        if exist_snum not in new_sw_vlan_intf_info:
            return NOOP
        new_sw_info = new_sw_vlan_intf_info.get(exist_snum)
        # This is the case of VLAN changing, so add the new network. It's not
        # a case of DELETE_ADD.
        # Different networks can still use the same
        # interface with different VLAN's. The below logic doesn't impact
        # that. Only when the same network gets different VLAN's, one needs to
        # Delete and Add.
        if str(exist_cfg_elem.get('vlanId')) != str(new_sw_info.get('vlan')):
            return ADD

        # Now comparing the interface list
        exist_intf = exist_cfg_elem.get('portNames')
        if exist_intf is not None:
            exist_intf_list = exist_intf.split(",")
        else:
            exist_intf_list = []
        new_intf_list = new_sw_info.get('intf_list')
        # 1. If any new interface is not present in the existing config, then
        # it's a case of interface add (may be a new switch add or worst a
        # neighbor change). Interface add for PO will still be a PO, it's not
        # a ADD. We do a ADD.
        # 2. IF any existing interface is not present in the new config, then
        # it's a case of interface change and we need to a DELETE_ADD
        # This may have some duplicate attach for interfaces thar are present
        # in both existing and new configs. This is simpler for now.
        # We will revisit if there's an issue.
        # case 2 first
        if not set(exist_intf_list).issubset(set(new_intf_list)):
            return DELETE_ADD
        # case 1
        if not set(new_intf_list).issubset(set(exist_intf_list)):
            return ADD
        return NOOP

    def _compare_exist_cfg(self, exist_cfg_arr, new_cfg, enable):
        '''
        Function to compare the passed config with existing config in
        DCNM for each switch.
        '''
        sw_oper_dict = {}
        exist_cfg_dict = {}
        if len(exist_cfg_arr) > 0:
            exist_cfg = exist_cfg_arr[0]
            for exist_cfg_elem in exist_cfg.get('lanAttachList'):
                snum = exist_cfg_elem.get('switchSerialNo')
                oper = self._compare_exist_cfg_sw(exist_cfg_elem, new_cfg,
                                                  enable)
                exist_cfg_dict.update({snum: exist_cfg_elem})
                sw_oper_dict.update({snum: oper})
        for snum in new_cfg.get('snum_vlan_intf_dict').keys():
            if snum not in sw_oper_dict:
                if enable:
                    sw_oper_dict.update({snum: ADD})
                else:
                    # For a disable case, if there's a new switch, it's a NOOP
                    sw_oper_dict.update({snum: NOOP})
        return sw_oper_dict, exist_cfg_dict

    def _create_lan_attach_data(self, fabric, nwk_name, snum,
                                sw_ports, vlan, enable):
        dot1q = 1
        lan_attach = {'fabric': fabric, 'networkName': nwk_name,
                      'serialNumber': snum, 'switchPorts': sw_ports,
                      'vlan': vlan, 'dot1QVlan': dot1q, 'untagged': False,
                      'detachSwitchPorts': "", 'freeformConfig': "",
                      'extensionValues': "", 'instanceValues': "",
                      'deployment': enable}
        return lan_attach

    def attach_network(self, enable, deploy, arg_dict):
        '''
        Top level function to attach the network.
        '''
        try:
            ret = self.login()
            if not ret:
                LOG.error("Failed to login to DCNM")
                return
            LOG.info("attach_network arg is %s for enable: %s", arg_dict,
                     enable)
            fab_parent = arg_dict.get('fab_parent')
            fabric = arg_dict.get('fab')
            nwk_name = arg_dict.get('nwk')
            snum_vlan_intf_dict = arg_dict.get('snum_vlan_intf_dict')
            #vlan = arg_dict.get('vlan')

            exist_data = self._get_attachments(fab_parent, nwk_name)
            LOG.info("exist_data is %s", exist_data)
            sw_oper_dict, exist_cfg_dict = self._compare_exist_cfg(exist_data,
                                                                   arg_dict,
                                                                   enable)
            lan_attach_del_list = []
            lan_attach_list = []
            for snum, vlan_intf_dict in snum_vlan_intf_dict.items():
                oper = sw_oper_dict.get(snum)
                LOG.info("For %s, operation is %s", snum, oper)
                if oper == NOOP:
                    continue
                vlan = vlan_intf_dict.get('vlan')
                intf_list = vlan_intf_dict.get('intf_list')
                if enable:
                    if oper == DELETE_ADD:
                        exist_cfg = exist_cfg_dict.get(snum)
                        lan_attach_del = self._create_lan_attach_data(
                            fabric, nwk_name, snum,
                            exist_cfg.get('portNames'),
                            exist_cfg.get('vlanId'), False)
                        lan_attach_del_list.append(lan_attach_del)
                    # For ADD and a DELETE_ADD, the below enable is common
                    lan_attach = self._create_lan_attach_data(
                        fabric, nwk_name, snum,
                        ",".join(intf_list), vlan, enable)
                    lan_attach_list.append(lan_attach)
                else:
                    #disable cannot have a DELETE_ADD
                    lan_attach = self._create_lan_attach_data(
                        fabric, nwk_name, snum,
                        ",".join(intf_list), vlan, enable)
                    lan_attach_list.append(lan_attach)
            flag = False
            if len(lan_attach_del_list) != 0:
                flag = True
                self._attach_network(fab_parent, nwk_name, lan_attach_del_list)
            if len(lan_attach_list) != 0:
                flag = True
                self._attach_network(fab_parent, nwk_name, lan_attach_list)
            if flag and deploy:
                self._deploy_network(fabric, nwk_name)
            self.logout()
        except Exception as exc:
            LOG.error("attach network failed with %(exc)s", {'exc': exc})

    @http_exc_handler
    def _deploy_network(self, fabric, nwk_name):
        '''
        Function to deploy the network in DCNM.
        '''
        url = self._build_url(self._base_url) + fabric + "/" + (
            self._deploy_url)
        payload = {'networkNames' : nwk_name}
        #payload_list.append(payload)
        data = json.dumps(payload)
        res = requests.post(url, data=data,
                            headers=self._req_headers,
                            timeout=self._timeout_resp, verify=False)
        if res and res.status_code in self._resp_ok:
            LOG.info("deploy network successful")
        else:
            LOG.info("deploy network failed with res %s", res)

    def deploy_network(self, fabric, nwk_name):
        '''
        Top level function to deployt the network.
        '''
        try:
            ret = self.login()
            if not ret:
                LOG.error("Failed to login to DCNM")
                return
            self._deploy_network(fabric, nwk_name)
            self.logout()
        except Exception as exc:
            LOG.error("deploy network failed with exception %(exc)s",
                      {'exc': exc})
