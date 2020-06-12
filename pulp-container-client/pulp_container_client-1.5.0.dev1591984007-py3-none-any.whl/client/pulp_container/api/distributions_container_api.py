# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from pulpcore.client.pulp_container.api_client import ApiClient
from pulpcore.client.pulp_container.exceptions import (
    ApiTypeError,
    ApiValueError
)


class DistributionsContainerApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create(self, data, **kwargs):  # noqa: E501
        """Create a container distribution  # noqa: E501

        Trigger an asynchronous create task  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create(data, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param ContainerContainerDistribution data: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AsyncOperationResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.create_with_http_info(data, **kwargs)  # noqa: E501

    def create_with_http_info(self, data, **kwargs):  # noqa: E501
        """Create a container distribution  # noqa: E501

        Trigger an asynchronous create task  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_with_http_info(data, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param ContainerContainerDistribution data: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AsyncOperationResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['data']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'data' is set
        if self.api_client.client_side_validation and ('data' not in local_var_params or  # noqa: E501
                                                        local_var_params['data'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `data` when calling `create`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'data' in local_var_params:
            body_params = local_var_params['data']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Basic']  # noqa: E501

        return self.api_client.call_api(
            '/pulp/api/v3/distributions/container/container/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AsyncOperationResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete(self, container_distribution_href, **kwargs):  # noqa: E501
        """Delete a container distribution  # noqa: E501

        Trigger an asynchronous delete task  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete(container_distribution_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str container_distribution_href: URI of Container Distribution. e.g.: /pulp/api/v3/distributions/container/container/1/ (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AsyncOperationResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.delete_with_http_info(container_distribution_href, **kwargs)  # noqa: E501

    def delete_with_http_info(self, container_distribution_href, **kwargs):  # noqa: E501
        """Delete a container distribution  # noqa: E501

        Trigger an asynchronous delete task  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_with_http_info(container_distribution_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str container_distribution_href: URI of Container Distribution. e.g.: /pulp/api/v3/distributions/container/container/1/ (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AsyncOperationResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['container_distribution_href']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'container_distribution_href' is set
        if self.api_client.client_side_validation and ('container_distribution_href' not in local_var_params or  # noqa: E501
                                                        local_var_params['container_distribution_href'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `container_distribution_href` when calling `delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'container_distribution_href' in local_var_params:
            path_params['container_distribution_href'] = local_var_params['container_distribution_href']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Basic']  # noqa: E501

        return self.api_client.call_api(
            '{container_distribution_href}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AsyncOperationResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list(self, **kwargs):  # noqa: E501
        """List container distributions  # noqa: E501

        The Container Distribution will serve the latest version of a Repository if ``repository`` is specified. The Container Distribution will serve a specific repository version if ``repository_version``. Note that **either** ``repository`` or ``repository_version`` can be set on a Container Distribution, but not both.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str ordering: Which field to use when ordering the results.
        :param str name:
        :param str name__in: Filter results where name is in a comma-separated list of values
        :param str base_path:
        :param str base_path__contains: Filter results where base_path contains value
        :param str base_path__icontains: Filter results where base_path contains value
        :param str base_path__in: Filter results where base_path is in a comma-separated list of values
        :param int limit: Number of results to return per page.
        :param int offset: The initial index from which to return the results.
        :param str fields: A list of fields to include in the response.
        :param str exclude_fields: A list of fields to exclude from the response.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: InlineResponse2003
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.list_with_http_info(**kwargs)  # noqa: E501

    def list_with_http_info(self, **kwargs):  # noqa: E501
        """List container distributions  # noqa: E501

        The Container Distribution will serve the latest version of a Repository if ``repository`` is specified. The Container Distribution will serve a specific repository version if ``repository_version``. Note that **either** ``repository`` or ``repository_version`` can be set on a Container Distribution, but not both.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str ordering: Which field to use when ordering the results.
        :param str name:
        :param str name__in: Filter results where name is in a comma-separated list of values
        :param str base_path:
        :param str base_path__contains: Filter results where base_path contains value
        :param str base_path__icontains: Filter results where base_path contains value
        :param str base_path__in: Filter results where base_path is in a comma-separated list of values
        :param int limit: Number of results to return per page.
        :param int offset: The initial index from which to return the results.
        :param str fields: A list of fields to include in the response.
        :param str exclude_fields: A list of fields to exclude from the response.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(InlineResponse2003, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['ordering', 'name', 'name__in', 'base_path', 'base_path__contains', 'base_path__icontains', 'base_path__in', 'limit', 'offset', 'fields', 'exclude_fields']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'ordering' in local_var_params and local_var_params['ordering'] is not None:  # noqa: E501
            query_params.append(('ordering', local_var_params['ordering']))  # noqa: E501
        if 'name' in local_var_params and local_var_params['name'] is not None:  # noqa: E501
            query_params.append(('name', local_var_params['name']))  # noqa: E501
        if 'name__in' in local_var_params and local_var_params['name__in'] is not None:  # noqa: E501
            query_params.append(('name__in', local_var_params['name__in']))  # noqa: E501
        if 'base_path' in local_var_params and local_var_params['base_path'] is not None:  # noqa: E501
            query_params.append(('base_path', local_var_params['base_path']))  # noqa: E501
        if 'base_path__contains' in local_var_params and local_var_params['base_path__contains'] is not None:  # noqa: E501
            query_params.append(('base_path__contains', local_var_params['base_path__contains']))  # noqa: E501
        if 'base_path__icontains' in local_var_params and local_var_params['base_path__icontains'] is not None:  # noqa: E501
            query_params.append(('base_path__icontains', local_var_params['base_path__icontains']))  # noqa: E501
        if 'base_path__in' in local_var_params and local_var_params['base_path__in'] is not None:  # noqa: E501
            query_params.append(('base_path__in', local_var_params['base_path__in']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'offset' in local_var_params and local_var_params['offset'] is not None:  # noqa: E501
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'fields' in local_var_params and local_var_params['fields'] is not None:  # noqa: E501
            query_params.append(('fields', local_var_params['fields']))  # noqa: E501
        if 'exclude_fields' in local_var_params and local_var_params['exclude_fields'] is not None:  # noqa: E501
            query_params.append(('exclude_fields', local_var_params['exclude_fields']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Basic']  # noqa: E501

        return self.api_client.call_api(
            '/pulp/api/v3/distributions/container/container/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse2003',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def partial_update(self, container_distribution_href, data, **kwargs):  # noqa: E501
        """Partially update a container distribution  # noqa: E501

        Trigger an asynchronous partial update task  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.partial_update(container_distribution_href, data, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str container_distribution_href: URI of Container Distribution. e.g.: /pulp/api/v3/distributions/container/container/1/ (required)
        :param ContainerContainerDistribution data: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AsyncOperationResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.partial_update_with_http_info(container_distribution_href, data, **kwargs)  # noqa: E501

    def partial_update_with_http_info(self, container_distribution_href, data, **kwargs):  # noqa: E501
        """Partially update a container distribution  # noqa: E501

        Trigger an asynchronous partial update task  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.partial_update_with_http_info(container_distribution_href, data, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str container_distribution_href: URI of Container Distribution. e.g.: /pulp/api/v3/distributions/container/container/1/ (required)
        :param ContainerContainerDistribution data: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AsyncOperationResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['container_distribution_href', 'data']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method partial_update" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'container_distribution_href' is set
        if self.api_client.client_side_validation and ('container_distribution_href' not in local_var_params or  # noqa: E501
                                                        local_var_params['container_distribution_href'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `container_distribution_href` when calling `partial_update`")  # noqa: E501
        # verify the required parameter 'data' is set
        if self.api_client.client_side_validation and ('data' not in local_var_params or  # noqa: E501
                                                        local_var_params['data'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `data` when calling `partial_update`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'container_distribution_href' in local_var_params:
            path_params['container_distribution_href'] = local_var_params['container_distribution_href']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'data' in local_var_params:
            body_params = local_var_params['data']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Basic']  # noqa: E501

        return self.api_client.call_api(
            '{container_distribution_href}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AsyncOperationResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def read(self, container_distribution_href, **kwargs):  # noqa: E501
        """Inspect a container distribution  # noqa: E501

        The Container Distribution will serve the latest version of a Repository if ``repository`` is specified. The Container Distribution will serve a specific repository version if ``repository_version``. Note that **either** ``repository`` or ``repository_version`` can be set on a Container Distribution, but not both.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read(container_distribution_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str container_distribution_href: URI of Container Distribution. e.g.: /pulp/api/v3/distributions/container/container/1/ (required)
        :param str fields: A list of fields to include in the response.
        :param str exclude_fields: A list of fields to exclude from the response.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ContainerContainerDistributionRead
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.read_with_http_info(container_distribution_href, **kwargs)  # noqa: E501

    def read_with_http_info(self, container_distribution_href, **kwargs):  # noqa: E501
        """Inspect a container distribution  # noqa: E501

        The Container Distribution will serve the latest version of a Repository if ``repository`` is specified. The Container Distribution will serve a specific repository version if ``repository_version``. Note that **either** ``repository`` or ``repository_version`` can be set on a Container Distribution, but not both.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_with_http_info(container_distribution_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str container_distribution_href: URI of Container Distribution. e.g.: /pulp/api/v3/distributions/container/container/1/ (required)
        :param str fields: A list of fields to include in the response.
        :param str exclude_fields: A list of fields to exclude from the response.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(ContainerContainerDistributionRead, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['container_distribution_href', 'fields', 'exclude_fields']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method read" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'container_distribution_href' is set
        if self.api_client.client_side_validation and ('container_distribution_href' not in local_var_params or  # noqa: E501
                                                        local_var_params['container_distribution_href'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `container_distribution_href` when calling `read`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'container_distribution_href' in local_var_params:
            path_params['container_distribution_href'] = local_var_params['container_distribution_href']  # noqa: E501

        query_params = []
        if 'fields' in local_var_params and local_var_params['fields'] is not None:  # noqa: E501
            query_params.append(('fields', local_var_params['fields']))  # noqa: E501
        if 'exclude_fields' in local_var_params and local_var_params['exclude_fields'] is not None:  # noqa: E501
            query_params.append(('exclude_fields', local_var_params['exclude_fields']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Basic']  # noqa: E501

        return self.api_client.call_api(
            '{container_distribution_href}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ContainerContainerDistributionRead',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update(self, container_distribution_href, data, **kwargs):  # noqa: E501
        """Update a container distribution  # noqa: E501

        Trigger an asynchronous update task  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update(container_distribution_href, data, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str container_distribution_href: URI of Container Distribution. e.g.: /pulp/api/v3/distributions/container/container/1/ (required)
        :param ContainerContainerDistribution data: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AsyncOperationResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.update_with_http_info(container_distribution_href, data, **kwargs)  # noqa: E501

    def update_with_http_info(self, container_distribution_href, data, **kwargs):  # noqa: E501
        """Update a container distribution  # noqa: E501

        Trigger an asynchronous update task  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_with_http_info(container_distribution_href, data, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str container_distribution_href: URI of Container Distribution. e.g.: /pulp/api/v3/distributions/container/container/1/ (required)
        :param ContainerContainerDistribution data: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AsyncOperationResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['container_distribution_href', 'data']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'container_distribution_href' is set
        if self.api_client.client_side_validation and ('container_distribution_href' not in local_var_params or  # noqa: E501
                                                        local_var_params['container_distribution_href'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `container_distribution_href` when calling `update`")  # noqa: E501
        # verify the required parameter 'data' is set
        if self.api_client.client_side_validation and ('data' not in local_var_params or  # noqa: E501
                                                        local_var_params['data'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `data` when calling `update`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'container_distribution_href' in local_var_params:
            path_params['container_distribution_href'] = local_var_params['container_distribution_href']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'data' in local_var_params:
            body_params = local_var_params['data']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Basic']  # noqa: E501

        return self.api_client.call_api(
            '{container_distribution_href}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AsyncOperationResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
