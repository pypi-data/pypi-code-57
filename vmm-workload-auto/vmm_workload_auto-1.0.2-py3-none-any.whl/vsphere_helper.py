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
vSphere/vCenter helper module. This module interacts with vSphere using pynmoni
'''

from pyVim.connect import SmartConnectNoSSL
from pyVmomi import vim
from workload_auto import logger

LOG = logger.get_logging(__name__)

class VsphereHelper:
    '''
    VSphere Helper class
    '''
    def __init__(self, **kwargs):
        '''
        Init routine that connects with the specified vCenter
        '''
        self.ip_addr = kwargs.get('ip')
        self.user = kwargs.get('user')
        self.pwd = kwargs.get('pwd')
        self.si_obj = SmartConnectNoSSL(host=self.ip_addr, user=self.user,
                                        pwd=self.pwd)

    def get_all_objs(self, vimtype):
        '''
        Retrieve all the objects of a specific type
        '''
        obj = {}
        container = self.si_obj.content.viewManager.CreateContainerView(
            self.si_obj.content.rootFolder, vimtype, True)
        for managed_object_ref in container.view:
            obj.update({managed_object_ref: managed_object_ref.name})
        return obj

    def get_specific_obj(self, vimtype, name):
        '''
        Retrieve the object of a specific type matching the name.
        '''
        container = self.si_obj.content.viewManager.CreateContainerView(
            self.si_obj.content.rootFolder, vimtype, True)
        for managed_object_ref in container.view:
            if managed_object_ref.name == name:
                return managed_object_ref
        return None

    def get_dvs_pg_obj(self, dvs_name, dvs_pg):
        '''
        Returns the DVS and DVS PG objects.
        '''
        dvs_obj = self.get_specific_obj([vim.DistributedVirtualSwitch],
                                        dvs_name)
        if dvs_obj is None or dvs_obj.name != dvs_name:
            LOG.error("DVS %s does not exist", dvs_name)
            return None, None
        dvs_pgs = dvs_obj.portgroup
        for dvpg in dvs_pgs:
            if dvpg.name == dvs_pg:
                return dvs_obj, dvpg
        LOG.error("DVS PG %s does not exist", dvs_pg)
        return None, None

    def is_dvs_dvspg_exist(self, dvs_name, dvs_pg):
        '''
        Checks if the DVS and DVS PG exist in vSphere.
        '''
        dvs_obj, dvs_pg_obj = self.get_dvs_pg_obj(dvs_name, dvs_pg)
        if dvs_obj is None or dvs_pg_obj is None:
            LOG.error("get_dvs_pg_obj returns false for DVS %s dvs PG %s",
                      dvs_name, dvs_pg)
            return False
        return True

    def get_host_pg_obj(self, host_name, host_pg):
        '''
        Returns the Host and PG object
        '''
        host_obj = self.get_specific_obj([vim.HostSystem], host_name)
        if host_obj is None or host_obj.name != host_name:
            LOG.error("Host %s does not exist", host_name)
            return None, None
        for pg_obj in host_obj.config.network.portgroup:
            if pg_obj.spec.name == host_pg:
                return host_obj, pg_obj
        LOG.error("Host PG %s does not exist", host_pg)
        return None, None

    def is_host_hostpg_exist(self, host_name, host_pg):
        '''
        Checks if the Host and Host PG exist in vSphere.
        '''
        host_obj, host_pg_obj = self.get_host_pg_obj(host_name, host_pg)
        if host_obj is None or host_pg_obj is None:
            LOG.error("get_host_pg_obj returns false for host %s host PG %s",
                      host_name, host_pg)
            return False
        return True

    def get_vlan_dvs(self, dvs_name, dvs_pg):
        '''
        Get the Vlan associated wih the DV-PG in a DVS.
        First get all the DVS and get the DVS object matching the argument DVS
        For all the DV-PG in the DVS object, find the DV-PG that matches the
        DV-PG needed
        Then from that DV-PG object get the VLAN as give.
        Wish there's a should be a faster method to directly get the dvpg
        info instead of going through the loop.
        '''
        dvs_obj, dvs_pg_obj = self.get_dvs_pg_obj(dvs_name, dvs_pg)
        if dvs_obj is None or dvs_pg_obj is None:
            LOG.error("DVS %s or PG %s does not exist, cannot obtain VLAN",
                      dvs_name, dvs_pg)
            return ""
        vlan_info = dvs_pg_obj.config.defaultPortConfig.vlan
        cl_obj = vim.dvs.VmwareDistributedVirtualSwitch.TrunkVlanSpec
        if isinstance(vlan_info, cl_obj):
            # This needs to be tested
            return ""
        vlan_id = str(vlan_info.vlanId)
        return vlan_id

    def get_vlan_host_pg(self, host_name, pg_name):
        '''
        Get the Vlan associated wih the PG in a Host.
        First get the network object associated with the PG.
        Second, match the host, in case the same PG name is cfgs in multiple
        hosts. There are other ways to write the loop, but i think this is
        little better since the host loop being big is rare unless one cfgs the
        same PG name in multiple hosts.
        Next, for all the PG cfgd in the host find the matching PG object and
        return the VLAN.
        '''
        #hosts = self.get_all_objs([vim.HostSystem])
        host_obj, host_pg_obj = self.get_host_pg_obj(host_name, pg_name)
        if host_obj is None or host_pg_obj is None:
            LOG.error("Host %s or PG %s does not exist, cannot obtain VLAN",
                      host_name, pg_name)
            return ""
        vlan_id = str(host_pg_obj.spec.vlanId)
        return vlan_id

    def get_vlan(self, is_dvs, dvs_or_host_name, cmn_pg):
        '''
        Top level get vlan function.
        '''
        if is_dvs:
            return self.get_vlan_dvs(dvs_or_host_name, cmn_pg)
        else:
            return self.get_vlan_host_pg(dvs_or_host_name, cmn_pg)

    def get_host_neighbour(self, host_name, pnic_list):
        '''
        Retrieve the neighbour given a host and pnic's.
        '''
        host = self.get_specific_obj([vim.HostSystem], host_name)
        neighbour = []
        query = host.configManager.networkSystem.QueryNetworkHint()
        for nic in query:
            if not hasattr(nic, 'device'):
                LOG.error('device attribute not present')
                continue
            pnic = nic.device
            if pnic not in pnic_list:
                continue
            dct = {}
            conn_sw_port = nic.connectedSwitchPort
            if not hasattr(conn_sw_port, 'portId') or (
                    not hasattr(conn_sw_port, 'devId')):
                LOG.error("Port Id or devId attribute not present")
                continue
            sw_port = conn_sw_port.portId
            dev_id = conn_sw_port.devId
            snum_str = dev_id.split('(')
            if len(snum_str) > 1:
                snum = snum_str[1].split(')')[0]
            else:
                LOG.error("snum not present for the switch")
            if hasattr(conn_sw_port, 'mgmtAddr'):
                sw_ip = conn_sw_port.mgmtAddr
            if hasattr(conn_sw_port, 'systemName'):
                sw_name = conn_sw_port.systemName
            dct.update({'ip': sw_ip, 'snum': snum, 'pnic': pnic,
                        'sw_port': sw_port, 'name': sw_name})
            neighbour.append(dct)
        return neighbour

    def get_pnic_dvs(self, host_name, key_dvs):
        '''
        Return the list of pnic's of a host that is a part of a DVS.
        The pnic is taken from the host of DCV object.
        '''
        pnic_list = []
        for host in key_dvs.config.host:
            if host.config.host.name == host_name:
                for pnic_elem in host.config.backing.pnicSpec:
                    pnic_list.append(pnic_elem.pnicDevice)
        return pnic_list

    def get_dvs_pnic_info(self, dvs, dvs_pg):
        '''
        Return the list of neighbours for every host associated with the DVS.
        First get the matching DVS object and DV-PG object from the complete
        list.
        For the host that is a part of the DVS get the pnic and neighbour info.
        '''
        dvs_obj, dvs_pg_obj = self.get_dvs_pg_obj(dvs, dvs_pg)
        if dvs_obj is None or dvs_pg_obj is None:
            LOG.error("DVS %s or PG %s does not exist, cannot obtain pnic",
                      dvs, dvs_pg)
            return ""
        host_dict = {}
        for host_obj in dvs_pg_obj.host:
            pnic_list = self.get_pnic_dvs(host_obj.name, dvs_obj)
            nei_list = self.get_host_neighbour(host_obj.name, pnic_list)
            host_dict.update({host_obj.name: nei_list})
        return host_dict

    def _get_pnic_from_key(self, pnic_obj, pnic_comp_key):
        '''
        Return the device from pnic object for matching object name.
        '''
        for pnic_elem in pnic_obj:
            if pnic_elem.key == pnic_comp_key:
                return pnic_elem.device
        return None

    def get_host_pnic_info(self, host_name, pg_name):
        '''
        Get the pnic info for a specific host.
        First get the list of all network object for the PG.
        Then, filter the objects based on the passed host. This, i assume
        may not be much unless the same PG name is cfgd in multiple host.
        Get the vSwitch name that this PG is a part of.
        Then, for all the vswitches in the host, filter the specific vswitch
        and get the vswitch object.
        Get the pnic list from the vswitch, this gives the object list!!
        Then call _get_pnic_from_key which returns the dev associated
        with the pnic object.
        Retrieve the neighbour for the host and pnic.
        '''
        #hosts = self.get_all_objs([vim.HostSystem])
        host_dict = {}
        host_obj, host_pg_obj = self.get_host_pg_obj(host_name, pg_name)
        if host_obj is None or host_pg_obj is None:
            LOG.error("Host %s or PG %s does not exist, cannot obtain pnic",
                      host_name, pg_name)
            return ""
        vsw_name = host_pg_obj.spec.vswitchName
        for vsw in host_obj.config.network.vswitch:
            if vsw.name != vsw_name:
                continue
            pnic_list = vsw.pnic
            pnic_dev_list = []
            for pnic_elem in pnic_list:
                dev = self._get_pnic_from_key(host_obj.config.network.pnic,
                                              pnic_elem)
                pnic_dev_list.append(dev)
            nei_list = self.get_host_neighbour(host_name, pnic_dev_list)
            host_dict.update({host_name: nei_list})
        return host_dict

    def get_pnic(self, is_dvs, dvs_host_name, cmn_pg):
        '''
        Top level function to retrieve the information associated with the pnic.
        '''
        if is_dvs:
            return self.get_dvs_pnic_info(dvs_host_name, cmn_pg)
        else:
            return self.get_host_pnic_info(dvs_host_name, cmn_pg)
