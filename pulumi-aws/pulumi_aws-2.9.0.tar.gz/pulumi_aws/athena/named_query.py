# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class NamedQuery(pulumi.CustomResource):
    database: pulumi.Output[str]
    """
    The database to which the query belongs.
    """
    description: pulumi.Output[str]
    """
    A brief explanation of the query. Maximum length of 1024.
    """
    name: pulumi.Output[str]
    """
    The plain language name for the query. Maximum length of 128.
    """
    query: pulumi.Output[str]
    """
    The text of the query itself. In other words, all query statements. Maximum length of 262144.
    """
    workgroup: pulumi.Output[str]
    """
    The workgroup to which the query belongs. Defaults to `primary`
    """
    def __init__(__self__, resource_name, opts=None, database=None, description=None, name=None, query=None, workgroup=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an Athena Named Query resource.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws

        hoge_bucket = aws.s3.Bucket("hogeBucket")
        test_key = aws.kms.Key("testKey",
            deletion_window_in_days=7,
            description="Athena KMS Key")
        test_workgroup = aws.athena.Workgroup("testWorkgroup", configuration={
            "resultConfiguration": {
                "encryption_configuration": {
                    "encryptionOption": "SSE_KMS",
                    "kms_key_arn": test_key.arn,
                },
            },
        })
        hoge_database = aws.athena.Database("hogeDatabase",
            bucket=hoge_bucket.id,
            name="users")
        foo = aws.athena.NamedQuery("foo",
            database=hoge_database.name,
            query=hoge_database.name.apply(lambda name: f"SELECT * FROM {name} limit 10;"),
            workgroup=test_workgroup.id)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database: The database to which the query belongs.
        :param pulumi.Input[str] description: A brief explanation of the query. Maximum length of 1024.
        :param pulumi.Input[str] name: The plain language name for the query. Maximum length of 128.
        :param pulumi.Input[str] query: The text of the query itself. In other words, all query statements. Maximum length of 262144.
        :param pulumi.Input[str] workgroup: The workgroup to which the query belongs. Defaults to `primary`
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            if database is None:
                raise TypeError("Missing required property 'database'")
            __props__['database'] = database
            __props__['description'] = description
            __props__['name'] = name
            if query is None:
                raise TypeError("Missing required property 'query'")
            __props__['query'] = query
            __props__['workgroup'] = workgroup
        super(NamedQuery, __self__).__init__(
            'aws:athena/namedQuery:NamedQuery',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, database=None, description=None, name=None, query=None, workgroup=None):
        """
        Get an existing NamedQuery resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database: The database to which the query belongs.
        :param pulumi.Input[str] description: A brief explanation of the query. Maximum length of 1024.
        :param pulumi.Input[str] name: The plain language name for the query. Maximum length of 128.
        :param pulumi.Input[str] query: The text of the query itself. In other words, all query statements. Maximum length of 262144.
        :param pulumi.Input[str] workgroup: The workgroup to which the query belongs. Defaults to `primary`
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["database"] = database
        __props__["description"] = description
        __props__["name"] = name
        __props__["query"] = query
        __props__["workgroup"] = workgroup
        return NamedQuery(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

