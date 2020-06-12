from requests import Session
from requests.adapters import HTTPAdapter
from http import HTTPStatus
from urllib3.util.retry import Retry
from datetime import datetime, timedelta
import os
import json


def __isjson(myjson):
    """
    Checks if a string is a valid json object
    """
    try:
        json_object = json.loads(myjson)
    except ValueError:
        return False
    return True


class NcmClient:
    def __init__(self,
                 api_keys,
                 logEvents=True,
                 retries=5,
                 retry_backoff_factor=2,
                 retry_on=[
                     HTTPStatus.REQUEST_TIMEOUT,
                     HTTPStatus.GATEWAY_TIMEOUT,
                     HTTPStatus.SERVICE_UNAVAILABLE
                 ],
                 base_url=os.environ.get(
                     'CP_BASE_URL', 'https://www.cradlepointecm.com/api/v2')
                 ):
        """
        Constructor. Sets up and opens request session.
        :param api_keys: Dictionary of API credentials. Required.
        :type api_keys: dict
        :param retries: number of retries on failure. Optional.
        :param retry_backoff_factor: backoff time multiplier for retries. Optional.
        :param retry_on: types of errors on which automatic retry will occur. Optional.
        :param base_url: # base url for calls. Configurable for testing. Optional.
        """
        self.logEvents = logEvents

        if type(api_keys) is not dict:
            raise TypeError("API Keys must be passed as a dictionary")

        if 'X-CP-API-ID' not in api_keys:
            raise KeyError("X-CP-API-ID missing. Please ensure all API Keys are present.")

        if 'X-CP-API-KEY' not in api_keys:
            raise KeyError("X-CP-API-KEY missing. Please ensure all API Keys are present.")

        if 'X-ECM-API-ID' not in api_keys:
            raise KeyError("X-ECM-API-ID missing. Please ensure all API Keys are present.")

        if 'X-ECM-API-KEY' not in api_keys:
            raise KeyError("X-ECM-API-KEY missing. Please ensure all API Keys are present.")

        self.base_url = base_url
        self.session = Session()
        self.adapter = HTTPAdapter(
            max_retries=Retry(total=retries,
                              backoff_factor=retry_backoff_factor,
                              status_forcelist=retry_on,
                              redirect=3
                              )
        )
        self.session.mount(self.base_url, self.adapter)
        self.session.headers.update(api_keys)
        self.session.headers.update({
            'Content-Type': 'application/json'
        })

    def __returnhandler(self, statuscode, returntext, objtype):
        """
        Prints returned HTTP request information if self.logEvents is True.
        """

        if str(statuscode) == '200':
            if self.logEvents:
                print('{0} Operation Successful\n'.format(str(objtype)))
            return None
        elif str(statuscode) == '201':
            if self.logEvents:
                print('{0} Added Successfully\n'.format(str(objtype)))
            return None
        elif str(statuscode) == '204':
            if self.logEvents:
                print('{0} Deleted Successfully\n'.format(str(objtype)))
            return None
        elif str(statuscode) == '400':
            if self.logEvents:
                print('Bad Request\n')
            return None
        elif str(statuscode) == '401':
            if self.logEvents:
                print('Unauthorized Access\n')
            return returntext
        elif str(statuscode) == '404':
            if self.logEvents:
                print('Resource Not Found\n')
            return returntext
        elif str(statuscode) == '500':
            if self.logEvents:
                print('HTTP 500 - Server Error\n')
            return returntext
        else:
            print('HTTP Status Code: {0} - No returned data\n'.format(str(statuscode)))

    def __get_json(self, geturl, call_type, params=None):
        """
        Returns full paginated results, and handles chunking "__in" params in groups of 100
        """

        results = []
        __in_keys = 0
        if params['limit'] == 'all':
            params['limit'] = 1000000
        limit = int(params['limit'])

        if params is not None:
            # Ensures that order_by is passed as a comma separated string
            if 'order_by' in params.keys():
                if type(params['order_by']) is list:
                    params['order_by'] = ','.join(str(x) for x in params['order_by'])
                elif type(params['order_by']) is not list and type(params['order_by']) is not str:
                    raise TypeError("Invalid 'order_by' parameter. Must be 'list' or 'str'.")

            for key, val in params.items():
                # Handles multiple filters using __in fields.
                if '__in' in key:
                    __in_keys += 1
                    # Cradlepoint limit of 100 values. If more than 100 values, break into chunks
                    chunks = self.__chunk_param(val)
                    # For each chunk, get the full results list and filter by __in parameter
                    for chunk in chunks:
                        chunkstr = ','.join(map(str, chunk))
                        params.update({key: chunkstr})
                        url = geturl
                        while url and (len(results) < limit):
                            ncm = self.session.get(url, params=params)
                            if not (200 <= ncm.status_code < 300):
                                break
                            self.__returnhandler(ncm.status_code, ncm.json()['data'], call_type)
                            url = ncm.json()['meta']['next']
                            for d in ncm.json()['data']:
                                results.append(d)

        if __in_keys == 0:
            url = geturl
            while url and (len(results) < limit):
                ncm = self.session.get(url, params=params)
                if not (200 <= ncm.status_code < 300):
                    break
                self.__returnhandler(ncm.status_code, ncm.json()['data'], call_type)
                url = ncm.json()['meta']['next']
                for d in ncm.json()['data']:
                    results.append(d)
        return results

    def __parse_kwargs(self, kwargs, allowed_params):
        """
        Increases default return limit to 500, and checks for invalid parameters
        """
        params = {k: v for (k, v) in kwargs.items() if k in allowed_params}
        if 'limit' not in params:
            params.update({'limit': '500'})

        bad_params = {k: v for (k, v) in kwargs.items() if k not in allowed_params}
        if len(bad_params) > 0:
            raise ValueError("Invalid parameters: {}".format(bad_params))
        return params

    def __chunk_param(self, param):
        """
        Chunks parameters into groups of 100 per Cradlepoint limit. Iterate through chunks with a for loop.
        """
        n = 100

        if type(param) is str:
            paramlist = param.split(",")
        elif type(param) is list:
            paramlist = param
        else:
            raise TypeError("Invalid param format. Must be str or list.")

        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(paramlist), n):
            yield paramlist[i:i + n]

    def get_accounts(self, **kwargs):
        """
        Returns accounts with details.


        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return: A list of accounts based on API Key.
        """

        call_type = 'Accounts'
        geturl = '{0}/accounts/'.format(self.base_url)

        allowed_params = ['account', 'account__in', 'id', 'id__in', 'name',
                          'name__in', 'expand', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_account_by_id(self, account_id):
        """
        This method returns a single account with its information specified by id.
        :param account_id: ID of account to return

        :return:
        """

        return self.get_accounts(id=account_id)[0]

    def get_account_by_name(self, account_name):
        """
        This method returns a single account with its information specified by name.
        :param account_name: Name of account to return

        :return:
        """
        return self.get_accounts(name=account_name)[0]

    def create_subaccount_by_parent_id(self, parent_account_id, subaccount_name):
        """
        This operation creates a new subaccount.
        :param parent_account_id: ID of parent account.
        :param subaccount_name: Name for new subaccount.

        :return:
        """
        call_type = 'Subaccount'
        posturl = '{0}/accounts/'.format(self.base_url)

        postdata = {
            'account': '/api/v1/accounts/{}/'.format(str(parent_account_id)),
            'name': str(subaccount_name)
        }

        ncm = self.session.post(posturl, data=json.dumps(postdata))
        result = self.__returnhandler(ncm.status_code, ncm.json(), call_type)
        return result

    def create_subaccount_by_parent_name(self, parent_account_name, subaccount_name):
        """
        This operation creates a new subaccount.
        :param parent_account_name: Name of parent account.
        :param subaccount_name: Name for new subaccount.

        :return:
        """
        return self.create_subaccount_by_parent_id(self.get_account_by_name(
            parent_account_name)['id'], subaccount_name)

    def rename_subaccount_by_id(self, subaccount_id, new_subaccount_name):
        """
        This operation renames a subaccount
        :param subaccount_id: ID of subaccount to rename
        :param new_subaccount_name: New name for subaccount

        :return:
        """
        call_type = 'Subaccount'
        puturl = '{0}/accounts/{1}/'.format(self.base_url, str(subaccount_id))

        putdata = {
            "name": str(new_subaccount_name)
        }

        ncm = self.session.put(puturl, data=json.dumps(putdata))
        result = self.__returnhandler(ncm.status_code, ncm.json(), call_type)
        return result

    def rename_subaccount_by_name(self, subaccount_name, new_subaccount_name):
        """
        This operation renames a subaccount
        :param subaccount_name: Name of subaccount to rename
        :param new_subaccount_name: New name for subaccount

        :return:
        """
        return self.rename_subaccount_by_id(self.get_account_by_name(
            subaccount_name)['id'], new_subaccount_name)

    def delete_subaccount_by_id(self, subaccount_id):
        """
        This operation deletes a subaccount
        :param subaccount_id: ID of subaccount to delete

        :return:
        """
        call_type = 'Subccount'
        posturl = '{0}/accounts/{1}'.format(self.base_url, subaccount_id)

        ncm = self.session.delete(posturl)
        result = self.__returnhandler(ncm.status_code, ncm.text, call_type)
        return result

    def delete_subaccount_by_name(self, subaccount_name):
        """
        This operation deletes a subaccount
        :param subaccount_name: Name of subaccount to delete

        :return:
        """
        return self.delete_subaccount_by_id(self.get_account_by_name(
            subaccount_name)['id'])

    def get_activity_logs(self, **kwargs):
        """
        This method returns NCM activity log information.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Activity Logs'
        geturl = '{0}/activity_logs/'.format(self.base_url)

        allowed_params = ['account', 'created_at__exact', 'created_at__lt', 'created_at__lte', 'created_at__gt',
                          'created_at__gte', 'action__timestamp__exact', 'action__timestamp__lt',
                          'action__timestamp__lte', 'action__timestamp__gt', 'action__timestamp__gte', 'actor__id',
                          'object__id', 'action__id__exact', 'actor__type', 'action__type', 'object__type', 'order_by',
                          'limit']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_alerts(self, **kwargs):
        """
        This method gives alert information with associated id.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Alerts'
        geturl = '{0}/alerts/'.format(self.base_url)

        allowed_params = ['account', 'created_at', 'created_at_timeuuid', 'detected_at', 'friendly_info', 'info',
                          'router', 'type', 'order_by', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)


    def get_configuration_managers(self, **kwargs):
        """
        A configuration manager is an abstract resource for controlling and monitoring config sync on a single device.
        Each device has its own corresponding configuration manager.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Configuration Managers'
        geturl = '{0}/configuration_managers/'.format(self.base_url)

        allowed_params = ['account', 'account__in', 'id', 'id__in', 'router', 'router__in', 'synched',
                          'suspended', 'expand', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    # This method updates an configuration_managers for associated id
    def update_configuration_managers(self, configman_id, configman_json):
        call_type = 'Configuration Manager'
        puturl = '{0}/configuration_managers/{1}/'.format(self.base_url, configman_id)

        payload = str(configman_json)

        ncm = self.session.put(puturl, data=json.dumps(payload))
        result = self.__returnhandler(ncm.status_code, ncm.json(), call_type)
        return result

    def get_device_app_bindings(self, **kwargs):
        """
        This method gives device app binding information for all device app bindings associated with the account.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Device App Bindings'
        geturl = '{0}/device_app_bindings/'.format(self.base_url)

        allowed_params = ['account', 'account__in', 'group', 'group__in', 'app_version', 'app_version__in',
                          'id', 'id__in', 'state', 'state__in', 'expand', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_device_app_states(self, **kwargs):
        """
        This method gives device app state information for all device app states associated with the account.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Device App States'
        geturl = '{0}/device_app_states/'.format(self.base_url)

        allowed_params = ['account', 'account__in', 'router', 'router__in', 'app_version', 'app_version__in',
                          'id', 'id__in', 'state', 'state__in', 'expand', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_device_app_versions(self, **kwargs):
        """
        This method gives device app version information for all device app versions associated with the account.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Device App Versions'
        geturl = '{0}/device_app_versions/'.format(self.base_url)

        allowed_params = ['account', 'account__in', 'app', 'app__in', 'id', 'id__in', 'state', 'state__in',
                          'expand', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_device_apps(self, **kwargs):
        """
        This method gives device app information for all device apps associated with the account.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Device Apps'
        geturl = '{0}/device_apps/'.format(self.base_url)

        allowed_params = ['account', 'account__in', 'name', 'name__in', 'id', 'id__in', 'uuid', 'uuid__in',
                          'expand', 'order_by', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_failovers(self, **kwargs):
        """
        This method returns a list of Failover Events for a device, group, or account.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Failovers'
        geturl = '{0}/failovers/'.format(self.base_url)

        allowed_params = ['account_id', 'group_id', 'router_id', 'started_at', 'ended_at', 'order_by', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_firmwares(self, **kwargs):
        """
        This operation gives the list of device firmwares.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Firmwares'
        geturl = '{0}/firmwares/'.format(self.base_url)

        allowed_params = ['id', 'id__in', 'version', 'version__in', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_firmware_for_productid_by_version(self, product_id, firmware_name):
        """
        This operation returns firmwares for a given model ID and version name.
        :param product_id: The ID of the product (e.g. 46)
        :param firmware_name: The Firmware Version (e.g. 7.2.0)

        :return:
        """
        for f in self.get_firmwares(version=firmware_name):
            if f['product'] == '{0}/products/{1}/'.format(self.base_url, str(product_id)):
                return f
        raise ValueError("Invalid Firmware Version")
        return

    def get_firmware_for_productname_by_version(self, product_name, firmware_name):
        """
        This operation returns firmwares for a given model name and version name.
        :param product_name: The Name of the product (e.g. IBR200)
        :param firmware_name: The Firmware Version (e.g. 7.2.0)

        :return:
        """
        product_id = self.get_product_by_name(product_name)['id']
        return self.get_firmware_for_productid_by_version(product_id, firmware_name)

    def get_groups(self, **kwargs):
        """
        This method gives a groups list.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Groups'
        geturl = '{0}/groups/'.format(self.base_url)

        allowed_params = ['account', 'account__in', 'id', 'id__in', 'name', 'name__in', 'expand', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_group_by_id(self, group_id):
        """
        This method returns a single group.
        :param group_id: The ID of the group.

        :return:
        """
        return self.get_groups(id=group_id)[0]

    def get_group_by_name(self, group_name):
        """
        This method returns a single group.
        :param group_name: The Name of the group.

        :return:
        """
        return self.get_groups(name=group_name)[0]

    def create_group_by_parent_id(self, parent_account_id, group_name, product_name, firmware_version):
        """This operation creates a new group.

        :param parent_account_id: ID of parent account
        :param group_name: Name for new group
        :param product_name: Product model (e.g. IBR200)
        :param firmware_version: Firmware version for group (e.g. 7.2.0)

        :return:

        Example: n.create_group_by_parent_id('123456', 'My New Group', 'IBR200', '7.2.0')
        """

        call_type = 'Group'
        posturl = '{0}/groups/'.format(self.base_url)

        firmware = self.get_firmware_for_productname_by_version(product_name, firmware_version)

        postdata = {
            'account': '/api/v1/accounts/{}/'.format(str(parent_account_id)),
            'name': str(group_name),
            'product': str(self.get_product_by_name(product_name)['resource_url']),
            'target_firmware': str(firmware['resource_url'])
        }

        ncm = self.session.post(posturl, data=json.dumps(postdata))
        result = self.__returnhandler(ncm.status_code, ncm.json(), call_type)
        return result

    def create_group_by_parent_name(self, parent_account_name, group_name, product_name, firmware_version):
        """
        This operation creates a new group.

        :param parent_account_name: Name of parent account
        :param group_name: Name for new group
        :param product_name: Product model (e.g. IBR200)
        :param firmware_version: Firmware version for group (e.g. 7.2.0)
        :return:

        Example: n.create_group_by_parent_name('Parent Account', 'My New Group', 'IBR200', '7.2.0')
        """

        return self.create_group_by_parent_id(
            self.get_account_by_name(parent_account_name)['id'], group_name, product_name,
            firmware_version)

    def rename_group_by_id(self, group_id, new_group_name):
        """
        This operation renames a group by specifying ID.
        :param group_id: ID of the group to rename.
        :param new_group_name: New name for the group.

        :return:
        """
        call_type = 'Group'
        puturl = '{0}/groups/{1}/'.format(self.base_url, group_id)

        putdata = {
            "name": str(new_group_name)
        }

        ncm = self.session.put(puturl, data=json.dumps(putdata))
        result = self.__returnhandler(ncm.status_code, ncm.json(), call_type)
        return result

    def rename_group_by_name(self, existing_group_name, new_group_name):
        """
        This operation renames a group by specifying name.
        :param existing_group_name: Name of the group to rename
        :param new_group_name: New name for the group.

        :return:
        """
        return self.rename_group_by_id(
            self.get_group_by_name(existing_group_name)['id'], new_group_name)

    def delete_group_by_id(self, group_id):
        """
        This operation deletes a group by specifying ID.
        :param group_id: ID of the group to delete

        :return:
        """
        call_type = 'Group'
        posturl = '{0}/groups/{1}/'.format(self.base_url, group_id)

        ncm = self.session.delete(posturl)
        result = self.__returnhandler(ncm.status_code, ncm.text, call_type)
        return result

    def delete_group_by_name(self, group_name):
        """
        This operation deletes a group by specifying Name.
        :param group_name: Name of the group to delete

        :return:
        """
        return self.delete_group_by_id(
            self.get_group_by_name(group_name)['id'])

    def get_historical_locations(self, router_id, **kwargs):
        """
        This method returns a list of locations visited by a device.
        :param router_id: ID of the router

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Historical Locations'
        geturl = '{0}/historical_locations/?router={1}'.format(self.base_url, router_id)

        allowed_params = ['created_at__gt', 'created_at_timeuuid__gt', 'created_at__lte', 'order_by', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_locations(self, **kwargs):
        """
        This method gives a list of locations.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Locations'
        geturl = '{0}/locations/'.format(self.base_url)

        allowed_params = ['id', 'id__in', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_net_device_health(self, **kwargs):
        """
        This operation gets cellular heath scores, by device.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Net Device Health'
        geturl = '{0}/net_device_health/'.format(self.base_url)

        allowed_params = ['net_device']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_net_device_metrics(self, **kwargs):
        """
        This endpoint is supplied to allow easy access to the latest signal and usage data reported by an account’s
        net_devices without querying the historical raw sample tables, which are not optimized for a query spanning
        many net_devices at once.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Net Device Metrics'
        geturl = '{0}/net_device_metrics/'.format(self.base_url)

        allowed_params = ['net_device', 'net_device__in', 'update_ts__lt', 'update_ts__gt', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_net_device_signal_samples(self, **kwargs):
        """
        This endpoint is supplied to allow easy access to the latest signal and usage data reported by an account’s
        net_devices without querying the historical raw sample tables, which are not optimized for a query spanning
        many net_devices at once.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Get Net Device Signal Samples'
        geturl = '{0}/net_device_signal_samples/'.format(self.base_url)

        allowed_params = ['net_device', 'net_device__in', 'created_at', 'created_at__lt', 'created_at__gt',
                          'created_at_timeuuid', 'created_at_timeuuid__in', 'created_at_timeuuid__gt',
                          'created_at_timeuuid__gte', 'created_at_timeuuid__lt', 'created_at_timeuuid__lte',
                          'order_by', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_net_device_usage_samples(self, **kwargs):
        """
        This method provides information about the net device's overall network traffic.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Net Device Usage Samples'
        geturl = '{0}/net_device_usage_samples/'.format(self.base_url)

        allowed_params = ['net_device', 'net_device__in', 'created_at', 'created_at__lt', 'created_at__gt',
                          'created_at_timeuuid', 'created_at_timeuuid__in', 'created_at_timeuuid__gt',
                          'created_at_timeuuid__gte', 'created_at_timeuuid__lt', 'created_at_timeuuid__lte',
                          'order_by', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_net_devices(self, **kwargs):
        """
        This method gives a list of net devices.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Net Devices'
        geturl = '{0}/net_devices/'.format(self.base_url)

        allowed_params = ['account', 'account__in', 'connection_state', 'connection_state__in', 'id', 'id__in',
                          'is_asset', 'ipv4_address', 'ipv4_address', 'mode', 'mode__in', 'router', 'router__in',
                          'expand', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    # TODO handle kwargs
    def get_net_devices_for_router(self, router_id, **kwargs):
        """
        This method gives a list of net devices for a given router.
        :param router_id: ID of the router

        :return:
        """
        return self.get_net_devices(router=router_id)

    def get_net_devices_metrics_for_wan(self, **kwargs):
        """
        This endpoint is supplied to allow easy access to the latest signal and usage data reported by an account’s
        net_devices without querying the historical raw sample tables, which are not optimized for a query spanning
        many net_devices at once. Returns data only for WAN interfaces.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        ids = []
        for net_device in self.get_net_devices(mode='wan'):
            ids.append(net_device['id'])
        idstring = ','.join(str(x) for x in ids)
        return self.get_net_device_metrics(net_device__in=idstring)

    def get_net_devices_metrics_for_mdm(self, **kwargs):
        """
        This endpoint is supplied to allow easy access to the latest signal and usage data reported by an account’s
        net_devices without querying the historical raw sample tables, which are not optimized for a query spanning
        many net_devices at once. Returns data only for Modem interfaces.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        ids = []
        for net_device in self.get_net_devices(is_asset=True):
            ids.append(net_device['id'])
        idstring = ','.join(str(x) for x in ids)
        return self.get_net_device_metrics(net_device__in=idstring)

    def get_net_devices_for_router_by_mode(self, router_id, mode, **kwargs):
        """
        This method gives a list of net devices for a given router, filtered by mode (lan/wan).
        :param router_id: ID of router
        :param mode: lan/wan

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        return self.get_net_devices(router=router_id, mode=mode)

    def get_products(self, **kwargs):
        """
        This method gives a list of product information.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Products'
        geturl = '{0}/products/'.format(self.base_url)

        allowed_params = ['id', 'id__in', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_product_by_id(self, product_id):
        """
        This method returns a single product by ID.
        :param product_id: ID of product (e.g. 46)

        :return:
        """
        return self.get_products(id=product_id)[0]

    def get_product_by_name(self, product_name):
        """
        This method returns a single product for a given model name.
        :param product_name: Name of product (e.g. IBR200)

        :return:
        """
        for p in self.get_products():
            if p['name'] == product_name:
                return p
        raise ValueError("Invalid Product Name")
        return

    def reboot_device(self, router_id):
        """
        This operation reboots a device.
        :param router_id: ID of router to reboot

        :return:
        """
        call_type = 'Reboot Device'
        posturl = '{0}/reboot_activity/'.format(self.base_url)

        postdata = {
            'router': '{0}/routers/{1}/'.format(self.base_url, str(router_id))
        }

        ncm = self.session.post(posturl, data=json.dumps(postdata))
        result = self.__returnhandler(ncm.status_code, ncm.text, call_type)
        return result

    def reboot_group(self, group_id):
        """
        This operation reboots all routers in a group.
        :param group_id: ID of group to reboot

        :return:
        """
        call_type = 'Reboot Group'
        posturl = '{0}/reboot_activity/'.format(self.base_url)

        postdata = {
            'group': '{0}/groups/{1}/'.format(self.base_url, str(group_id))
        }

        ncm = self.session.post(posturl, data=json.dumps(postdata))
        result = self.__returnhandler(ncm.status_code, ncm.text, call_type)
        return result

    def get_router_alerts(self, **kwargs):
        """
        This method provides a history of device alerts. To receive device alerts, you must enable them
        through the ECM UI: Alerts -> Settings. The info section of the alert is firmware dependent and
        may change between firmware releases.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Router Alerts'
        geturl = '{0}/router_alerts/'.format(self.base_url)

        allowed_params = ['router', 'router__in', 'created_at', 'created_at__lt', 'created_at__gt',
                          'created_at_timeuuid', 'created_at_timeuuid__in', 'created_at_timeuuid__gt',
                          'created_at_timeuuid__gte', 'created_at_timeuuid__lt', 'created_at_timeuuid__lte',
                          'order_by', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_router_alerts_last_24hrs(self, tzoffset_hrs=0, **kwargs):
        """
        This method provides a history of device alerts. To receive device alerts, you must enable them
        through the ECM UI: Alerts -> Settings. The info section of the alert is firmware dependent and
        may change between firmware releases.
        :param tzoffset_hrs: Offset from UTC for local timezone
        :type tzoffset_hrs: int

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        d = datetime.utcnow() + timedelta(hours=tzoffset_hrs)
        end = d.strftime("%Y-%m-%dT%H:%M:%S")
        start = (d - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%S")

        call_type = 'Router Alerts'
        geturl = '{0}/router_alerts/'.format(self.base_url)

        allowed_params = ['router', 'router__in']
        params = self.__parse_kwargs(kwargs, allowed_params)

        params.update({'created_at__lt': end,
                       'created_at__gt': start,
                       'order_by': 'created_at_timeuuid',
                       'limit': '500'})

        return self.__get_json(geturl, call_type, params=params)

    def get_router_alerts_for_date(self, date, tzoffset_hrs=0, **kwargs):
        """
        This method provides a history of device alerts. To receive device alerts, you must enable them
        through the ECM UI: Alerts -> Settings. The info section of the alert is firmware dependent and
        may change between firmware releases.
        :param date: Date to filter logs. Must be in format "YYYY-mm-dd"
        :type date: str
        :param tzoffset_hrs: Offset from UTC for local timezone
        :type tzoffset_hrs: int

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """

        d = datetime.strptime(date, '%Y-%m-%d') + timedelta(hours=tzoffset_hrs)
        start = d.strftime("%Y-%m-%dT%H:%M:%S")
        end = (d + timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%S")

        call_type = 'Router Alerts'
        geturl = '{0}/router_alerts/'.format(self.base_url)

        allowed_params = ['router', 'router__in']
        params = self.__parse_kwargs(kwargs, allowed_params)

        params.update({'created_at__lt': end,
                       'created_at__gt': start,
                       'order_by': 'created_at_timeuuid',
                       'limit': '500'})

        return self.__get_json(geturl, call_type, params=params)

    def get_router_logs(self, router_id, **kwargs):
        """
        This method provides a history of device events. To receive device logs, you must enable them on the
        Group settings form. Enabling device logs can significantly increase the ECM network traffic from the
        device to the server depending on how quickly the device is generating events.
        :param router_id: ID of router from which to grab logs.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Router Logs'
        geturl = '{0}/router_logs/?router={1}'.format(self.base_url, router_id)

        allowed_params = ['created_at', 'created_at__lt', 'created_at__gt', 'created_at_timeuuid',
                          'created_at_timeuuid__in', 'created_at_timeuuid__gt', 'created_at_timeuuid__gte',
                          'created_at_timeuuid__lt', 'created_at_timeuuid__lte', 'order_by', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_router_logs_last_24hrs(self, router_id, tzoffset_hrs=0):
        """
        This method provides a history of device events. To receive device logs, you must enable them on the
        Group settings form. Enabling device logs can significantly increase the ECM network traffic from the
        device to the server depending on how quickly the device is generating events.
        :param router_id: ID of router from which to grab logs.
        :param tzoffset_hrs: Offset from UTC for local timezone
        :type tzoffset_hrs: int

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        d = datetime.utcnow() + timedelta(hours=tzoffset_hrs)
        end = d.strftime("%Y-%m-%dT%H:%M:%S")
        start = (d - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%S")

        call_type = 'Router Logs'
        geturl = '{0}/router_logs/?router={1}'.format(self.base_url, router_id)

        params = {'created_at__lt': end, 'created_at__gt': start, 'order_by': 'created_at_timeuuid', 'limit': '500'}

        return self.__get_json(geturl, call_type, params=params)

    def get_router_logs_for_date(self, router_id, date, tzoffset_hrs=0):
        """
        This method provides a history of device events. To receive device logs, you must enable them on the
        Group settings form. Enabling device logs can significantly increase the ECM network traffic from the
        device to the server depending on how quickly the device is generating events.
        :param router_id: ID of router from which to grab logs.
        :param date: Date to filter logs. Must be in format "YYYY-mm-dd"
        :type date: str
        :param tzoffset_hrs: Offset from UTC for local timezone
        :type tzoffset_hrs: int

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """

        d = datetime.strptime(date, '%Y-%m-%d') + timedelta(hours=tzoffset_hrs)
        start = d.strftime("%Y-%m-%dT%H:%M:%S")
        end = (d + timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%S")

        call_type = 'Router Logs'
        geturl = '{0}/router_logs/?router={1}'.format(self.base_url, router_id)

        params = {'created_at__lt': end, 'created_at__gt': start, 'order_by': 'created_at_timeuuid', 'limit': '500'}

        return self.__get_json(geturl, call_type, params=params)

    def get_router_state_samples(self, **kwargs):
        """
        This method provides information about the connection state of the device with the ECM server.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Router State Samples'
        geturl = '{0}/router_state_samples/'.format(self.base_url)

        allowed_params = ['router', 'router__in', 'created_at', 'created_at__lt', 'created_at__gt',
                          'created_at_timeuuid', 'created_at_timeuuid__in', 'created_at_timeuuid__gt',
                          'created_at_timeuuid__gte', 'created_at_timeuuid__lt', 'created_at_timeuuid__lte',
                          'order_by', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_router_stream_usage_samples(self, **kwargs):
        """
        This method provides information about the connection state of the device with the ECM server.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Router Stream Usage Samples'
        geturl = '{0}/router_stream_usage_samples/'.format(self.base_url)

        allowed_params = ['router', 'router__in', 'created_at', 'created_at__lt', 'created_at__gt',
                          'created_at_timeuuid', 'created_at_timeuuid__in', 'created_at_timeuuid__gt',
                          'created_at_timeuuid__gte', 'created_at_timeuuid__lt', 'created_at_timeuuid__lte',
                          'order_by', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_routers(self, **kwargs):
        """
        This method gives device information with associated id.

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        call_type = 'Routers'
        geturl = '{0}/routers/'.format(self.base_url)

        allowed_params = ['account', 'account__in', 'group', 'group__in', 'id', 'id__in',
                          'ipv4_address', 'ipv4_address__in', 'mac', 'mac__in', 'name', 'name__in', 'state',
                          'state__in', 'state_updated_at__lt', 'state_updated_at__gt', 'updated_at__lt',
                          'updated_at__gt', 'expand', 'order_by', 'limit', 'offset']
        params = self.__parse_kwargs(kwargs, allowed_params)

        return self.__get_json(geturl, call_type, params=params)

    def get_router_by_id(self, router_id, **kwargs):
        """
        This method gives device information for a given router ID.
        :param router_id: ID of router

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        return self.get_routers(id=router_id, **kwargs)[0]

    def get_router_by_name(self, router_name, **kwargs):
        """
        This method gives device information for a given router name.
        :param router_name: Name of router

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        return self.get_routers(name=router_name, **kwargs)[0]

    def get_routers_for_account(self, account_id, **kwargs):
        """
        This method gives a groups list filtered by account.
        :param account_id: Account ID to filter

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        return self.get_routers(account=account_id, **kwargs)

    def get_routers_for_group(self, group_id, **kwargs):
        """
        This method gives a groups list filtered by group.
        :param group_id: Group ID to filter

        :param kwargs: A set of zero or more allowed parameters in the allowed_params list.
        :return:
        """
        return self.get_routers(group=group_id, **kwargs)

    def rename_router_by_id(self, router_id, new_router_name):
        """
        This operation renames a router by ID.
        :param router_id: ID of router to rename
        :param new_router_name: New name for router

        :return:
        """
        call_type = 'Router'
        puturl = '{0}/routers/{1}/'.format(self.base_url, router_id)

        putdata = {
            'name': str(new_router_name)
        }

        ncm = self.session.put(puturl, data=json.dumps(putdata))
        result = self.__returnhandler(ncm.status_code, ncm.json(), call_type)
        return result

    def rename_router_by_name(self, existing_router_name, new_router_name):
        """
        This operation renames a router by name.
        :param existing_router_name: Name of router to rename
        :param new_router_name: New name for router

        :return:
        """
        return self.rename_router_by_id(
            self.get_router_by_name(existing_router_name)['id'], new_router_name)

    def delete_router_by_id(self, router_id):
        """
        This operation deletes a router by ID.
        :param router_id: ID of router to delete.

        :return:
        """
        call_type = 'Router'
        posturl = '{0}/routers/{1}/'.format(self.base_url, router_id)

        ncm = self.session.delete(posturl)
        result = self.__returnhandler(ncm.status_code, ncm.text, call_type)
        return result

    def delete_router_by_name(self, router_name):
        """
        This operation deletes a router by name.
        :param router_name: Name of router to delete

        :return:
        """
        return self.delete_router_by_id(
            self.get_router_by_name(router_name)['id'])

    def get_speed_test(self, speed_test_id):
        """
        Gets the results of a speed test job. The results are updated with the latest known state of the speed tests.
        :param speed_test_id: ID ot Speed Test

        :return:
        """
        call_type = 'Speed Test'
        geturl = '{0}/speed_test/{1}/'.format(self.base_url, str(speed_test_id))

        ncm = self.session.get(geturl)
        result = self.__returnhandler(ncm.status_code, ncm.json()['data'], call_type)
        return result

    # TODO create speed test

    def delete_speed_test(self, speed_test_id):
        """
        Deletes a speed test job. Deleting a job aborts it, but any test already started on a router will finish.
        :param speed_test_id: Speed Test ID to delete

        :return:
        """
        call_type = 'Speed Test'
        posturl = '{0}/speed_test/{1}'.format(self.base_url, str(speed_test_id))

        ncm = self.session.delete(posturl)
        result = self.__returnhandler(ncm.status_code, ncm.json(), call_type)
        return result

    def set_lan_ip_address(self, router_id, lan_ip):
        """
        This method sets the IP Address for the Primary LAN for a given router id.
        :param router_id: ID of router to update
        :param lan_ip: LAN IP Address. (e.g. 192.168.1.1)

        :return:
        """
        call_type = 'LAN IP Address'

        response = self.session.get('{0}/configuration_managers/?router.id={1}&fields=id'.format(
            self.base_url, str(router_id)))  # Get Configuration Managers ID for current Router from API
        response = json.loads(response.content.decode("utf-8"))  # Decode the response and make it a dictionary
        configman_id = response['data'][0]['id']  # get the Configuration Managers ID from response

        payload = {
            "configuration": [
                {
                    "lan": {
                        "00000000-0d93-319d-8220-4a1fb0372b51": {
                            "_id_": "00000000-0d93-319d-8220-4a1fb0372b51",
                            "ip_address": lan_ip
                        }
                    }
                },
                []
            ]
        }

        ncm = self.session.patch('{0}/configuration_managers/{1}/'.format(self.base_url, str(configman_id)),
                                 data=json.dumps(payload))  # Patch indie config with new values
        result = self.__returnhandler(ncm.status_code, ncm.text, call_type)
        return result
