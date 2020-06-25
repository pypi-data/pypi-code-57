"""
# core module

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **Reference Documentation**:| <span style="font-weight: normal">https://docs.aws.amazon.com/solutions/latest/constructs/</span>|
|:-------------|:-------------|

<div style="height:8px"></div>

The core library includes the basic building blocks of the AWS Solutions Constructs Library. It defines the core classes that are used in the rest of the AWS Solutions Constructs Library.

## Default Properties for AWS CDK Constructs

Core library sets the default properties for the AWS CDK Constructs used by the AWS Solutions Constructs Library constructs.

For example, the following is the snippet of default properties for S3 Bucket construct created by AWS Solutions Constructs. By default, it will turn on the server-side encryption, bucket versioning, block all public access and setup the S3 access logging.

```
{
  encryption: s3.BucketEncryption.S3_MANAGED,
  versioned: true,
  blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
  removalPolicy: RemovalPolicy.RETAIN,
  serverAccessLogsBucket: loggingBucket
}
```

## Override the default properties

The default properties set by the Core library can be overridden by user provided properties. For example, the user can override the Amazon S3 Block Public Access property to meet specific requirements.

```
  const stack = new cdk.Stack();

  const props: CloudFrontToS3Props = {
    deployBucket: true,
    bucketProps: {
      blockPublicAccess: {
        blockPublicAcls: false,
        blockPublicPolicy: true,
        ignorePublicAcls: false,
        restrictPublicBuckets: true
      }
    }
  };

  new CloudFrontToS3(stack, 'test-cloudfront-s3', props);

  expect(stack).toHaveResource("AWS::S3::Bucket", {
    PublicAccessBlockConfiguration: {
      BlockPublicAcls: false,
      BlockPublicPolicy: true,
      IgnorePublicAcls: false,
      RestrictPublicBuckets: true
    },
  });
```

## Property override warnings

When a default property from the Core library is overridden by a user-provided property, Constructs will emit one or more warning messages to the console highlighting the change(s). These messages are intended to provide situational awareness to the user and prevent unintentional overrides that could create security risks. These messages will appear whenever deployment/build-related commands are executed, including `cdk deploy`, `cdk synth`, `npm test`, etc.

Example message:
`AWS_CONSTRUCTS_WARNING: An override has been provided for the property: BillingMode. Default value: 'PAY_PER_REQUEST'. You provided: 'PROVISIONED'.`

#### Toggling override warnings

Override warning messages are enabled by default, but can be explicitly turned on/off using the `overrideWarningsEnabled` shell variable.

* To explicitly <u>turn off</u> override warnings, run `export overrideWarningsEnabled=false`.
* To explicitly <u>turn on</u> override warnings, run `export overrideWarningsEnabled=true`.
* To revert to the default, run `unset overrideWarningsEnabled`.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.aws_cognito
import aws_cdk.aws_dynamodb
import aws_cdk.aws_kinesisfirehose
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.aws_sqs


@jsii.data_type(jsii_type="@aws-solutions-constructs/core.BuildDeadLetterQueueProps", jsii_struct_bases=[], name_mapping={'dead_letter_queue': 'deadLetterQueue', 'max_receive_count': 'maxReceiveCount'})
class BuildDeadLetterQueueProps():
    def __init__(self, *, dead_letter_queue: aws_cdk.aws_sqs.Queue, max_receive_count: typing.Optional[jsii.Number]=None) -> None:
        """
        :param dead_letter_queue: An existing queue that has already been defined to be used as the dead letter queue. Default: - Default props are used.
        :param max_receive_count: The number of times a message can be unsuccessfully dequeued before being moved to the dead-letter queue. Default: - Default props are used
        """
        self._values = {
            'dead_letter_queue': dead_letter_queue,
        }
        if max_receive_count is not None: self._values["max_receive_count"] = max_receive_count

    @builtins.property
    def dead_letter_queue(self) -> aws_cdk.aws_sqs.Queue:
        """An existing queue that has already been defined to be used as the dead letter queue.

        default
        :default: - Default props are used.
        """
        return self._values.get('dead_letter_queue')

    @builtins.property
    def max_receive_count(self) -> typing.Optional[jsii.Number]:
        """The number of times a message can be unsuccessfully dequeued before being moved to the dead-letter queue.

        default
        :default: - Default props are used
        """
        return self._values.get('max_receive_count')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BuildDeadLetterQueueProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-solutions-constructs/core.BuildDynamoDBTableProps", jsii_struct_bases=[], name_mapping={'dynamo_table_props': 'dynamoTableProps', 'existing_table_obj': 'existingTableObj'})
class BuildDynamoDBTableProps():
    def __init__(self, *, dynamo_table_props: typing.Optional[aws_cdk.aws_dynamodb.TableProps]=None, existing_table_obj: typing.Optional[aws_cdk.aws_dynamodb.Table]=None) -> None:
        """
        :param dynamo_table_props: Optional user provided props to override the default props. Default: - Default props are used
        :param existing_table_obj: Existing instance of dynamodb table object. If this is set then the dynamoTableProps is ignored Default: - None
        """
        if isinstance(dynamo_table_props, dict): dynamo_table_props = aws_cdk.aws_dynamodb.TableProps(**dynamo_table_props)
        self._values = {
        }
        if dynamo_table_props is not None: self._values["dynamo_table_props"] = dynamo_table_props
        if existing_table_obj is not None: self._values["existing_table_obj"] = existing_table_obj

    @builtins.property
    def dynamo_table_props(self) -> typing.Optional[aws_cdk.aws_dynamodb.TableProps]:
        """Optional user provided props to override the default props.

        default
        :default: - Default props are used
        """
        return self._values.get('dynamo_table_props')

    @builtins.property
    def existing_table_obj(self) -> typing.Optional[aws_cdk.aws_dynamodb.Table]:
        """Existing instance of dynamodb table object.

        If this is set then the dynamoTableProps is ignored

        default
        :default: - None
        """
        return self._values.get('existing_table_obj')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BuildDynamoDBTableProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-solutions-constructs/core.BuildEncryptionKeyProps", jsii_struct_bases=[], name_mapping={'encryption_key_props': 'encryptionKeyProps'})
class BuildEncryptionKeyProps():
    def __init__(self, *, encryption_key_props: typing.Any=None) -> None:
        """
        :param encryption_key_props: Optional user-provided props to override the default props for the encryption key. Default: - Default props are used.
        """
        self._values = {
        }
        if encryption_key_props is not None: self._values["encryption_key_props"] = encryption_key_props

    @builtins.property
    def encryption_key_props(self) -> typing.Any:
        """Optional user-provided props to override the default props for the encryption key.

        default
        :default: - Default props are used.
        """
        return self._values.get('encryption_key_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BuildEncryptionKeyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-solutions-constructs/core.BuildKinesisAnalyticsAppProps", jsii_struct_bases=[], name_mapping={'kinesis_firehose': 'kinesisFirehose', 'kinesis_analytics_props': 'kinesisAnalyticsProps'})
class BuildKinesisAnalyticsAppProps():
    def __init__(self, *, kinesis_firehose: aws_cdk.aws_kinesisfirehose.CfnDeliveryStream, kinesis_analytics_props: typing.Any=None) -> None:
        """
        :param kinesis_firehose: A Kinesis Data Firehose for the Kinesis Streams application to connect to. Default: - Default props are used
        :param kinesis_analytics_props: Optional user provided props to override the default props for the Kinesis analytics app. Default: - Default props are used
        """
        self._values = {
            'kinesis_firehose': kinesis_firehose,
        }
        if kinesis_analytics_props is not None: self._values["kinesis_analytics_props"] = kinesis_analytics_props

    @builtins.property
    def kinesis_firehose(self) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream:
        """A Kinesis Data Firehose for the Kinesis Streams application to connect to.

        default
        :default: - Default props are used
        """
        return self._values.get('kinesis_firehose')

    @builtins.property
    def kinesis_analytics_props(self) -> typing.Any:
        """Optional user provided props to override the default props for the Kinesis analytics app.

        default
        :default: - Default props are used
        """
        return self._values.get('kinesis_analytics_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BuildKinesisAnalyticsAppProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-solutions-constructs/core.BuildKinesisStreamProps", jsii_struct_bases=[], name_mapping={'kinesis_stream_props': 'kinesisStreamProps'})
class BuildKinesisStreamProps():
    def __init__(self, *, kinesis_stream_props: typing.Any=None) -> None:
        """
        :param kinesis_stream_props: Optional user provided props to override the default props for the Kinesis stream. Default: - Default props are used.
        """
        self._values = {
        }
        if kinesis_stream_props is not None: self._values["kinesis_stream_props"] = kinesis_stream_props

    @builtins.property
    def kinesis_stream_props(self) -> typing.Any:
        """Optional user provided props to override the default props for the Kinesis stream.

        default
        :default: - Default props are used.
        """
        return self._values.get('kinesis_stream_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BuildKinesisStreamProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-solutions-constructs/core.BuildLambdaFunctionProps", jsii_struct_bases=[], name_mapping={'deploy_lambda': 'deployLambda', 'existing_lambda_obj': 'existingLambdaObj', 'lambda_function_props': 'lambdaFunctionProps'})
class BuildLambdaFunctionProps():
    def __init__(self, *, deploy_lambda: bool, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps]=None) -> None:
        """
        :param deploy_lambda: Whether to create a new Lambda function or use an existing Lambda function. If set to false, you must provide a lambda function object as ``existingLambdaObj`` Default: - true
        :param existing_lambda_obj: Existing instance of Lambda Function object. If ``deploy`` is set to false only then this property is required Default: - None
        :param lambda_function_props: Optional user provided props to override the default props for the Lambda function. If ``deploy`` is set to true only then this property is required Default: - Default props are used
        """
        if isinstance(lambda_function_props, dict): lambda_function_props = aws_cdk.aws_lambda.FunctionProps(**lambda_function_props)
        self._values = {
            'deploy_lambda': deploy_lambda,
        }
        if existing_lambda_obj is not None: self._values["existing_lambda_obj"] = existing_lambda_obj
        if lambda_function_props is not None: self._values["lambda_function_props"] = lambda_function_props

    @builtins.property
    def deploy_lambda(self) -> bool:
        """Whether to create a new Lambda function or use an existing Lambda function.

        If set to false, you must provide a lambda function object as ``existingLambdaObj``

        default
        :default: - true
        """
        return self._values.get('deploy_lambda')

    @builtins.property
    def existing_lambda_obj(self) -> typing.Optional[aws_cdk.aws_lambda.Function]:
        """Existing instance of Lambda Function object.

        If ``deploy`` is set to false only then this property is required

        default
        :default: - None
        """
        return self._values.get('existing_lambda_obj')

    @builtins.property
    def lambda_function_props(self) -> typing.Optional[aws_cdk.aws_lambda.FunctionProps]:
        """Optional user provided props to override the default props for the Lambda function.

        If ``deploy`` is set to true only then this property is required

        default
        :default: - Default props are used
        """
        return self._values.get('lambda_function_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BuildLambdaFunctionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-solutions-constructs/core.BuildQueueProps", jsii_struct_bases=[], name_mapping={'dead_letter_queue': 'deadLetterQueue', 'queue_props': 'queueProps'})
class BuildQueueProps():
    def __init__(self, *, dead_letter_queue: typing.Optional[aws_cdk.aws_sqs.DeadLetterQueue]=None, queue_props: typing.Any=None) -> None:
        """
        :param dead_letter_queue: Optional dead letter queue to pass bad requests to after the max receive count is reached. Default: - Default props are used.
        :param queue_props: Optional user provided props to override the default props for the primary queue. Default: - Default props are used.
        """
        if isinstance(dead_letter_queue, dict): dead_letter_queue = aws_cdk.aws_sqs.DeadLetterQueue(**dead_letter_queue)
        self._values = {
        }
        if dead_letter_queue is not None: self._values["dead_letter_queue"] = dead_letter_queue
        if queue_props is not None: self._values["queue_props"] = queue_props

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[aws_cdk.aws_sqs.DeadLetterQueue]:
        """Optional dead letter queue to pass bad requests to after the max receive count is reached.

        default
        :default: - Default props are used.
        """
        return self._values.get('dead_letter_queue')

    @builtins.property
    def queue_props(self) -> typing.Any:
        """Optional user provided props to override the default props for the primary queue.

        default
        :default: - Default props are used.
        """
        return self._values.get('queue_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BuildQueueProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-solutions-constructs/core.BuildS3BucketProps", jsii_struct_bases=[], name_mapping={'bucket_props': 'bucketProps', 'deploy_bucket': 'deployBucket', 'existing_bucket_obj': 'existingBucketObj'})
class BuildS3BucketProps():
    def __init__(self, *, bucket_props: typing.Optional[aws_cdk.aws_s3.BucketProps]=None, deploy_bucket: typing.Optional[bool]=None, existing_bucket_obj: typing.Optional[aws_cdk.aws_s3.Bucket]=None) -> None:
        """
        :param bucket_props: Optional user provided props to override the default props. If ``deploy`` is set to true only then this property is required Default: - Default props are used
        :param deploy_bucket: Whether to create a S3 Bucket or use an existing S3 Bucket. If set to false, you must provide S3 Bucket as ``existingBucketObj`` Default: - true
        :param existing_bucket_obj: Existing instance of S3 Bucket object. If ``deployBucket`` is set to false only then this property is required Default: - None
        """
        if isinstance(bucket_props, dict): bucket_props = aws_cdk.aws_s3.BucketProps(**bucket_props)
        self._values = {
        }
        if bucket_props is not None: self._values["bucket_props"] = bucket_props
        if deploy_bucket is not None: self._values["deploy_bucket"] = deploy_bucket
        if existing_bucket_obj is not None: self._values["existing_bucket_obj"] = existing_bucket_obj

    @builtins.property
    def bucket_props(self) -> typing.Optional[aws_cdk.aws_s3.BucketProps]:
        """Optional user provided props to override the default props.

        If ``deploy`` is set to true only then this property is required

        default
        :default: - Default props are used
        """
        return self._values.get('bucket_props')

    @builtins.property
    def deploy_bucket(self) -> typing.Optional[bool]:
        """Whether to create a S3 Bucket or use an existing S3 Bucket.

        If set to false, you must provide S3 Bucket as ``existingBucketObj``

        default
        :default: - true
        """
        return self._values.get('deploy_bucket')

    @builtins.property
    def existing_bucket_obj(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        """Existing instance of S3 Bucket object.

        If ``deployBucket`` is set to false only then this property is required

        default
        :default: - None
        """
        return self._values.get('existing_bucket_obj')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BuildS3BucketProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-solutions-constructs/core.BuildTopicProps", jsii_struct_bases=[], name_mapping={'enable_encryption': 'enableEncryption', 'encryption_key': 'encryptionKey', 'topic_props': 'topicProps'})
class BuildTopicProps():
    def __init__(self, *, enable_encryption: typing.Optional[bool]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.Key]=None, topic_props: typing.Any=None) -> None:
        """
        :param enable_encryption: Use a KMS Key, either managed by this CDK app, or imported. If importing an encryption key, it must be specified in the encryptionKey property for this construct. Default: - true (encryption enabled, managed by this CDK app).
        :param encryption_key: An optional, imported encryption key to encrypt the SNS topic with. Default: - not specified.
        :param topic_props: Optional user provided props to override the default props for the SNS topic. Default: - Default props are used.
        """
        self._values = {
        }
        if enable_encryption is not None: self._values["enable_encryption"] = enable_encryption
        if encryption_key is not None: self._values["encryption_key"] = encryption_key
        if topic_props is not None: self._values["topic_props"] = topic_props

    @builtins.property
    def enable_encryption(self) -> typing.Optional[bool]:
        """Use a KMS Key, either managed by this CDK app, or imported.

        If importing an encryption key, it must be specified in
        the encryptionKey property for this construct.

        default
        :default: - true (encryption enabled, managed by this CDK app).
        """
        return self._values.get('enable_encryption')

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.Key]:
        """An optional, imported encryption key to encrypt the SNS topic with.

        default
        :default: - not specified.
        """
        return self._values.get('encryption_key')

    @builtins.property
    def topic_props(self) -> typing.Any:
        """Optional user provided props to override the default props for the SNS topic.

        default
        :default: - Default props are used.
        """
        return self._values.get('topic_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BuildTopicProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-solutions-constructs/core.CfnDomainOptions", jsii_struct_bases=[], name_mapping={'cognito_authorized_role_arn': 'cognitoAuthorizedRoleARN', 'identitypool': 'identitypool', 'userpool': 'userpool', 'service_role_arn': 'serviceRoleARN'})
class CfnDomainOptions():
    def __init__(self, *, cognito_authorized_role_arn: str, identitypool: aws_cdk.aws_cognito.CfnIdentityPool, userpool: aws_cdk.aws_cognito.UserPool, service_role_arn: typing.Optional[str]=None) -> None:
        """
        :param cognito_authorized_role_arn: -
        :param identitypool: -
        :param userpool: -
        :param service_role_arn: -
        """
        self._values = {
            'cognito_authorized_role_arn': cognito_authorized_role_arn,
            'identitypool': identitypool,
            'userpool': userpool,
        }
        if service_role_arn is not None: self._values["service_role_arn"] = service_role_arn

    @builtins.property
    def cognito_authorized_role_arn(self) -> str:
        return self._values.get('cognito_authorized_role_arn')

    @builtins.property
    def identitypool(self) -> aws_cdk.aws_cognito.CfnIdentityPool:
        return self._values.get('identitypool')

    @builtins.property
    def userpool(self) -> aws_cdk.aws_cognito.UserPool:
        return self._values.get('userpool')

    @builtins.property
    def service_role_arn(self) -> typing.Optional[str]:
        return self._values.get('service_role_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDomainOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-solutions-constructs/core.CognitoOptions", jsii_struct_bases=[], name_mapping={'identitypool': 'identitypool', 'userpool': 'userpool', 'userpoolclient': 'userpoolclient'})
class CognitoOptions():
    def __init__(self, *, identitypool: aws_cdk.aws_cognito.CfnIdentityPool, userpool: aws_cdk.aws_cognito.UserPool, userpoolclient: aws_cdk.aws_cognito.UserPoolClient) -> None:
        """
        :param identitypool: -
        :param userpool: -
        :param userpoolclient: -
        """
        self._values = {
            'identitypool': identitypool,
            'userpool': userpool,
            'userpoolclient': userpoolclient,
        }

    @builtins.property
    def identitypool(self) -> aws_cdk.aws_cognito.CfnIdentityPool:
        return self._values.get('identitypool')

    @builtins.property
    def userpool(self) -> aws_cdk.aws_cognito.UserPool:
        return self._values.get('userpool')

    @builtins.property
    def userpoolclient(self) -> aws_cdk.aws_cognito.UserPoolClient:
        return self._values.get('userpoolclient')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CognitoOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "BuildDeadLetterQueueProps",
    "BuildDynamoDBTableProps",
    "BuildEncryptionKeyProps",
    "BuildKinesisAnalyticsAppProps",
    "BuildKinesisStreamProps",
    "BuildLambdaFunctionProps",
    "BuildQueueProps",
    "BuildS3BucketProps",
    "BuildTopicProps",
    "CfnDomainOptions",
    "CognitoOptions",
]

publication.publish()
