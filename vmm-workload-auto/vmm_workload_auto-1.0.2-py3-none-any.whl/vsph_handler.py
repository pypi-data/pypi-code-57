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
Vsphere module, which is instantiated one per vCenter per DCNM. This maintains
the list of DVS and PG's and the associated, pNIC's, VLAN's and neighbour for
each pNIC. This module also calls the DCNM helper to do the network
attachment.
'''

from functools import wraps
import sys
from workload_auto import logger
from workload_auto import vsphere_helper

LOG = logger.get_logging(__name__)

class HostInfo:
    '''
    Class to store the host's neighbour information.
    '''
    def __init__(self, host, sw, dcnm_obj):
        '''
        Initialization routine for the class.
        '''
        self.host = host
        self.dcnm_obj = dcnm_obj
        self.neighbour_list = []
        self.add_neighbour(sw)

    def fill_po_intf(self):
        '''
        This function finds the associated PO index associated with the
        interfaces, if any.
        '''
        ind = 0
        for nbr_dict in self.neighbour_list:
            snum = nbr_dict.get('snum')
            intf_list = nbr_dict.get('sw_port')
            new_intf_list = []
            for intf in intf_list.split(","):
                po_id = self.dcnm_obj.get_portchannel_id(snum, intf)
                if po_id is None:
                    new_intf_list.append(intf)
                else:
                    new_intf = "Port-channel" + str(po_id)
                    if new_intf not in new_intf_list:
                        new_intf_list.append(new_intf)
            new_intf_str = ",".join(new_intf_list)
            nbr_dict['sw_port'] = new_intf_str
            self.neighbour_list[ind] = nbr_dict
            ind = ind + 1

    def add_neighbour(self, sw_info):
        '''
        This function maintains the list of hosts and its neighbours.
        '''
        flag = False
        cnt = 0
        for nbr_dict in self.neighbour_list:
            snum = nbr_dict.get('snum')
            if sw_info.get('snum') == snum:
                flag = True
                break
            cnt = cnt + 1
        nei_dict = sw_info
        if flag:
            LOG.info("Overwritting the neighbour for %s", sw_info.get('snum'))
            self.neighbour_list[cnt] = nei_dict
        else:
            self.neighbour_list.append(nei_dict)
        self.fill_po_intf()

    def add_undiscovered_neighbour(self, snum):
        '''
        This function adds an undiscovered vpc host to the neighbours list.
        Except for snum, other information are just copied over.
        '''
        if len(self.neighbour_list) == 0:
            LOG.error("Cannot add an undiscovered neighbour to an empty list")
            return
        nbr_dict = self.neighbour_list[0]
        new_dict = nbr_dict.copy()
        new_dict['snum'] = snum
        self.neighbour_list.append(new_dict)

    def get_neighbour(self):
        '''
        Function to return the neighbour list
        '''
        return self.neighbour_list

class VsphHandler:
    '''
    vSphere handler class.
    '''
    def __init__(self, **kwargs):
        '''
        The init routine which also instantiates the vsphere helper class.
        The two main data structures are:
        dvs_dict => Map of DVS pointing to map of DVS PG's.
        host_dict => Map of host name pointing to map of host PG's.
        Each DVS PG or host PG holds a list of fabric structure.
        Each fabric structure has the mapped DCNM Network name, VLAN and a
        map of hosts that this DVS spans.
        Each host map contains the object for the class HostInfo which holds
        the list of neighbour switches. It's a list because one host can point
        to multiple switches (vPC).
        '''
        srvr_cntrl_dict = kwargs['vsph_dict']
        self.ip_addr = srvr_cntrl_dict['Ip']
        self.user = srvr_cntrl_dict['User']
        self.pwd = srvr_cntrl_dict['Password']
        self.dcnm_obj = kwargs['dcnm_obj']
        self.csv_list = {}
        self.fab_parent_info = {}
        self.dvs_dict = {}
        self.host_dict = {}
        self.vsph_obj = vsphere_helper.VsphereHelper(ip=self.ip_addr,
                                                     user=self.user,
                                                     pwd=self.pwd)

    def get_ip(self):
        '''
        Retrieve the IP address of vSphere
        '''
        return self.ip_addr

    def get_dvs(self, dvs_name):
        '''
        Returns the dict of DVS PG's when given the DVS name.
        '''
        return self.dvs_dict.get(dvs_name)

    def set_dvs(self, dvs_name):
        '''
        Initializes the DVS dict if empty.
        '''
        dvs_dict = self.get_dvs(dvs_name)
        if dvs_dict is None:
            self.dvs_dict.update({dvs_name: {}})

    def get_host(self, host_name):
        '''
        Returns the dict of Host PG's when given the DVS name.
        '''
        return self.host_dict.get(host_name)

    def set_host(self, host_name):
        '''
        Initializes the Host dict if empty.
        '''
        host_dict = self.get_host(host_name)
        if host_dict is None:
            self.host_dict.update({host_name: {}})

    def cmn_dict_decor(fnc):
        '''
        Decorator function that calls the original function passing
        either the dvs_dict or host_dict based on the argument.
        '''
        @wraps(fnc)
        def cmn_dict_decor_int(self, *args):
            is_dvs = args[0]
            if is_dvs:
                cmn_dict = self.get_dvs(args[1])
            else:
                cmn_dict = self.get_host(args[1])
            return fnc(self, *args, cmn_dict=cmn_dict)
        return cmn_dict_decor_int

    @cmn_dict_decor
    def get_cmn_pg(self, is_dvs, dvs_or_host_name, cmn_pg_name, cmn_dict=None):
        '''
        Common function to return the port group or DVS PG content (List of fab)
        '''
        if cmn_dict is None:
            return None
        return cmn_dict.get(cmn_pg_name)

    @cmn_dict_decor
    def set_cmn_pg(self, is_dvs, dvs_or_host_name, cmn_pg_name, cmn_dict=None):
        '''
        Common function to initialzie the port group or DVS PG map.
        '''
        if cmn_dict is None:
            LOG.error("Unable to set dvs %(dvs)s dvs_name is null",
                      {'dvs': dvs_or_host_name})
            return
        cmn_pg = self.get_cmn_pg(is_dvs, dvs_or_host_name, cmn_pg_name)
        if cmn_pg is None:
            cmn_dict.update({cmn_pg_name: []})

    @cmn_dict_decor
    def get_cmn_fabric_info(self, is_dvs, dvs_or_host_name, cmn_pg_name, fab,
                            cmn_dict=None):
        '''
        Common function to return the fabric content of a PG or DVS PG.
        '''
        cmn_pg_list = self.get_cmn_pg(is_dvs, dvs_or_host_name, cmn_pg_name)
        if cmn_pg_list is None:
            return None
        #dvs_pg_list is basically a list of fabric dict
        for cmn_fab_dict in cmn_pg_list:
            if cmn_fab_dict.get('fabric') == fab:
                return cmn_fab_dict
        return None

    @cmn_dict_decor
    def set_cmn_fabric_info(self, is_dvs, dvs_or_host_name, cmn_pg_name, fab,
                            network, cmn_dict=None):
        '''
        Common function to set the fabric content of a PG or DVS PG.
        '''
        fabric_dict = self.get_cmn_fabric_info(is_dvs, dvs_or_host_name,
                                               cmn_pg_name, fab)
        if fabric_dict is not None:
            LOG.error('Fabric info already present for %(fabric)s, duplicate!!',
                      {'fabric': fab})
            return
        fabric_dict = {}
        # This is set at the beginning as well as when neighbour is filled.
        vlan = self.vsph_obj.get_vlan(is_dvs, dvs_or_host_name, cmn_pg_name)
        fabric_dict.update({'fabric': fab, 'network': network, 'vlan': vlan,
                            'host_obj_map': {}})
        cmn_dict[cmn_pg_name].append(fabric_dict)

    @cmn_dict_decor
    def set_neighbour_host(self, is_dvs, dvs_or_host_name, cmn_pg_name, fab,
                           host, sw_info, cmn_dict=None):
        '''
        Common function to set the host map of the fabric structure inside
        DVS PG or PG. This initializes the HostInfo class for the host.
        '''
        fabric_dict = self.get_cmn_fabric_info(is_dvs, dvs_or_host_name,
                                               cmn_pg_name, fab)
        if fabric_dict is None:
            LOG.error('Fabric info not present for %(fabric)s',
                      {'fabric': fab})
            return
        host_obj_dict = fabric_dict.get('host_obj_map')
        if host_obj_dict is None:
            host_obj_dict = {}
        if host not in host_obj_dict:
            host_obj = HostInfo(host, sw_info, self.dcnm_obj)
            host_obj_dict.update({host: host_obj})
            fabric_dict.update({'host_obj_map': host_obj_dict})
        else:
            host_obj = host_obj_dict.get(host)
            host_obj.add_neighbour(sw_info)

    @cmn_dict_decor
    def set_undisc_neighbour_host(self, is_dvs, dvs_or_host_name, cmn_pg_name,
                                  fab, host, snum, cmn_dict=None):
        '''
        In some cases, like a ESXI host connecting to a FEX, which is dual homed
        to two vPC leafs, the ESXi will only see one neighbour. But, the config
        needs to happen in both the leafs. This function sets the undiscovered
        vpc host also as one of the neighbour.
        '''
        fabric_dict = self.get_cmn_fabric_info(is_dvs, dvs_or_host_name,
                                               cmn_pg_name, fab)
        if fabric_dict is None:
            LOG.error('Fabric info not present for %(fabric)s',
                      {'fabric': fab})
            return
        host_obj_dict = fabric_dict.get('host_obj_map')
        if host_obj_dict is None or host not in host_obj_dict:
            LOG.error("host %(host)s does not have a neighbour, so cannot set "
                      "an undiscovered host ", host)
        else:
            host_obj = host_obj_dict.get(host)
            host_obj.add_undiscovered_neighbour(snum)

    @cmn_dict_decor
    def set_vlan(self, is_dvs, dvs_or_host_name, cmn_pg_name, fab, vlan,
                 cmn_dict=None):
        '''
        Common function to set the VLAN of the fabric structure inside
        DVS PG or PG.
        '''
        fabric_dict = self.get_cmn_fabric_info(is_dvs, dvs_or_host_name,
                                               cmn_pg_name, fab)
        if fabric_dict is None:
            LOG.error('Fabric info not present for %(fabric)s',
                      {'fabric': fab})
            return
        fabric_dict.update({'vlan': vlan})

    @cmn_dict_decor
    def get_vlan(self, is_dvs, dvs_or_host_name, cmn_pg_name, fab,
                 cmn_dict=None):
        '''
        Common function to vlan the VLAN from the fabric structure inside
        DVS PG or PG.
        '''
        fabric_dict = self.get_cmn_fabric_info(is_dvs, dvs_or_host_name,
                                               cmn_pg_name, fab)
        if fabric_dict is None:
            LOG.error('Fabric info not present for %(fabric)s',
                      {'fabric': fab})
            return 0
        return fabric_dict.get('vlan')

    def add_dvs_or_host(self, is_dvs, dvs_or_host, cmn_pg, fabric, network):
        '''
        Add Top level DVS or Host map.
        '''
        if cmn_pg is None or fabric is None or network is None:
            LOG.error('Invalid CSV values, %(cmn_pg)s %(fabric)s %(network)s',
                      {'cmn_pg': cmn_pg, 'fabric': fabric, 'network': network})
            return
        if is_dvs:
            self.set_dvs(dvs_or_host)
        else:
            self.set_host(dvs_or_host)
        #self.set_dvs_pg(dvs, dvs_pg)
        self.set_cmn_pg(is_dvs, dvs_or_host, cmn_pg)
        self.set_cmn_fabric_info(is_dvs, dvs_or_host, cmn_pg, fabric, network)

    def validate_cfg(self, csv_list):
        '''
        Function to validate if the DVS, DVS PG, Host or Host PG specified in
        CSV map, exists in vCenter.
        '''
        LOG.info("Validating vCenter params in %s", self.get_ip)
        for csv_map in csv_list:
            vcenter_ip = csv_map.get('vCenter')
            if vcenter_ip is None or vcenter_ip != self.get_ip():
                continue
            if csv_map.get('Dvs') is not None and csv_map.get('Dvs') != '':
                if not self.vsph_obj.is_dvs_dvspg_exist(csv_map.get('Dvs'),
                                                        csv_map.get('Dvs_pg')):
                    LOG.error("DVS %s or DVS PG %s does not exist in vCenter",
                              csv_map.get('Dvs'), csv_map.get('Dvs_pg'))
                    return False
            elif csv_map.get('Host') is not None and csv_map.get('Host') != '':
                if not self.vsph_obj.is_host_hostpg_exist(
                        csv_map.get('Host'), csv_map.get('Host_pg')):
                    LOG.error("Host %s or Host PG %s does not exist in vCenter",
                              csv_map.get('Host'), csv_map.get('Host_pg'))
                    return False
        return True

    def store_csv_map(self):
        '''
        Top level function that creates the DVS or Host map based on the
        contents in the spec file.
        '''
        for csv_map in self.csv_list:
            vcenter_ip = csv_map.get('vCenter')
            if vcenter_ip is None or vcenter_ip != self.get_ip():
                continue
            if csv_map.get('Dvs') is not None and csv_map.get('Dvs') != '':
                self.add_dvs_or_host(True, csv_map.get('Dvs'),
                                     csv_map.get('Dvs_pg'),
                                     csv_map.get('Fabric'),
                                     csv_map.get('Network'))
            elif csv_map.get('Host') is not None and csv_map.get('Host') != '':
                self.add_dvs_or_host(False, csv_map.get('Host'),
                                     csv_map.get('Host_pg'),
                                     csv_map.get('Fabric'),
                                     csv_map.get('Network'))
            else:
                LOG.error("Both DVS and Host values are empty in CSV")
        LOG.info("----After storing CSV file----")
        LOG.info("DVS Dict is %s", self.dvs_dict)
        LOG.info("Host Dict is %s", self.host_dict)

    def _is_peer_discovered(self, peer_snum, sw_nbr):
        '''
        Check if the peer VPC is present in the list of neighbours.
        '''
        for _sw in sw_nbr:
            _snum = _sw.get('snum')
            if peer_snum == _snum:
                return True
        return False

    def _fill_host_neighbour_info(self, is_dvs, dvs_or_host_dict):
        '''
        This function fills the neighbour information for each host.
        For every host, it queries the vsphere object to get the list of
        pNics, vlan. For pNic it finds the list of neighbouring switches and
        calls the appropriate set function to populate the values.
        '''
        for dvs_or_host_name, cmn_dict in dvs_or_host_dict.items():
            for cmn_pg, cmn_pg_list in cmn_dict.items():
                vlan = self.vsph_obj.get_vlan(is_dvs, dvs_or_host_name, cmn_pg)
                host_pnic_dict = self.vsph_obj.get_pnic(is_dvs,
                                                        dvs_or_host_name,
                                                        cmn_pg)
                for fab_dict in cmn_pg_list:
                    fab = fab_dict.get('fabric')
                    # This is a dynamic data, means it can change.
                    # So, vlan is also re-discovered and set here.
                    self.set_vlan(is_dvs, dvs_or_host_name, cmn_pg, fab, vlan)
                    sw_inv = self.dcnm_obj.get_switches(fab)
                    for host, sw_nbr in host_pnic_dict.items():
                        _vpc_map = {}
                        undisc_nei = []
                        for _sw in sw_nbr:
                            _snum = _sw.get('snum')
                            if _snum not in sw_inv:
                                LOG.error("Neighbor snum %(snum)s not in "
                                          "inventory, skiping", {'snum': _snum})
                                continue
                            _sw_info = sw_inv.get(_snum)
                            self.set_neighbour_host(
                                is_dvs, dvs_or_host_name, cmn_pg, fab,
                                host, _sw)
                            if not _sw_info.get('is_vpc'):
                                continue
                            #VPC case
                            peer_snum = _sw_info.get('peer_snum')
                            if not self._is_peer_discovered(peer_snum, sw_nbr):
                                LOG.info("snum %(snum)s vpc pair "
                                         "%(vpc)s not recognized as a "
                                         "neighbour, may be a single fex case",
                                         {'snum': _snum, 'vpc': peer_snum})
                                undisc_nei.append(peer_snum)
                        for _nb_snum in undisc_nei:
                            LOG.info("Setting undiscovered vpc neighbour %s",
                                     _nb_snum)
                            self.set_undisc_neighbour_host(
                                is_dvs, dvs_or_host_name, cmn_pg, fab, host,
                                _nb_snum)

    def fill_host_neighbour_info(self, is_dvs):
        '''
        Top level function for filling the neighbour info for either DVS or
        Host.
        '''
        if is_dvs:
            cmn_dict = self.dvs_dict
        else:
            cmn_dict = self.host_dict
        self._fill_host_neighbour_info(is_dvs, cmn_dict)

    def _create_sw_nw_dict(self, vlan, sw_intf_dict):
        '''
        Create a map of snum's containing vlan and interface list.
        '''
        sw_nw_dict = {}
        for snum, intf_list in sw_intf_dict.items():
            new_nw_str = {'vlan': vlan, 'intf_list': intf_list}
            sw_nw_dict.update({snum: new_nw_str})
        return sw_nw_dict

    def _summarize_validate_cfg(self, cfg_fab_dict, vlan, sw_intf_dict, nwk,
                                fab_name):
        '''
        Validates the config that needs to be sent to DCNM. This also
        aggregates the interface list to the existing sw map present in every
        network structure.
        '''
        nwk_exist_dict = {}
        # (fixme)  this loop below is not yet UT'ed.
        if fab_name in cfg_fab_dict:
            nwk_exist_dict = cfg_fab_dict.get(fab_name)
            if nwk in nwk_exist_dict:
                nwk_exist_sw_cfg = nwk_exist_dict.get(nwk)
                for snum, intf_list in sw_intf_dict.items():
                    if snum in nwk_exist_sw_cfg:
                        sw_cfg = nwk_exist_sw_cfg.get(snum)
                        if vlan != sw_cfg.get('vlan'):
                            LOG.error("Conflict VLAN value of %(vlan)s, "
                                      "%(exist_vlan)s for fab %(fab)s "
                                      "nwk %(nwk)s, snum %(snum)s",
                                      {'vlan': vlan,
                                       'exist_vlan': sw_cfg.get('vlan'),
                                       'fab': fab_name, 'nwk': nwk,
                                       'snum': snum})
                            return False, {}
                        new_intf_list = sw_cfg.get('intf_list') + intf_list
                        nwk_exist_sw_cfg[snum].update(
                            {'intf_list': new_intf_list})
                    else:
                        new_nw_str = {'vlan': vlan, 'intf_list': intf_list}
                        nwk_exist_sw_cfg.update({snum: new_nw_str})
                sw_nw_dict = nwk_exist_sw_cfg
            else:
                sw_nw_dict = self._create_sw_nw_dict(vlan, sw_intf_dict)
        else:
            sw_nw_dict = self._create_sw_nw_dict(vlan, sw_intf_dict)
        nwk_exist_dict.update({nwk: sw_nw_dict})
        cfg_fab_dict.update({fab_name: nwk_exist_dict})
        return True, cfg_fab_dict

    def _agg_cfg_data(self, cfg_fab_dict, dvs_or_host_dict):
        '''
        Aggregates the information that is needed according to DCNM format.
        Basically this creates a map of fabric, that has a map of networks
        with each network having a list containing the VLAN and a map of switch
        interface information.
        '''
        for dvs_or_host_name, cmn_dict in dvs_or_host_dict.items():
            for cmn_pg, cmn_pg_list in cmn_dict.items():
                for fab_dict in cmn_pg_list:
                    cfg_dict = {}
                    nwk = fab_dict.get('network')
                    fab_name = fab_dict.get('fabric')
                    vlan = fab_dict.get('vlan')
                    for host, obj in fab_dict.get('host_obj_map').items():
                        nbr_list = obj.get_neighbour()
                        for nbr_dict in nbr_list:
                            snum = nbr_dict.get('snum')
                            if snum not in cfg_dict:
                                cfg_dict.update({snum: []})
                            cfg_dict[snum].append(nbr_dict.get('sw_port'))
                    if len(cfg_dict) == 0:
                        LOG.info("No neighbours for fab %(fab)s, nwk %(nwk)s",
                                 {'fab': fab_name, 'nwk': nwk})
                        continue
                    ret, cfg_fab_dict = self._summarize_validate_cfg(
                        cfg_fab_dict, vlan, cfg_dict, nwk, fab_name)
                    if not ret:
                        LOG.error("Incorrect config ")
                        sys.exit(1)
                    #self.dcnm_obj.attach_network(fab_parent, fab_name, nwk,
                    #                            cfg_dict, vlan, enable,
                    #                            auto_deploy)
        return cfg_fab_dict

    def _create_cfg_data(self, cfg_fab_dict, is_dvs):
        '''
        Top level function to create the config data to be sent to DCNM for
        attach. This creates the config data based on dvs_dict or host_dict.
        '''
        if is_dvs:
            cmn_dict = self.dvs_dict
        else:
            cmn_dict = self.host_dict
        return self._agg_cfg_data(cfg_fab_dict, cmn_dict)

    def _cfg_all(self, enable=True, auto_deploy=False):
        '''
        Function that creates the config data for both DVS and host.
        For every fabric, it calls the DCNM helper to attach the network.
        '''
        cfg_fab_dict = {}
        cfg_fab_dict = self._create_cfg_data(cfg_fab_dict, True)
        cfg_fab_dict = self._create_cfg_data(cfg_fab_dict, False)
        for fab_name, fab_items in cfg_fab_dict.items():
            if fab_name in self.fab_parent_info:
                fab_parent = self.fab_parent_info.get(fab_name)
            else:
                fab_parent = fab_name
            for nwk, nwk_items in fab_items.items():
                #vlan = nwk_items[0]
                cfg_dict = nwk_items
                arg_dict = {'fab_parent': fab_parent, 'fab': fab_name,
                            'nwk': nwk, 'snum_vlan_intf_dict': cfg_dict}
                LOG.info("Calling attach network for enable %(enable)s "
                         "arg %(arg)s", {'enable': enable, 'arg': arg_dict})
                self.dcnm_obj.attach_network(enable, auto_deploy, arg_dict)
                #self.dcnm_obj.attach_network(fab_parent, fab_name, nwk,
                #                            cfg_dict, vlan, enable,
                #                            auto_deploy)

    def configure(self, read_cfg=False, enable=True, auto_deploy=False,
                  csv_list=[]):
        '''
        Top level configure function that does the following:
        refresh => Read cfg, read neighbour and reconfigure
        resync => read neighbour and reconfigure
        cleanup => reconfigure
        '''
        if read_cfg:
            self.csv_list = csv_list
            self.store_csv_map()
        if enable:
            self.fill_host_neighbour_info(True)
            self.fill_host_neighbour_info(False)
        self.fab_parent_info = self.dcnm_obj.get_all_fabric_associations()
        self._cfg_all(enable=enable, auto_deploy=auto_deploy)
        # Resetting it back so that it's not used from the cache.
        self.fab_parent_info = {}
