# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class Database(pulumi.CustomResource):
    default_character_set: pulumi.Output[str]
    """
    The default character set to use when
    a table is created without specifying an explicit character set. Defaults
    to "utf8".
    """
    default_collation: pulumi.Output[str]
    """
    The default collation to use when a table
    is created without specifying an explicit collation. Defaults to
    ``utf8_general_ci``. Each character set has its own set of collations, so
    changing the character set requires also changing the collation.
    """
    name: pulumi.Output[str]
    """
    The name of the database. This must be unique within
    a given MySQL server and may or may not be case-sensitive depending on
    the operating system on which the MySQL server is running.
    """
    def __init__(__self__, resource_name, opts=None, default_character_set=None, default_collation=None, name=None, __props__=None, __name__=None, __opts__=None):
        """
        The ``.Database`` resource creates and manages a database on a MySQL
        server.

        > **Caution:** The ``.Database`` resource can completely delete your
        database just as easily as it can create it. To avoid costly accidents,
        consider setting
        [``prevent_destroy``](https://www.terraform.io/docs/configuration/resources.html#prevent_destroy)
        on your database resources as an extra safety measure.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_mysql as mysql

        app = mysql.Database("app")
        ```


        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] default_character_set: The default character set to use when
               a table is created without specifying an explicit character set. Defaults
               to "utf8".
        :param pulumi.Input[str] default_collation: The default collation to use when a table
               is created without specifying an explicit collation. Defaults to
               ``utf8_general_ci``. Each character set has its own set of collations, so
               changing the character set requires also changing the collation.
        :param pulumi.Input[str] name: The name of the database. This must be unique within
               a given MySQL server and may or may not be case-sensitive depending on
               the operating system on which the MySQL server is running.
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

            __props__['default_character_set'] = default_character_set
            __props__['default_collation'] = default_collation
            __props__['name'] = name
        super(Database, __self__).__init__(
            'mysql:index/database:Database',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, default_character_set=None, default_collation=None, name=None):
        """
        Get an existing Database resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] default_character_set: The default character set to use when
               a table is created without specifying an explicit character set. Defaults
               to "utf8".
        :param pulumi.Input[str] default_collation: The default collation to use when a table
               is created without specifying an explicit collation. Defaults to
               ``utf8_general_ci``. Each character set has its own set of collations, so
               changing the character set requires also changing the collation.
        :param pulumi.Input[str] name: The name of the database. This must be unique within
               a given MySQL server and may or may not be case-sensitive depending on
               the operating system on which the MySQL server is running.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["default_character_set"] = default_character_set
        __props__["default_collation"] = default_collation
        __props__["name"] = name
        return Database(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

