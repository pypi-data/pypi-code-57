# coding: utf-8

"""
    IncQuery Server Web API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    OpenAPI spec version: 0.15.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from iqs_client.api_client import ApiClient


class ImpactAnalysisApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def list_dependencies(self, md_object_id_list, **kwargs):  # noqa: E501
        """Calculates the impact of given Elements, listing elements referring to each  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_dependencies(md_object_id_list, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MDObjectIDList md_object_id_list: List of MDObject IDs (local identifier) of model elements  (required)
        :return: ListDependenciesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_dependencies_with_http_info(md_object_id_list, **kwargs)  # noqa: E501
        else:
            (data) = self.list_dependencies_with_http_info(md_object_id_list, **kwargs)  # noqa: E501
            return data

    def list_dependencies_with_http_info(self, md_object_id_list, **kwargs):  # noqa: E501
        """Calculates the impact of given Elements, listing elements referring to each  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_dependencies_with_http_info(md_object_id_list, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MDObjectIDList md_object_id_list: List of MDObject IDs (local identifier) of model elements  (required)
        :return: ListDependenciesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['md_object_id_list']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_dependencies" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'md_object_id_list' is set
        if ('md_object_id_list' not in local_var_params or
                local_var_params['md_object_id_list'] is None):
            raise ValueError("Missing the required parameter `md_object_id_list` when calling `list_dependencies`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'md_object_id_list' in local_var_params:
            body_params = local_var_params['md_object_id_list']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/impact-analysis.listDependencies', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ListDependenciesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_revisions_with_dependencies(self, md_object_id_list, **kwargs):  # noqa: E501
        """Calculates the impact of given Elements, listing revisions with elements referring to each  # noqa: E501

        Returns revisions containing elements depending on the specified Elements   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_revisions_with_dependencies(md_object_id_list, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MDObjectIDList md_object_id_list: List of MDObject IDs (local identifier) of model elements  (required)
        :return: ListRevisionsWithDependenciesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_revisions_with_dependencies_with_http_info(md_object_id_list, **kwargs)  # noqa: E501
        else:
            (data) = self.list_revisions_with_dependencies_with_http_info(md_object_id_list, **kwargs)  # noqa: E501
            return data

    def list_revisions_with_dependencies_with_http_info(self, md_object_id_list, **kwargs):  # noqa: E501
        """Calculates the impact of given Elements, listing revisions with elements referring to each  # noqa: E501

        Returns revisions containing elements depending on the specified Elements   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_revisions_with_dependencies_with_http_info(md_object_id_list, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MDObjectIDList md_object_id_list: List of MDObject IDs (local identifier) of model elements  (required)
        :return: ListRevisionsWithDependenciesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['md_object_id_list']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_revisions_with_dependencies" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'md_object_id_list' is set
        if ('md_object_id_list' not in local_var_params or
                local_var_params['md_object_id_list'] is None):
            raise ValueError("Missing the required parameter `md_object_id_list` when calling `list_revisions_with_dependencies`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'md_object_id_list' in local_var_params:
            body_params = local_var_params['md_object_id_list']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/impact-analysis.listRevisionsWithDependencies', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ListRevisionsWithDependenciesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def register_md_object_i_ds(self, md_object_id_list, **kwargs):  # noqa: E501
        """Registers a list of Elements that should have their dependency information preloaded  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.register_md_object_i_ds(md_object_id_list, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MDObjectIDList md_object_id_list: List of MDObject IDs (local identifier) of model elements  (required)
        :return: SimpleMessage
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.register_md_object_i_ds_with_http_info(md_object_id_list, **kwargs)  # noqa: E501
        else:
            (data) = self.register_md_object_i_ds_with_http_info(md_object_id_list, **kwargs)  # noqa: E501
            return data

    def register_md_object_i_ds_with_http_info(self, md_object_id_list, **kwargs):  # noqa: E501
        """Registers a list of Elements that should have their dependency information preloaded  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.register_md_object_i_ds_with_http_info(md_object_id_list, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MDObjectIDList md_object_id_list: List of MDObject IDs (local identifier) of model elements  (required)
        :return: SimpleMessage
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['md_object_id_list']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method register_md_object_i_ds" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'md_object_id_list' is set
        if ('md_object_id_list' not in local_var_params or
                local_var_params['md_object_id_list'] is None):
            raise ValueError("Missing the required parameter `md_object_id_list` when calling `register_md_object_i_ds`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'md_object_id_list' in local_var_params:
            body_params = local_var_params['md_object_id_list']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/impact-analysis.register', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SimpleMessage',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def unregister_md_object_i_ds(self, md_object_id_list, **kwargs):  # noqa: E501
        """Unregisters a list of Elements that were previously registered  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.unregister_md_object_i_ds(md_object_id_list, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MDObjectIDList md_object_id_list: List of MDObject IDs (local identifier) of model elements  (required)
        :return: SimpleMessage
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.unregister_md_object_i_ds_with_http_info(md_object_id_list, **kwargs)  # noqa: E501
        else:
            (data) = self.unregister_md_object_i_ds_with_http_info(md_object_id_list, **kwargs)  # noqa: E501
            return data

    def unregister_md_object_i_ds_with_http_info(self, md_object_id_list, **kwargs):  # noqa: E501
        """Unregisters a list of Elements that were previously registered  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.unregister_md_object_i_ds_with_http_info(md_object_id_list, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MDObjectIDList md_object_id_list: List of MDObject IDs (local identifier) of model elements  (required)
        :return: SimpleMessage
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['md_object_id_list']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method unregister_md_object_i_ds" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'md_object_id_list' is set
        if ('md_object_id_list' not in local_var_params or
                local_var_params['md_object_id_list'] is None):
            raise ValueError("Missing the required parameter `md_object_id_list` when calling `unregister_md_object_i_ds`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'md_object_id_list' in local_var_params:
            body_params = local_var_params['md_object_id_list']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/impact-analysis.unregister', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SimpleMessage',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
