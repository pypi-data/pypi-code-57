# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class GetBillingServiceAccountResult:
    """
    A collection of values returned by getBillingServiceAccount.
    """
    def __init__(__self__, arn=None, id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        __self__.arn = arn
        """
        The ARN of the AWS billing service account.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
class AwaitableGetBillingServiceAccountResult(GetBillingServiceAccountResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBillingServiceAccountResult(
            arn=self.arn,
            id=self.id)

def get_billing_service_account(opts=None):
    """
    Use this data source to get the Account ID of the [AWS Billing and Cost Management Service Account](http://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-getting-started.html#step-2) for the purpose of whitelisting in S3 bucket policy.

    ## Example Usage



    ```python
    import pulumi
    import pulumi_aws as aws

    main = aws.get_billing_service_account()
    billing_logs = aws.s3.Bucket("billingLogs",
        acl="private",
        policy=f\"\"\"{{
      "Id": "Policy",
      "Version": "2012-10-17",
      "Statement": [
        {{
          "Action": [
            "s3:GetBucketAcl", "s3:GetBucketPolicy"
          ],
          "Effect": "Allow",
          "Resource": "arn:aws:s3:::my-billing-tf-test-bucket",
          "Principal": {{
            "AWS": [
              "{main.arn}"
            ]
          }}
        }},
        {{
          "Action": [
            "s3:PutObject"
          ],
          "Effect": "Allow",
          "Resource": "arn:aws:s3:::my-billing-tf-test-bucket/*",
          "Principal": {{
            "AWS": [
              "{main.arn}"
            ]
          }}
        }}
      ]
    }}

    \"\"\")
    ```
    """
    __args__ = dict()


    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:index/getBillingServiceAccount:getBillingServiceAccount', __args__, opts=opts).value

    return AwaitableGetBillingServiceAccountResult(
        arn=__ret__.get('arn'),
        id=__ret__.get('id'))
