################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

from __future__ import print_function
import requests
from watson_machine_learning_client.utils import SPACES_DETAILS_TYPE, INSTANCE_DETAILS_TYPE, MEMBER_DETAILS_TYPE,SW_SPEC_DETAILS_TYPE, STR_TYPE, STR_TYPE_NAME, docstring_parameter, meta_props_str_conv, str_type_conv, get_file_from_cos
from watson_machine_learning_client.metanames import SwSpecMetaNames
from watson_machine_learning_client.wml_resource import WMLResource
from watson_machine_learning_client.wml_client_error import WMLClientError, ApiRequestFailure
import os,json

_DEFAULT_LIST_LENGTH = 50


class SwSpec(WMLResource):
    """
    Store and manage your software specs.

    """
    ConfigurationMetaNames = SwSpecMetaNames()
    """MetaNames for Software Specification creation."""

    def __init__(self, client):
        WMLResource.__init__(self, __name__, client)
        self._ICP = client.ICP

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_details(self,sw_spec_uid=None):
        """
            Get software specification details.

            **Parameters**

            .. important::
                #. **sw_spec_details**:  Metadata of the stored sw_spec\n
                   **type**: dict\n

            **Output**

            .. important::
                **returns**: sw_spec UID\n
                **return type**: str

            **Example**

             >>> sw_spec_details = client.software_specifications.get_details(sw_spec_uid)

        """
        SwSpec._validate_type(sw_spec_uid, u'sw_spec_uid', STR_TYPE, True)


        if not self._ICP:
            response = requests.get(self._href_definitions.get_sw_spec_href(sw_spec_uid), params=self._client._params(),
                                    headers=self._client._get_headers())
        else:
            response = requests.get(self._href_definitions.get_sw_spec_href(sw_spec_uid), params=self._client._params(),
                                      headers=self._client._get_headers(), verify=False)
        if response.status_code == 200:
            return self._get_required_element_from_response(self._handle_response(200, u'get sw spec details', response))
        else:
            return self._handle_response(200, u'get sw spec details', response)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def store(self, meta_props):
        """
                Create a software specification.

                **Parameters**

                .. important::
                   #. **meta_props**:  meta data of the space configuration. To see available meta names use:\n
                                    >>> client.software_specifications.ConfigurationMetaNames.get()

                      **type**: dict\n

                **Output**

                .. important::

                    **returns**: metadata of the stored space\n
                    **return type**: dict\n

                **Example**

                 >>> meta_props = {
                 >>>    client.software_specifications.ConfigurationMetaNames.NAME: "skl_pipeline_heart_problem_prediction",
                 >>>    client.software_specifications.ConfigurationMetaNames.DESCRIPTION: "description scikit-learn_0.20",
                 >>>    client.software_specifications.ConfigurationMetaNames.PACKAGE_EXTENSIONS_UID: [],
                 >>>    client.software_specifications.ConfigurationMetaNames.SOFTWARE_CONFIGURATIONS: {},
                 >>>    client.software_specifications.ConfigurationMetaNames.BASE_SOFTWARE_SPECIFICATION_ID: "guid"
                 >>> }

        """

        SwSpec._validate_type(meta_props, u'meta_props', dict, True)
        sw_spec_meta = self.ConfigurationMetaNames._generate_resource_metadata(
            meta_props,
            with_validation=True,
            client=self._client)

        sw_spec_meta_json = json.dumps(sw_spec_meta)
        href = self._href_definitions.get_sw_specs_href()

        if not self._ICP:
            creation_response = requests.post(href, params=self._client._params(), headers=self._client._get_headers(), data=sw_spec_meta_json)
        else:
            creation_response = requests.post(href, params=self._client._params(), headers=self._client._get_headers(), data=sw_spec_meta_json, verify=False)

        sw_spec_details = self._handle_response(201, u'creating sofware specifications', creation_response)

        return sw_spec_details


    def list(self):
        """
           List software specifications.

           **Output**

           .. important::
                This method only prints the list of all software specifications in a table format.\n
                **return type**: None\n

           **Example**

            >>> client.software_specifications.list()
        """

        # Todo provide api to return
        href = self._href_definitions.get_sw_specs_href()


        if not self._ICP:
            response = requests.get(href, params=self._client._params(), headers=self._client._get_headers())
        else:
            response = requests.get(href, params=self._client._params(), headers=self._client._get_headers(), verify=False)
        self._handle_response(200, u'list sw_specs', response)
        asset_details = self._handle_response(200, u'list assets', response)["resources"]
        sw_spec_values = [
            (m[u'metadata'][u'name'], m[u'metadata'][u'asset_id'],m[u'entity'][u'software_specification'][u'type']) for
            m in asset_details]

        self._list(sw_spec_values, [u'NAME', u'ASSET_ID', u'TYPE'], None, _DEFAULT_LIST_LENGTH)


    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_uid(sw_spec_details):
        """
                Get Unique Id of software specification.

                **Parameters**

                .. important::

                   #. **sw_spec_details**:  Metadata of the software specification\n
                      **type**: dict\n

                **Output**

                .. important::

                    **returns**: Unique Id of software specification \n
                    **return type**: str\n

                **Example**


                 >>> asset_uid = client.software_specifications.get_uid(sw_spec_details)

        """
        SwSpec._validate_type(sw_spec_details, u'sw_spec_details', object, True)
        SwSpec._validate_type_of_details(sw_spec_details, SW_SPEC_DETAILS_TYPE)

        return WMLResource._get_required_element_from_dict(sw_spec_details, u'sw_spec_details',
                                                           [u'metadata', u'asset_id'])



    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_uid_by_name(self, sw_spec_name):
        """
                Get Unique Id of software specification.

                **Parameters**

                .. important::

                   #. **sw_spec_name**:  Name of the software specification\n
                      **type**: str\n

                **Output**

                .. important::

                    **returns**: Unique Id of software specification \n
                    **return type**: str\n

                **Example**


                 >>> asset_uid = client.software_specifications.get_uid_by_name(sw_spec_name)

        """

        SwSpec._validate_type(sw_spec_name, u'sw_spec_uid', STR_TYPE, True)
        parameters = self._client._params()
        parameters.update(name=sw_spec_name)
        if not self._ICP:
            response = requests.get(self._href_definitions.get_sw_specs_href(),
                                    params=parameters,
                                    headers=self._client._get_headers())
        else:

            response = requests.get(self._href_definitions.get_sw_specs_href(),
                                    params=parameters,
                                    headers=self._client._get_headers(), verify=False)
        if response.status_code == 200:
            total_values = self._handle_response(200, u'list assets', response)["total_results"]
            if total_values != 0:
                sw_spec_details = self._handle_response(200, u'list assets', response)["resources"]
                return sw_spec_details[0][u'metadata'][u'asset_id']
            else:
                return "Not Found"



    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_href(sw_spec_details):
        """
            Get url of software specification.

           **Parameters**

           .. important::
                #. **sw_spec_details**:  software specification details\n
                   **type**: dict\n

           **Output**

           .. important::
                **returns**: href of software specification \n
                **return type**: str\n

           **Example**

             >>> sw_spec_details = client.software_specifications.get_details(sw_spec_uid)
             >>> sw_spec_href = client.software_specifications.get_href(sw_spec_details)

        """
        SwSpec._validate_type(sw_spec_details, u'sw_spec_details', object, True)
        SwSpec._validate_type_of_details(sw_spec_details, SW_SPEC_DETAILS_TYPE)

        return WMLResource._get_required_element_from_dict(sw_spec_details, u'sw_spec_details', [u'metadata', u'href'])


    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def delete(self, sw_spec_uid):
        """
            Delete a software specification.

            **Parameters**

            .. important::
                #. **sw_spec_uid**: Unique Id of software specification\n
                   **type**: str\n

            **Output**

            .. important::
                **returns**: status ("SUCCESS" or "FAILED")\n
                **return type**: str\n

            **Example**

             >>> client.software_specifications.delete(sw_spec_uid)

        """
        SwSpec._validate_type(sw_spec_uid, u'sw_spec_uid', STR_TYPE, True)

        if not self._ICP:
            response = requests.delete(self._href_definitions.get_sw_spec_href(sw_spec_uid), params=self._client._params(),
                                    headers=self._client._get_headers())
        else:
            response = requests.delete(self._href_definitions.get_sw_spec_href(sw_spec_uid), params=self._client._params(),
                                      headers=self._client._get_headers(), verify=False)
        if response.status_code == 200:
            return self._get_required_element_from_response(response.json())
        else:
            return self._handle_response(204, u'delete software specification', response)


    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def add_package_extension(self, sw_spec_uid, pkg_extn_id):
        """
                Add a package extension to software specifications existing metadata.

                **Parameters**

                .. important::

                    #. **sw_spec_uid**:  Unique Id of software specification which should be updated\n
                       **type**: str\n
                    #. **pkg_extn_id**:  Unique Id of package extension which should needs to added to software specification\n
                       **type**: str\n

                **Example**

                >>> client.software_specifications.add_package_extension(sw_spec_uid, pkg_extn_id)

        """
        ##For CP4D, check if either spce or project ID is set
        self._client._check_if_either_is_set()

        sw_spec_uid = str_type_conv(sw_spec_uid)
        self._validate_type(sw_spec_uid, u'sw_spec_uid', STR_TYPE, True)
        self._validate_type(pkg_extn_id, u'pkg_extn_id', STR_TYPE, True)

        url = self._href_definitions.get_sw_spec_href(sw_spec_uid)

        url = url + "/package_extensions/" + pkg_extn_id


        if not self._ICP:
            response = requests.put(url, params=self._client._params(),headers=self._client._get_headers())
        else:
            response = requests.put(url,  params=self._client._params(),headers=self._client._get_headers(), verify=False)
            if response.status_code == 204:
                return "SUCCESS"
            else:
                return self._handle_response(204, u'pkg spec add', response, False)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def delete_package_extension(self, sw_spec_uid, pkg_extn_id):
        """
                Delete a package extension from software specifications existing metadata.

                **Parameters**

                .. important::

                    #. **sw_spec_uid**:  Unique Id of software specification which should be updated\n
                       **type**: str\n
                    #. **pkg_extn_id**:  Unique Id of package extension which should needs to deleted from software specification\n
                       **type**: str\n

                **Example**

                >>>> client.software_specifications.delete_package_extension(sw_spec_uid, pkg_extn_id)

        """

        ##For CP4D, check if either spce or project ID is set
        self._client._check_if_either_is_set()

        sw_spec_uid = str_type_conv(sw_spec_uid)
        self._validate_type(sw_spec_uid, u'sw_spec_uid', STR_TYPE, True)
        self._validate_type(pkg_extn_id, u'pkg_extn_id', STR_TYPE, True)

        url = self._href_definitions.get_sw_spec_href(sw_spec_uid)

        url = url + "/package_extensions/" + pkg_extn_id


        if not self._ICP:
            response = requests.delete(url, params=self._client._params(),
                                    headers=self._client._get_headers())
        else:
            response = requests.delete(url, params=self._client._params(),
                                    headers=self._client._get_headers(), verify=False)

        return self._handle_response(204, u'pkg spec delete', response, False)



    def _get_required_element_from_response(self, response_data):

        WMLResource._validate_type(response_data, u'sw_spec_response', dict)
        try:
            if self._client.default_space_id is not None:
                new_el = {'metadata': {
                                       'name': response_data['metadata']['name'],
                                       'asset_id': response_data['metadata']['asset_id'],
                                       'href': response_data['metadata']['href'],
                                       'asset_type': response_data['metadata']['asset_type'],
                                       'created_at': response_data['metadata']['created_at']
                                       #'updated_at': response_data['metadata']['updated_at']
                                       },
                          'entity': response_data['entity']

                          }
            elif self._client.default_project_id is not None:
                if self._client.WSD:

                    href = "/v2/assets/" + response_data['metadata']['asset_id'] + "?" + "project_id=" + response_data['metadata']['project_id']

                    new_el = {'metadata': {
                                           'name': response_data['metadata']['name'],
                                           'asset_id': response_data['metadata']['asset_id'],
                                           'href': response_data['metadata']['href'],
                                           'asset_type': response_data['metadata']['asset_type'],
                                           'created_at': response_data['metadata']['created_at']
                                           },
                              'entity': response_data['entity']

                              }
                else:
                    new_el = {'metadata': {
                                           'name': response_data['metadata']['name'],
                                           'asset_id': response_data['metadata']['asset_id'],
                                           'href': response_data['metadata']['href'],
                                           'asset_type': response_data['metadata']['asset_type'],
                                           'created_at': response_data['metadata']['created_at']
                                       },
                             'entity': response_data['entity']

                            }
            return new_el
        except Exception as e:
            raise WMLClientError("Failed to read Response from down-stream service: " + response_data.text)
