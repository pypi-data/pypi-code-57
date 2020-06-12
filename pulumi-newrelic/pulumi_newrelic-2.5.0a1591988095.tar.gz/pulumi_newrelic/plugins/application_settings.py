# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class ApplicationSettings(pulumi.CustomResource):
    app_apdex_threshold: pulumi.Output[float]
    """
    The appex threshold for the New Relic application.
    """
    enable_real_user_monitoring: pulumi.Output[bool]
    """
    Enable or disable real user monitoring for the New Relic application.
    """
    end_user_apdex_threshold: pulumi.Output[float]
    """
    The user's apdex threshold for the New Relic application.
    """
    name: pulumi.Output[str]
    """
    The name of the application in New Relic APM.
    """
    def __init__(__self__, resource_name, opts=None, app_apdex_threshold=None, enable_real_user_monitoring=None, end_user_apdex_threshold=None, name=None, __props__=None, __name__=None, __opts__=None):
        """
        > **NOTE:** Applications are not created by this resource, but are created by
        a reporting agent.

        Use this resource to manage configuration for an application that already
        exists in New Relic.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_newrelic as newrelic

        app = newrelic.plugins.ApplicationSettings("app",
            app_apdex_threshold="0.7",
            enable_real_user_monitoring=False,
            end_user_apdex_threshold="0.8")
        ```

        ## Notes

        > **NOTE:** Applications that have reported data in the last twelve hours
        cannot be deleted.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] app_apdex_threshold: The appex threshold for the New Relic application.
        :param pulumi.Input[bool] enable_real_user_monitoring: Enable or disable real user monitoring for the New Relic application.
        :param pulumi.Input[float] end_user_apdex_threshold: The user's apdex threshold for the New Relic application.
        :param pulumi.Input[str] name: The name of the application in New Relic APM.
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

            if app_apdex_threshold is None:
                raise TypeError("Missing required property 'app_apdex_threshold'")
            __props__['app_apdex_threshold'] = app_apdex_threshold
            if enable_real_user_monitoring is None:
                raise TypeError("Missing required property 'enable_real_user_monitoring'")
            __props__['enable_real_user_monitoring'] = enable_real_user_monitoring
            if end_user_apdex_threshold is None:
                raise TypeError("Missing required property 'end_user_apdex_threshold'")
            __props__['end_user_apdex_threshold'] = end_user_apdex_threshold
            __props__['name'] = name
        super(ApplicationSettings, __self__).__init__(
            'newrelic:plugins/applicationSettings:ApplicationSettings',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, app_apdex_threshold=None, enable_real_user_monitoring=None, end_user_apdex_threshold=None, name=None):
        """
        Get an existing ApplicationSettings resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] app_apdex_threshold: The appex threshold for the New Relic application.
        :param pulumi.Input[bool] enable_real_user_monitoring: Enable or disable real user monitoring for the New Relic application.
        :param pulumi.Input[float] end_user_apdex_threshold: The user's apdex threshold for the New Relic application.
        :param pulumi.Input[str] name: The name of the application in New Relic APM.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["app_apdex_threshold"] = app_apdex_threshold
        __props__["enable_real_user_monitoring"] = enable_real_user_monitoring
        __props__["end_user_apdex_threshold"] = end_user_apdex_threshold
        __props__["name"] = name
        return ApplicationSettings(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

