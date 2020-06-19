from .credentials import CredentialsAzure
import requests
import json
import urllib3

from easy_openshift import openshift
'''
:copyright: (c) 2020 by Alisson Castro.
:email: alissoncastroskt@gmail.com
'''

class MigrateVmAzure(CredentialsAzure):

    def __init__(self):
        super().__init__()

    def api_method(type_action):
        def action_decotator(func):
            def func_wrapper(*args):
                try:
                    _obj = func(*args)[0]
                    _token = _obj.get_token
                    _host = func(*args)[1]
                    _data_json = func(*args)[2]

                    if type_action in ["get", "put", "patch", "post", "delete"]:
                        if type_action == "get":
                            header = {
                                'Accept': 'application/json',
                                'Authorization': 'Bearer {0}'.format(_token)
                            }
                            response = requests.get(_host, verify=False, headers=header)
                            return json.loads(response.content)

                        elif type_action == "patch":
                            header = {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer {0}'.format(_token)
                            }
                        
                            response = requests.patch(_host, verify=False, headers=header, json=_data_json)
                            return response

                        elif type_action == "put":
                            header = {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer {0}'.format(_token)
                            }
                            response = requests.put(_host, verify=False, headers=header, json=_data_json)
                            return response

                        elif type_action == "post":
                            header = {
                                'Accept': "application/json, text/javascript, */*",
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer {0}'.format(_token)
                            }
                            response = requests.post(_host, verify=False, headers=header, json=_data_json)
                            return response

                        elif type_action == "delete":
                            header = {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer {0}'.format(_token)
                            }
                            response = requests.delete(_host, verify=False, headers=header)
                            return response

                    else:
                        print("==> Invalid type of action! ({0})".format(type_action))
                        exit(1)

                except (ConnectionError, TimeoutError, ValueError, SystemError) as err:
                    print("==> Erro: {0}".format(err))
                    exit(1)
            return func_wrapper
        return action_decotator        

    @property
    def get_token(self):

        return self.get_token_sp
    
    @api_method("post")
    def test_migrate_vm(self, host, recovery_point, network_id):

        '''The operation to initiate test migration of the item, all params are in details of a migration item.
        
        :param host: The host API migration items. Found in the details of a migration item.
        :recovery point: In the details of a migration: ['properties']['providerSpecificDetails']["lastRecoveryPointId"]
        :networkId: In the details of a migration: ['properties']['providerSpecificDetails']['targetNetworkId']
        
        .. note::

            link docs: https://docs.microsoft.com/en-us/rest/api/site-recovery/replicationmigrationitems/get
        
        '''
        data_json = {
        "properties": {
            "providerSpecificDetails": {
            "instanceType": "VMwareCbt",
            "recoveryPointId": f"{recovery_point}",
            "networkId": f"{network_id}"
            }
        }
        }

        host = f"https://management.azure.com{host}/testMigrate?api-version=2018-07-10"
        
        return self, host, data_json

    @api_method("post")
    def cleanup_test_migration(self, path_item):

        data_json = {
        "properties": {
            "comments": "Test Failover Cleanup"
        }
        }
        
        host = "https://management.azure.com"+path_item+"/testMigrateCleanup?api-version=2018-07-10"

        return self, host, data_json
    
    @api_method("get")
    def get_migration_items(self, subscription, resource_group, vault):

        host = f"https://management.azure.com/subscriptions/{subscription}/resourceGroups/{resource_group}/providers/Microsoft.RecoveryServices/vaults/{vault}/replicationMigrationItems?api-version=2018-07-10"
        
        return self, host, None
    
    @api_method("get")
    def get_migration_items_vm(self, host_path):

        host = f"https://management.azure.com"+host_path+"?api-version=2018-01-10"
        return self, host, None

    @api_method("get")
    def get_migration_items_nextlink(self, nextlink):

        return self, nextlink, None    

    @api_method("get")    
    def get_discovery_servers(self, subscription, resource_group, project, vm_name, vmware_site):

        host =  f"https://management.azure.com/subscriptions/{subscription}/resourceGroups/{resource_group}/providers/Microsoft.OffAzure/VMwareSites/{vmware_site}/machines?api-version=2019-06-06&pageSize=20&%24filter=(Properties%2FIsDeleted%20eq%20false)%20and%20((contains(Name%2C'{vm_name}'))%20or%20(contains(Properties%2FOperatingSystemDetails%2FOSName%2C'{vm_name}')))"
        
        return self, host, None
    
    @api_method("post")
    def enable_migrate(self, host_path):

        data_json = {
            "properties": {
                "providerSpecificDetails": {
                "instanceType": "VMwareCbt",
                "performShutdown": "true"
                }
            }
        }
    
        host  = f"https://management.azure.com{host_path}/migrate?api-version=2018-01-10"         
        return self, host, data_json

    @api_method("put")
    def create_group(self, subscription, resource_group, vm_name, group, project, asse_project=None):

        data_json = {
            "properties": {
                "machines": f"/subscriptions/{subscription}/resourceGroups/{resource_group}/providers/Microsoft.Migrate/assessmentprojects/{asse_project}/machines/{vm_name}",
                "operationType": "Add"
            },
        }
  
        host = f"https://management.azure.com/subscriptions/{subscription}/resourceGroups/{resource_group}/providers/Microsoft.Migrate/assessmentprojects/{asse_project}/groups/{group}?api-version=2019-05-01"

        return self, host, data_json

    @api_method("get")
    def get_machines(self, subscription, resource_group, vm_name, project, asse_project=None):
   
        host = f"https://management.azure.com/subscriptions/{subscription}/resourceGroups/{resource_group}/providers/Microsoft.Migrate/assessmentprojects/{asse_project}/machines?api-version=2019-05-01&pageSize=15&%24filter=(contains(Properties/DisplayName%2C'{vm_name}'))%20or%20(contains(Properties/OperatingSystemName%2C'{vm_name}'))"

        return self, host, None

    @api_method("post")
    def add_machine_to_group(self, group, id_machine, project, subscription, resource_group, asse_project=None):

        data_json = {
            "properties": {
                "machines": [f"/subscriptions/{subscription}/resourceGroups/{resource_group}/providers/Microsoft.Migrate/assessmentprojects/{asse_project}/machines/{id_machine}"],
                "operationType": "Add"
            },
            "eTag":"*"
        }
        
        host = f"https://management.azure.com/subscriptions/{subscription}/resourceGroups/{resource_group}/providers/Microsoft.Migrate/assessmentprojects/{asse_project}/groups/{group}/updateMachines?api-version=2019-05-01"    

        return self, host, data_json

    @api_method("delete")
    def delete_migration_item(self, id_vm):

        host = f"https://management.azure.com/{id_vm}?api-version=2018-07-10"

        return self, host, None    

    @api_method("patch")
    def update_network_machine(self, data_json):

        host = f"https://management.azure.com{data_json['id']}?api-version=2018-01-10"

        data_json = data_json

        return self, host, data_json

    @api_method("put")
    def enable_backup(self, vm_id, vm_name, resource_group, subscription_id, backup_vault, policy):
        
        data_json = {
        "properties": {
            "protectedItemType": "Microsoft.Compute/virtualMachines",
            "sourceResourceId": vm_id,
            "policyId": f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/microsoft.recoveryservices/vaults/{backup_vault}/backupPolicies/{policy}"
        }
        }
        host = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.RecoveryServices/vaults/{backup_vault}/backupFabrics/Azure/protectionContainers/IaasVMContainer;iaasvmcontainerv2;{resource_group};{vm_name}/protectedItems/vm;iaasvmcontainerv2;{resource_group};{vm_name}?api-version=2019-05-13"    

        return self, host, data_json
