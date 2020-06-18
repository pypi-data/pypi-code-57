#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from injector import inject
from requests import ConnectionError

from yams_cli.logic.core.models.access_key import CreateAccessKeyResult
from yams_cli.logic.core.models.bucket import CreateBucketResult
from yams_cli.logic.core.models.domain import CreateDomainResult
from yams_cli.logic.core.models.object import GetObjectResult, ObjectMetadata, PutObjectResult
from yams_cli.logic.core.models.policy import CreatePolicyResult
from yams_cli.logic.core.models.rule import CreateRuleResult
from yams_cli.logic.core.models.watermark import CreateWatermarkResult, GetWatermarkResult
from yams_cli.utils import exception_safe, valid_uuid
from yams_cli.logic.core.http_client import HttpClient
from yams_cli.connection_specs import ConnectionSpecs

log = logging.getLogger('yams-cli.manager')


class Manager(object):
    @inject
    def __init__(self, connection_specs: ConnectionSpecs, http_client: HttpClient):
        log.debug("Connection specs:\n{}".format(connection_specs.dump_connection_specs()))
        self._management_url = connection_specs.get_connection_value('management_url')
        self._fetch_url = connection_specs.get_connection_value('fetch_url')
        self._api_version = connection_specs.get_connection_value('api_version')
        self._http_client = http_client

    @exception_safe(ConnectionError)
    def _mgmt_request(self, method, path, payload=None, data=None, json_content=None, query_params=None, log_request=True):
        if payload is None:
            payload = {}
        if log_request:
            self.log_request(method, path)
        url = "{}/{}{}".format(self._management_url, self._api_version, path)
        response = self._http_client.execute_mgmt_request(method, url, path, payload=payload,
                                                          json_content=json_content, data=data,
                                                          query_params=query_params)

        return response, url

    @exception_safe(ConnectionError)
    def _fetch_request(self, method, path, log_request=True):
        if log_request:
            self.log_request(method, path)
        url = "{}/{}{}".format(self._fetch_url.replace('fetch', 'cdn'), self._api_version, path)
        return url

    def _mgmt_get(self, path, query_params=None, log_request=True):
        response, url = self._mgmt_request("GET", path, query_params=query_params, log_request=log_request)
        result = self._http_client.get_result_from_response(response)
        self._http_client.validate_result(result, url, [200])
        return result["content"]

    def _mgmt_delete(self, path, log_request=True):
        response, url = self._mgmt_request("DELETE", path, log_request=log_request)
        result = self._http_client.get_result_from_response(response)
        self._http_client.validate_result(result, url, [200, 202, 204])
        return result

    # ######################################################
    # TENANTS
    # ######################################################
    def get_tenants(self):
        return self._mgmt_get("/tenants")

    def get_tenant(self, tenant_id):
        path = "/tenants/{}".format(tenant_id)
        return self._mgmt_get(path)

    def delete_tenant(self, tenant_id):
        path = "/tenants/{}".format(tenant_id)
        self._mgmt_delete(path)

    # ######################################################
    # Distributions
    # ######################################################
    def get_distributions(self, tenant_id):
        path = "/tenants/{}/distributions".format(tenant_id)
        return self._mgmt_get(path)

    def get_distribution(self, tenant_id, distribution_id):
        path = "/tenants/{}/distributions/{}".format(tenant_id, distribution_id)
        return self._mgmt_get(path)

    def create_distribution(self, tenant_id, dns_name):
        path = "/tenants/{}/distributions".format(tenant_id)
        distribution_json = {
            'dns_name': dns_name
        }
        response, url = self._mgmt_request("POST", path, json_content=distribution_json)
        result = self._http_client.get_result_from_response(response)

        self._http_client.validate_result(result, url, [202])

        return result["content"]

    def delete_distribution(self, tenant_id, distribution_id):
        path = "/tenants/{}/distributions/{}".format(tenant_id, distribution_id)
        self._mgmt_delete(path)

    # ######################################################
    # DOMAINS
    # ######################################################
    def get_domain(self, tenant_id, domain_id):
        path = "/tenants/{}/domains/{}".format(tenant_id, domain_id)
        return self._mgmt_get(path)

    def get_domains(self, tenant_id):
        path = "/tenants/{}/domains".format(tenant_id)
        return self._mgmt_get(path)

    def create_domain(self, tenant_id, domain_alias, domain_status):
        path = "/tenants/{}/domains".format(tenant_id)
        domain_json = {
            'name': domain_alias,
            'status': domain_status
        }
        response, url = self._mgmt_request("POST", path, json_content=domain_json)
        result = self._http_client.get_result_from_response(response)

        self._http_client.validate_result(result, url, [201])

        return CreateDomainResult(tenant_id=tenant_id, domain_id=result["resource_id"], alias=domain_alias)

    def delete_domain(self, tenant_id, domain_id):
        path = "/tenants/{}/domains/{}".format(tenant_id, domain_id)
        self._mgmt_delete(path)

    # ######################################################
    # RULES
    # ######################################################
    def get_rule(self, tenant_id, domain_id, rule_id):
        path = "/tenants/{}/domains/{}/rules/{}".format(tenant_id, domain_id, rule_id)
        return self._mgmt_get(path)

    def get_rules(self, tenant_id, domain_id):
        path = "/tenants/{}/domains/{}/rules".format(tenant_id, domain_id)
        return self._mgmt_get(path)

    def create_rule(self, tenant_id, domain_id, rule_json=None):
        path = "/tenants/{}/domains/{}/rules".format(tenant_id, domain_id)
        watermark = self.get_watermark_from_rule(rule_json)

        if watermark is not None:
            get_watermark_path = "/tenants/{}/domains/{}/watermarks/{}".format(tenant_id, domain_id, watermark)
            get_watermark_response, url = self._mgmt_request("GET", get_watermark_path)
            if get_watermark_response.status_code == 404:
                log.warn("The watermark: {} does not exists".format(watermark))

        response, url = self._mgmt_request("POST", path, json_content=rule_json)
        result = self._http_client.get_result_from_response(response)
        self._http_client.validate_result(result, url, [201])
        alias = ""
        if "name" in rule_json:
            alias = rule_json["name"]
        create_rule_result = CreateRuleResult(tenant_id=tenant_id, domain_id=domain_id, rule_id=result["resource_id"],
                                              alias=alias)
        return create_rule_result

    def update_rule(self, tenant_id, domain_id, rule_id, rule_json=None):
        path = "/tenants/{}/domains/{}/rules/{}".format(tenant_id, domain_id, rule_id)
        response, url = self._mgmt_request("PUT", path, json_content=rule_json)
        result = self._http_client.get_result_from_response(response)
        self._http_client.validate_result(result, url, [200])

        return result

    def delete_rule(self, tenant_id, domain_id, rule_id):
        path = "/tenants/{}/domains/{}/rules/{}".format(tenant_id, domain_id, rule_id)
        return self._mgmt_delete(path)

    # ######################################################
    # POLICIES
    # ######################################################
    def get_policy(self, tenant_id, policy_id):
        path = "/tenants/{}/policies/{}".format(tenant_id, policy_id)
        return self._mgmt_get(path)

    def get_policies(self, tenant_id):
        path = "/tenants/{}/policies".format(tenant_id)
        return self._mgmt_get(path)

    def create_policy(self, tenant_id, policy_json=None):
        path = "/tenants/{}/policies".format(tenant_id)
        response, url = self._mgmt_request("POST", path, json_content=policy_json)
        result = self._http_client.get_result_from_response(response)
        self._http_client.validate_result(result, url, [201])
        return CreatePolicyResult(tenant_id=tenant_id, policy_id=result["resource_id"])

    def update_policy(self, tenant_id, policy_id, policy_json=None):
        path = "/tenants/{}/policies/{}".format(tenant_id, policy_id, json_content=policy_json)
        response, url = self._mgmt_request("PUT", path, json_content=policy_json)
        result = self._http_client.get_result_from_response(response)
        self._http_client.validate_result(result, url, [200])
        return result

    def delete_policy(self, tenant_id, policy_id):
        path = "/tenants/{}/policies/{}".format(tenant_id, policy_id)
        self._mgmt_delete(path)

    # ######################################################
    # ACCESS-KEYS
    # ######################################################
    def get_access_keys(self, tenant_id):
        path = "/tenants/{}/access-keys".format(tenant_id)
        return self._mgmt_get(path)

    def get_access_key(self, tenant_id, accesskey_id):
        path = "/tenants/{}/access-keys/{}".format(tenant_id, accesskey_id)
        return self._mgmt_get(path)

    def create_access_key(self, tenant_id, description):
        path = "/tenants/{}/access-keys".format(tenant_id)
        accesskey_json = {}
        if description is not None:
            accesskey_json['description'] = description
        response, url = self._mgmt_request("POST", path, json_content=accesskey_json)
        result = self._http_client.get_result_from_response(response)
        self._http_client.validate_result(result, url, [201])
        return CreateAccessKeyResult(tenant_id=tenant_id, access_key_id=result["content"]["access_id"], private_key=result["content"]["private_key"])

    def provide_access_key(self, tenant_id, public_key, description):
        path = "/tenants/{}/access-keys".format(tenant_id)
        accesskey_json = {'public_key': public_key}
        if description is not None:
            accesskey_json['description'] = description
        response, url = self._mgmt_request("PUT", path, json_content=accesskey_json)
        result = self._http_client.get_result_from_response(response)
        self._http_client.validate_result(result, url, [201])
        return CreateAccessKeyResult(tenant_id=tenant_id, access_key_id="", private_key=None)

    def update_access_key(self, tenant_id, accesskey_id, active, description):
        path = "/tenants/{}/access-keys/{}".format(tenant_id, accesskey_id)
        accesskey_json = {}
        if active is not None:
            accesskey_json['active'] = active
        if description is not None:
            accesskey_json['description'] = description
        response, url = self._mgmt_request("PUT", path, json_content=accesskey_json)
        result = self._http_client.get_result_from_response(response)
        self._http_client.validate_result(result, url, [200])
        return result

    def delete_access_key(self, tenant_id, accesskey_id):
        path = "/tenants/{}/access-keys/{}".format(tenant_id, accesskey_id)
        return self._mgmt_delete(path)

    # ######################################################
    # ATTACHED-POLICIES
    # ######################################################
    def get_attached_policies(self, tenant_id, accesskey_id):
        path = "/tenants/{}/access-keys/{}/policies".format(tenant_id, accesskey_id)
        return self._mgmt_get(path)

    def attach_policy(self, tenant_id, accesskey_id, policy_id):
        path = "/tenants/{}/access-keys/{}/policies".format(tenant_id, accesskey_id)
        if valid_uuid(policy_id):
            attach_json = {'policy_id': policy_id}
        else:
            attach_json = {'policy_alias': policy_id}
        response, url = self._mgmt_request("POST", path, json_content=attach_json)
        result = self._http_client.get_result_from_response(response)
        self._http_client.validate_result(result, url, [201])
        return result

    def detach_policy(self, tenant_id, accesskey_id, policy_id):
        path = "/tenants/{}/access-keys/{}/policies/{}".format(tenant_id, accesskey_id, policy_id)
        return self._mgmt_delete(path)

    # ######################################################
    # WATERMARKS
    # ######################################################
    def get_watermark(self, tenant_id, domain_id, watermark_id):
        path = "/tenants/{}/domains/{}/watermarks/{}".format(tenant_id, domain_id, watermark_id)
        watermark = self._mgmt_get(path)
        return GetWatermarkResult(watermark)

    def list_watermarks(self, tenant_id, domain_id):
        path = "/tenants/{}/domains/{}/watermarks".format(tenant_id, domain_id)
        response, url = self._mgmt_request("GET", path)
        result = self._http_client.get_result_from_response(response)
        self._http_client.validate_result(result, url, [200])
        return result

    def create_watermark(self, tenant_id, domain_id, alias, watermark_data):
        path = "/tenants/{}/domains/{}/watermarks".format(tenant_id, domain_id)
        metadata = {}
        if alias is not None:
            metadata["alias"] = alias
        response, url = self._mgmt_request("POST", path, payload=metadata, data=watermark_data)
        result = self._http_client.get_result_from_response(response)

        self._http_client.validate_result(result, url, [201])

        return CreateWatermarkResult(tenant_id=tenant_id, domain_id=domain_id, watermark_id=result["resource_id"],
                                     alias=alias)

    def update_watermark(self, tenant_id, domain_id, watermark_id, alias):
        path = "/tenants/{}/domains/{}/watermarks/{}".format(tenant_id, domain_id, watermark_id)
        watermark_json = {}
        if alias is not None:
            watermark_json['alias'] = alias

        response, url = self._mgmt_request("PUT", path, json_content=watermark_json)
        result = self._http_client.get_result_from_response(response)
        self._http_client.validate_result(result, url, [200])
        return result

    def delete_watermark(self, tenant_id, domain_id, watermark_id):
        path = "/tenants/{}/domains/{}/watermarks/{}".format(tenant_id, domain_id, watermark_id)
        return self._mgmt_delete(path)

    # ######################################################
    # METRICS
    # ######################################################
    def get_bucket_metric_names(self, tenant_id, domain_id, bucket_id):
        path = "/tenants/{}/domains/{}/buckets/{}/metrics".format(tenant_id, domain_id, bucket_id)
        return self._mgmt_get(path)

    def get_bucket_metric(self, tenant_id, domain_id, bucket_id, metric_name, year_month):
        path = "/tenants/{}/domains/{}/buckets/{}/metrics/{}".format(
            tenant_id, domain_id, bucket_id, metric_name)
        return self._mgmt_get(path, query_params={'when': year_month})

    # ######################################################
    # BUCKETS
    # ######################################################
    def get_bucket(self, tenant_id, domain_id, bucket_id):
        path = "/tenants/{}/domains/{}/buckets/{}".format(tenant_id, domain_id, bucket_id)
        return self._mgmt_get(path)

    def get_buckets(self, tenant_id, domain_id):
        path = "/tenants/{}/domains/{}/buckets".format(tenant_id, domain_id)
        return self._mgmt_get(path)

    def create_bucket(self, tenant_id, domain_id, bucket_name, bucket_region, bucket_statics, bucket_cache_max_age):
        path = "/tenants/{}/domains/{}/buckets".format(tenant_id, domain_id)

        bucket_json = {
            'name': bucket_name,
            'region': bucket_region,
            'statics': bucket_statics,
            'cache': {
                'max_age': int(bucket_cache_max_age)
            }
        }

        response, url = self._mgmt_request("POST", path, json_content=bucket_json)
        result = self._http_client.get_result_from_response(response)

        self._http_client.validate_result(result, url, [201])

        return CreateBucketResult(tenant_id=tenant_id, domain_id=domain_id, bucket_id=result["resource_id"],
                                  alias=bucket_name)

    def update_bucket(self, tenant_id, domain_id, bucket_id, bucket_name, bucket_statics, bucket_cache_max_age):
        path = "/tenants/{}/domains/{}/buckets/{}".format(tenant_id, domain_id, bucket_id)

        bucket_json = {}
        if bucket_name:
            bucket_json['name'] = bucket_name
        if bucket_statics is not None:
            bucket_json['statics'] = bucket_statics
        if bucket_cache_max_age:
            bucket_json['cache'] = {'max_age': int(bucket_cache_max_age)}

        response, url = self._mgmt_request("PUT", path, json_content=bucket_json)
        result = self._http_client.get_result_from_response(response)
        self._http_client.validate_result(result, url, [200])
        return result

    def delete_bucket(self, tenant_id, domain_id, bucket_id):
        path = "/tenants/{}/domains/{}/buckets/{}".format(tenant_id, domain_id, bucket_id)
        return self._mgmt_delete(path)

    # ######################################################
    # OBJECTS
    # ######################################################
    def list_objects(self, tenant_id, domain_id, bucket_id, options, token):
        path = "/tenants/{}/domains/{}/buckets/{}/objects".format(tenant_id, domain_id, bucket_id)

        query_params = {}
        if options.get('prefix'):
            query_params['prefix'] = options.get('prefix')
        if options.get('max_keys'):
            query_params['max-keys'] = options.get('max_keys')
        if options.get('show-recoverable'):
            query_params['show-recoverable'] = options.get('show-recoverable')
        if options.get('list-backup'):
            query_params['list-backup'] = options.get('list-backup')
        if token:
            query_params['continuation-token'] = token

        return self._mgmt_get(path, query_params=query_params, log_request=False)

    def head_object(self, tenant_id, domain_id, bucket_id, object_id):
        path = "/tenants/{}/domains/{}/buckets/{}/objects/{}".format(tenant_id, domain_id, bucket_id, object_id)
        response, url = self._mgmt_request("HEAD", path)

        result = self._http_client.get_result_from_response(response, True)
        self._http_client.validate_result(result, url, [200])

        return self._get_metadata_from_response(response)

    @staticmethod
    def _get_metadata_from_response(response):
        md5 = response.headers.get("content-md5", "")
        content_type = response.headers.get("content-type", "unknown")
        content_length = response.headers.get("content-length", "")
        last_modified = response.headers.get("last-modified", "")
        etag = response.headers.get("ETag", "")

        return ObjectMetadata(md5, content_type, content_length, etag, last_modified)

    def get_object(self, tenant_id, domain_id, bucket_id, object_id):
        path = "/tenants/{}/domains/{}/buckets/{}/objects/{}".format(tenant_id, domain_id, bucket_id, object_id)
        response, url = self._mgmt_request("GET", path)

        result = self._http_client.get_result_from_response(response, True)
        self._http_client.validate_result(result, url, [200])
        return GetObjectResult(content=result["content"], metadata=self._get_metadata_from_response(response))

    def put_object(self, tenant_id, domain_id, bucket_id, object_name, object_data, expiration):
        path = "/tenants/{}/domains/{}/buckets/{}/objects".format(tenant_id, domain_id, bucket_id)
        metadata = {}
        if object_name is not None:
            metadata["oid"] = object_name

        if expiration is not None:
            metadata["x-object-expiration"] = int(expiration)

        response, url = self._mgmt_request("POST", path, payload=metadata, data=object_data)
        result = self._http_client.get_result_from_response(response, is_object=True)

        self._http_client.validate_result(result, url, [201])

        return PutObjectResult(tenant_id=tenant_id, domain_id=domain_id, bucket_id=bucket_id,
                               object_id=result["resource_id"])

    def delete_object(self, tenant_id, domain_id, bucket_id, object_id, force):
        path = "/tenants/{}/domains/{}/buckets/{}/objects/{}".format(tenant_id, domain_id, bucket_id, object_id)
        metadata = {
            'oid': object_id,
            'force': force
        }

        response, url = self._mgmt_request("DELETE", path, payload=metadata)
        result = self._http_client.get_result_from_response(response)

        self._http_client.validate_result(result, url, [202])

    def delete_delete_marker(self, tenant_id, domain_id, bucket_id, object_id):
        path = "/tenants/{}/domains/{}/buckets/{}/delete-markers/{}".format(tenant_id, domain_id, bucket_id, object_id)
        return self._mgmt_delete(path)

    # ######################################################
    # OBJECT METADATA
    # ######################################################
    def get_object_metadata(self, tenant_id, domain_id, bucket_id, object_id):
        path = "/tenants/{}/domains/{}/buckets/{}/metadata/{}".format(tenant_id, domain_id, bucket_id, object_id)
        return self._mgmt_get(path)

    def update_object_metadata(self, tenant_id, domain_id, bucket_id, object_id, expiration):
        path = "/tenants/{}/domains/{}/buckets/{}/metadata/{}".format(tenant_id, domain_id, bucket_id, object_id)
        content = {}

        if expiration is not None:
            content["x-object-expiration"] = int(expiration)

        response, url = self._mgmt_request("PUT", path, payload={}, json_content=content)
        result = self._http_client.get_result_from_response(response)
        self._http_client.validate_result(result, url, [204])
        return result
    # ######################################################
    # PROCESSING
    # ######################################################
    def processing_start(self, tenant_id, domain_id, bucket_id, object_id, models):
        path = "/tenants/{}/domains/{}/buckets/{}/start-processing/{}".format(
            tenant_id, domain_id, bucket_id, object_id)
        response, url = self._mgmt_request("PUT", path, json_content={"models": models})
        result = self._http_client.get_result_from_response(response)
        self._http_client.validate_result(result, url, [202])
        return "Processing started"

    # ######################################################
    # IMAGES
    # ######################################################
    def fetch_object(self, tenant_id, domain_id, bucket_id, object_id, rule_id):
        path = "/tenants/{}/domains/{}/buckets/{}/images/{}".format(tenant_id, domain_id, bucket_id, object_id)
        url = self._fetch_request("GET", path)
        print("URL: {}?rule={}".format(url, rule_id))
        return True

    def fetch_object_with_rule(self, tenant_id, domain_id, bucket_id, object_id, rule_json):
        path = "/tenants/{}/domains/{}/buckets/{}/images/{}".format(tenant_id, domain_id, bucket_id, object_id)
        url = self._fetch_request("GET (with rule)", path)
        params = self._http_client.get_fetch_auth_params(origin_method="GET", origin_path=path,
                                                         metadata={'rule': rule_json})
        print("URL: {}?AccessKeyId={}&jwt={}".format(url, params["AccessKeyId"], params["jwt"]))
        return True

    def fetch_static_object(self, tenant_id, domain_id, bucket_id, object_id):
        path = "/tenants/{}/domains/{}/buckets/{}/statics/{}".format(tenant_id, domain_id, bucket_id, object_id)
        url = self._fetch_request("GET (statics)", path)
        params = self._http_client.get_fetch_auth_params(origin_method="GET", origin_path=path, metadata={})
        print("URL: {}?AccessKeyId={}&jwt={}".format(url, params["AccessKeyId"], params["jwt"]))
        return True

    # ######################################################
    # DOCUMENTS
    # ######################################################
    def fetch_document(self, tenant_id, domain_id, bucket_id, object_id, rule_id):
        path = "/tenants/{}/domains/{}/buckets/{}/documents/{}".format(tenant_id, domain_id, bucket_id, object_id)
        url = self._fetch_request("GET", path)
        print("URL: {}?rule={}".format(url, rule_id))
        return True

    def fetch_document_with_rule(self, tenant_id, domain_id, bucket_id, object_id, rule_json):
        path = "/tenants/{}/domains/{}/buckets/{}/documents/{}".format(tenant_id, domain_id, bucket_id, object_id)
        url = self._fetch_request("GET (with rule)", path)
        params = self._http_client.get_fetch_auth_params(origin_method="GET", origin_path=path,
                                                         metadata={'rule': rule_json})
        print("URL: {}?AccessKeyId={}&jwt={}".format(url, params["AccessKeyId"], params["jwt"]))
        return True

    @staticmethod
    def get_watermark_from_rule(rule_json):
        if rule_json is not None and "watermark" in rule_json and "id" in rule_json["watermark"]:
            return rule_json["watermark"]["id"]
        return None

    @classmethod
    def log_request(cls, method, path):
        logging.info("{method} {path}".format(method=method, path=path))
