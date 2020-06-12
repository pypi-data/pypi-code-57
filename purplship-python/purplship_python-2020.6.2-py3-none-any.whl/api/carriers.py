# coding: utf-8

"""
    PurplShip Multi-carrier API

    PurplShip is a Multi-carrier Shipping API that simplifies the integration of logistic carrier services  # noqa: E501

    OpenAPI spec version: v1
    Contact: hello@purplship.com
    Generated by: https://github.com/purplship-api/purplship-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from purplship.client import ApiClient


class Carriers(object):
    """NOTE: This class is auto generated by the purplship code generator program.

    Do not edit the class manually.
    Ref: https://github.com/purplship-api/purplship-codegen
    """

    def __init__(self, client=None):
        if client is None:
            client = ApiClient()
        self.client = client

    def retrieve(self, **kwargs):  # noqa: E501
        """retrieve  # noqa: E501

        Returns the list of configured carriers  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.retrieve(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str carrier_name: Indicates a carrier (type)
        :param str carrier_id: Indicates a specific carrier configuration name.
        :param bool test:  The test flag indicates whether to use a carrier configured for test.  
        :return: list[CarrierSettings]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.retrieve_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.retrieve_with_http_info(**kwargs)  # noqa: E501
            return data

    def retrieve_with_http_info(self, **kwargs):  # noqa: E501
        """retrieve  # noqa: E501

        Returns the list of configured carriers  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.retrieve_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str carrier_name: Indicates a carrier (type)
        :param str carrier_id: Indicates a specific carrier configuration name.
        :param bool test:  The test flag indicates whether to use a carrier configured for test.  
        :return: list[CarrierSettings]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['carrier_name', 'carrier_id', 'test']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method retrieve" % key
                )
            params[key] = val
        del params['kwargs']

        if ('carrier_id' in params and
                len(params['carrier_id']) < 1):
            raise ValueError("Invalid value for parameter `carrier_id` when calling `retrieve`, length must be greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'carrier_name' in params:
            query_params.append(('carrierName', params['carrier_name']))  # noqa: E501
        if 'carrier_id' in params:
            query_params.append(('carrierId', params['carrier_id']))  # noqa: E501
        if 'test' in params:
            query_params.append(('test', params['test']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Token']  # noqa: E501

        return self.client.call_api(
            '/carriers', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[CarrierSettings]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
