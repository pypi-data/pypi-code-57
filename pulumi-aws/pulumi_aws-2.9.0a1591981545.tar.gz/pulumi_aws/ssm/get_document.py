# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetDocumentResult:
    """
    A collection of values returned by getDocument.
    """
    def __init__(__self__, arn=None, content=None, document_format=None, document_type=None, document_version=None, id=None, name=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        __self__.arn = arn
        """
        The ARN of the document.
        """
        if content and not isinstance(content, str):
            raise TypeError("Expected argument 'content' to be a str")
        __self__.content = content
        """
        The contents of the document.
        """
        if document_format and not isinstance(document_format, str):
            raise TypeError("Expected argument 'document_format' to be a str")
        __self__.document_format = document_format
        if document_type and not isinstance(document_type, str):
            raise TypeError("Expected argument 'document_type' to be a str")
        __self__.document_type = document_type
        """
        The type of the document.
        """
        if document_version and not isinstance(document_version, str):
            raise TypeError("Expected argument 'document_version' to be a str")
        __self__.document_version = document_version
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
class AwaitableGetDocumentResult(GetDocumentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDocumentResult(
            arn=self.arn,
            content=self.content,
            document_format=self.document_format,
            document_type=self.document_type,
            document_version=self.document_version,
            id=self.id,
            name=self.name)

def get_document(document_format=None,document_version=None,name=None,opts=None):
    """
    Gets the contents of the specified Systems Manager document.

    ## Example Usage



    ```python
    import pulumi
    import pulumi_aws as aws

    foo = aws.ssm.get_document(document_format="YAML",
        name="AWS-GatherSoftwareInventory")
    pulumi.export("content", foo.content)
    ```


    :param str document_format: Returns the document in the specified format. The document format can be either JSON or YAML. JSON is the default format.
    :param str document_version: The document version for which you want information.
    :param str name: The name of the Systems Manager document.
    """
    __args__ = dict()


    __args__['documentFormat'] = document_format
    __args__['documentVersion'] = document_version
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:ssm/getDocument:getDocument', __args__, opts=opts).value

    return AwaitableGetDocumentResult(
        arn=__ret__.get('arn'),
        content=__ret__.get('content'),
        document_format=__ret__.get('documentFormat'),
        document_type=__ret__.get('documentType'),
        document_version=__ret__.get('documentVersion'),
        id=__ret__.get('id'),
        name=__ret__.get('name'))
