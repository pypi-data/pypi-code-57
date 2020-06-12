# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class ReportDefinition(pulumi.CustomResource):
    additional_artifacts: pulumi.Output[list]
    """
    A list of additional artifacts. Valid values are: REDSHIFT, QUICKSIGHT.
    """
    additional_schema_elements: pulumi.Output[list]
    """
    A list of schema elements. Valid values are: RESOURCES.
    """
    compression: pulumi.Output[str]
    """
    Compression format for report. Valid values are: GZIP, ZIP.
    """
    format: pulumi.Output[str]
    """
    Format for report. Valid values are: textORcsv.
    """
    report_name: pulumi.Output[str]
    """
    Unique name for the report. Must start with a number/letter and is case sensitive. Limited to 256 characters.
    """
    s3_bucket: pulumi.Output[str]
    """
    Name of the existing S3 bucket to hold generated reports.
    """
    s3_prefix: pulumi.Output[str]
    """
    Report path prefix. Limited to 256 characters.
    """
    s3_region: pulumi.Output[str]
    """
    Region of the existing S3 bucket to hold generated reports.
    """
    time_unit: pulumi.Output[str]
    """
    The frequency on which report data are measured and displayed.  Valid values are: HOURLY, DAILY.
    """
    def __init__(__self__, resource_name, opts=None, additional_artifacts=None, additional_schema_elements=None, compression=None, format=None, report_name=None, s3_bucket=None, s3_prefix=None, s3_region=None, time_unit=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages Cost and Usage Report Definitions.

        > *NOTE:* The AWS Cost and Usage Report service is only available in `us-east-1` currently.

        > *NOTE:* If AWS Organizations is enabled, only the master account can use this resource.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_aws as aws

        example_cur_report_definition = aws.cur.ReportDefinition("exampleCurReportDefinition",
            additional_artifacts=[
                "REDSHIFT",
                "QUICKSIGHT",
            ],
            additional_schema_elements=["RESOURCES"],
            compression="GZIP",
            format="textORcsv",
            report_name="example-cur-report-definition",
            s3_bucket="example-bucket-name",
            s3_region="us-east-1",
            time_unit="HOURLY")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] additional_artifacts: A list of additional artifacts. Valid values are: REDSHIFT, QUICKSIGHT.
        :param pulumi.Input[list] additional_schema_elements: A list of schema elements. Valid values are: RESOURCES.
        :param pulumi.Input[str] compression: Compression format for report. Valid values are: GZIP, ZIP.
        :param pulumi.Input[str] format: Format for report. Valid values are: textORcsv.
        :param pulumi.Input[str] report_name: Unique name for the report. Must start with a number/letter and is case sensitive. Limited to 256 characters.
        :param pulumi.Input[str] s3_bucket: Name of the existing S3 bucket to hold generated reports.
        :param pulumi.Input[str] s3_prefix: Report path prefix. Limited to 256 characters.
        :param pulumi.Input[str] s3_region: Region of the existing S3 bucket to hold generated reports.
        :param pulumi.Input[str] time_unit: The frequency on which report data are measured and displayed.  Valid values are: HOURLY, DAILY.
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

            __props__['additional_artifacts'] = additional_artifacts
            if additional_schema_elements is None:
                raise TypeError("Missing required property 'additional_schema_elements'")
            __props__['additional_schema_elements'] = additional_schema_elements
            if compression is None:
                raise TypeError("Missing required property 'compression'")
            __props__['compression'] = compression
            if format is None:
                raise TypeError("Missing required property 'format'")
            __props__['format'] = format
            if report_name is None:
                raise TypeError("Missing required property 'report_name'")
            __props__['report_name'] = report_name
            if s3_bucket is None:
                raise TypeError("Missing required property 's3_bucket'")
            __props__['s3_bucket'] = s3_bucket
            __props__['s3_prefix'] = s3_prefix
            if s3_region is None:
                raise TypeError("Missing required property 's3_region'")
            __props__['s3_region'] = s3_region
            if time_unit is None:
                raise TypeError("Missing required property 'time_unit'")
            __props__['time_unit'] = time_unit
        super(ReportDefinition, __self__).__init__(
            'aws:cur/reportDefinition:ReportDefinition',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, additional_artifacts=None, additional_schema_elements=None, compression=None, format=None, report_name=None, s3_bucket=None, s3_prefix=None, s3_region=None, time_unit=None):
        """
        Get an existing ReportDefinition resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] additional_artifacts: A list of additional artifacts. Valid values are: REDSHIFT, QUICKSIGHT.
        :param pulumi.Input[list] additional_schema_elements: A list of schema elements. Valid values are: RESOURCES.
        :param pulumi.Input[str] compression: Compression format for report. Valid values are: GZIP, ZIP.
        :param pulumi.Input[str] format: Format for report. Valid values are: textORcsv.
        :param pulumi.Input[str] report_name: Unique name for the report. Must start with a number/letter and is case sensitive. Limited to 256 characters.
        :param pulumi.Input[str] s3_bucket: Name of the existing S3 bucket to hold generated reports.
        :param pulumi.Input[str] s3_prefix: Report path prefix. Limited to 256 characters.
        :param pulumi.Input[str] s3_region: Region of the existing S3 bucket to hold generated reports.
        :param pulumi.Input[str] time_unit: The frequency on which report data are measured and displayed.  Valid values are: HOURLY, DAILY.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["additional_artifacts"] = additional_artifacts
        __props__["additional_schema_elements"] = additional_schema_elements
        __props__["compression"] = compression
        __props__["format"] = format
        __props__["report_name"] = report_name
        __props__["s3_bucket"] = s3_bucket
        __props__["s3_prefix"] = s3_prefix
        __props__["s3_region"] = s3_region
        __props__["time_unit"] = time_unit
        return ReportDefinition(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

