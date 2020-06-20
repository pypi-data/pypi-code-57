import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (Duration as _Duration_5170c158)
from ..aws_apigateway import (MethodOptions as _MethodOptions_0e815882)
from ..aws_dynamodb import (ITable as _ITable_e6850701)
from ..aws_kinesis import (IStream as _IStream_c7ff3ed6)
from ..aws_lambda import (IFunction as _IFunction_1c1de0bc, IEventSource as _IEventSource_0e6bcb85, StartingPosition as _StartingPosition_98f65751, IEventSourceDlq as _IEventSourceDlq_64554172, DlqDestinationConfig as _DlqDestinationConfig_986227db, IEventSourceMapping as _IEventSourceMapping_803047f8, EventSourceMappingOptions as _EventSourceMappingOptions_2fe36144)
from ..aws_s3 import (Bucket as _Bucket_abb659b1, EventType as _EventType_726686dc, NotificationKeyFilter as _NotificationKeyFilter_c547ae3c)
from ..aws_sns import (ITopic as _ITopic_ef0ebe0e)
from ..aws_sqs import (IQueue as _IQueue_b743f559)


@jsii.implements(_IEventSource_0e6bcb85)
class ApiEventSource(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda_event_sources.ApiEventSource"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, method: str, path: str, *, api_key_required: typing.Optional[bool]=None, authorization_scopes: typing.Optional[typing.List[str]]=None, authorization_type: typing.Optional[_AuthorizationType_2cb72e24]=None, authorizer: typing.Optional[_IAuthorizer_fd7d6200]=None, method_responses: typing.Optional[typing.List[_MethodResponse_fdda6847]]=None, operation_name: typing.Optional[str]=None, request_models: typing.Optional[typing.Mapping[str, _IModel_13fecd8f]]=None, request_parameters: typing.Optional[typing.Mapping[str, bool]]=None, request_validator: typing.Optional[_IRequestValidator_f057dc3b]=None, request_validator_options: typing.Optional[_RequestValidatorOptions_7a8ad269]=None) -> None:
        """
        :param method: -
        :param path: -
        :param api_key_required: Indicates whether the method requires clients to submit a valid API key. Default: false
        :param authorization_scopes: A list of authorization scopes configured on the method. The scopes are used with a COGNITO_USER_POOLS authorizer to authorize the method invocation. Default: - no authorization scopes
        :param authorization_type: Method authorization. If the value is set of ``Custom``, an ``authorizer`` must also be specified. If you're using one of the authorizers that are available via the {@link Authorizer} class, such as {@link Authorizer#token()}, it is recommended that this option not be specified. The authorizer will take care of setting the correct authorization type. However, specifying an authorization type using this property that conflicts with what is expected by the {@link Authorizer} will result in an error. Default: - open access unless ``authorizer`` is specified
        :param authorizer: If ``authorizationType`` is ``Custom``, this specifies the ID of the method authorizer resource. If specified, the value of ``authorizationType`` must be set to ``Custom``
        :param method_responses: The responses that can be sent to the client who calls the method. Default: None This property is not required, but if these are not supplied for a Lambda proxy integration, the Lambda function must return a value of the correct format, for the integration response to be correctly mapped to a response to the client.
        :param operation_name: A friendly operation name for the method. For example, you can assign the OperationName of ListPets for the GET /pets method.
        :param request_models: The models which describe data structure of request payload. When combined with ``requestValidator`` or ``requestValidatorOptions``, the service will validate the API request payload before it reaches the API's Integration (including proxies). Specify ``requestModels`` as key-value pairs, with a content type (e.g. ``'application/json'``) as the key and an API Gateway Model as the value.
        :param request_parameters: The request parameters that API Gateway accepts. Specify request parameters as key-value pairs (string-to-Boolean mapping), with a source as the key and a Boolean as the value. The Boolean specifies whether a parameter is required. A source must match the format method.request.location.name, where the location is querystring, path, or header, and name is a valid, unique parameter name. Default: None
        :param request_validator: The ID of the associated request validator. Only one of ``requestValidator`` or ``requestValidatorOptions`` must be specified. Works together with ``requestModels`` or ``requestParameters`` to validate the request before it reaches integration like Lambda Proxy Integration. Default: - No default validator
        :param request_validator_options: Request validator options to create new validator Only one of ``requestValidator`` or ``requestValidatorOptions`` must be specified. Works together with ``requestModels`` or ``requestParameters`` to validate the request before it reaches integration like Lambda Proxy Integration. Default: - No default validator

        stability
        :stability: experimental
        """
        options = _MethodOptions_0e815882(api_key_required=api_key_required, authorization_scopes=authorization_scopes, authorization_type=authorization_type, authorizer=authorizer, method_responses=method_responses, operation_name=operation_name, request_models=request_models, request_parameters=request_parameters, request_validator=request_validator, request_validator_options=request_validator_options)

        jsii.create(ApiEventSource, self, [method, path, options])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_1c1de0bc) -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [target])


@jsii.implements(_IEventSource_0e6bcb85)
class S3EventSource(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda_event_sources.S3EventSource"):
    """Use S3 bucket notifications as an event source for AWS Lambda.

    stability
    :stability: experimental
    """
    def __init__(self, bucket: _Bucket_abb659b1, *, events: typing.List[_EventType_726686dc], filters: typing.Optional[typing.List[_NotificationKeyFilter_c547ae3c]]=None) -> None:
        """
        :param bucket: -
        :param events: The s3 event types that will trigger the notification.
        :param filters: S3 object key filter rules to determine which objects trigger this event. Each filter must include a ``prefix`` and/or ``suffix`` that will be matched against the s3 object key. Refer to the S3 Developer Guide for details about allowed filter rules.

        stability
        :stability: experimental
        """
        props = S3EventSourceProps(events=events, filters=filters)

        jsii.create(S3EventSource, self, [bucket, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_1c1de0bc) -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [target])

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _Bucket_abb659b1:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "bucket")


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda_event_sources.S3EventSourceProps", jsii_struct_bases=[], name_mapping={'events': 'events', 'filters': 'filters'})
class S3EventSourceProps():
    def __init__(self, *, events: typing.List[_EventType_726686dc], filters: typing.Optional[typing.List[_NotificationKeyFilter_c547ae3c]]=None) -> None:
        """
        :param events: The s3 event types that will trigger the notification.
        :param filters: S3 object key filter rules to determine which objects trigger this event. Each filter must include a ``prefix`` and/or ``suffix`` that will be matched against the s3 object key. Refer to the S3 Developer Guide for details about allowed filter rules.

        stability
        :stability: experimental
        """
        self._values = {
            'events': events,
        }
        if filters is not None: self._values["filters"] = filters

    @builtins.property
    def events(self) -> typing.List[_EventType_726686dc]:
        """The s3 event types that will trigger the notification.

        stability
        :stability: experimental
        """
        return self._values.get('events')

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[_NotificationKeyFilter_c547ae3c]]:
        """S3 object key filter rules to determine which objects trigger this event.

        Each filter must include a ``prefix`` and/or ``suffix`` that will be matched
        against the s3 object key. Refer to the S3 Developer Guide for details
        about allowed filter rules.

        stability
        :stability: experimental
        """
        return self._values.get('filters')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'S3EventSourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IEventSourceDlq_64554172)
class SnsDlq(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda_event_sources.SnsDlq"):
    """An SNS dead letter queue destination configuration for a Lambda event source.

    stability
    :stability: experimental
    """
    def __init__(self, topic: _ITopic_ef0ebe0e) -> None:
        """
        :param topic: -

        stability
        :stability: experimental
        """
        jsii.create(SnsDlq, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(self, _target: _IEventSourceMapping_803047f8, target_handler: _IFunction_1c1de0bc) -> _DlqDestinationConfig_986227db:
        """Returns a destination configuration for the DLQ.

        :param _target: -
        :param target_handler: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_target, target_handler])


@jsii.implements(_IEventSource_0e6bcb85)
class SnsEventSource(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda_event_sources.SnsEventSource"):
    """Use an Amazon SNS topic as an event source for AWS Lambda.

    stability
    :stability: experimental
    """
    def __init__(self, topic: _ITopic_ef0ebe0e) -> None:
        """
        :param topic: -

        stability
        :stability: experimental
        """
        jsii.create(SnsEventSource, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_1c1de0bc) -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [target])

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> _ITopic_ef0ebe0e:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "topic")


@jsii.implements(_IEventSourceDlq_64554172)
class SqsDlq(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda_event_sources.SqsDlq"):
    """An SQS dead letter queue destination configuration for a Lambda event source.

    stability
    :stability: experimental
    """
    def __init__(self, queue: _IQueue_b743f559) -> None:
        """
        :param queue: -

        stability
        :stability: experimental
        """
        jsii.create(SqsDlq, self, [queue])

    @jsii.member(jsii_name="bind")
    def bind(self, _target: _IEventSourceMapping_803047f8, target_handler: _IFunction_1c1de0bc) -> _DlqDestinationConfig_986227db:
        """Returns a destination configuration for the DLQ.

        :param _target: -
        :param target_handler: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_target, target_handler])


@jsii.implements(_IEventSource_0e6bcb85)
class SqsEventSource(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda_event_sources.SqsEventSource"):
    """Use an Amazon SQS queue as an event source for AWS Lambda.

    stability
    :stability: experimental
    """
    def __init__(self, queue: _IQueue_b743f559, *, batch_size: typing.Optional[jsii.Number]=None) -> None:
        """
        :param queue: -
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10. Default: 10

        stability
        :stability: experimental
        """
        props = SqsEventSourceProps(batch_size=batch_size)

        jsii.create(SqsEventSource, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_1c1de0bc) -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [target])

    @builtins.property
    @jsii.member(jsii_name="eventSourceMappingId")
    def event_source_mapping_id(self) -> str:
        """The identifier for this EventSourceMapping.

        stability
        :stability: experimental
        """
        return jsii.get(self, "eventSourceMappingId")

    @builtins.property
    @jsii.member(jsii_name="queue")
    def queue(self) -> _IQueue_b743f559:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "queue")


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda_event_sources.SqsEventSourceProps", jsii_struct_bases=[], name_mapping={'batch_size': 'batchSize'})
class SqsEventSourceProps():
    def __init__(self, *, batch_size: typing.Optional[jsii.Number]=None) -> None:
        """
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10. Default: 10

        stability
        :stability: experimental
        """
        self._values = {
        }
        if batch_size is not None: self._values["batch_size"] = batch_size

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        """The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range: Minimum value of 1. Maximum value of 10.

        default
        :default: 10

        stability
        :stability: experimental
        """
        return self._values.get('batch_size')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SqsEventSourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IEventSource_0e6bcb85)
class StreamEventSource(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_lambda_event_sources.StreamEventSource"):
    """Use an stream as an event source for AWS Lambda.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _StreamEventSourceProxy

    def __init__(self, *, starting_position: _StartingPosition_98f65751, batch_size: typing.Optional[jsii.Number]=None, bisect_batch_on_error: typing.Optional[bool]=None, max_batching_window: typing.Optional[_Duration_5170c158]=None, max_record_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional[_IEventSourceDlq_64554172]=None, parallelization_factor: typing.Optional[jsii.Number]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """
        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        stability
        :stability: experimental
        """
        props = StreamEventSourceProps(starting_position=starting_position, batch_size=batch_size, bisect_batch_on_error=bisect_batch_on_error, max_batching_window=max_batching_window, max_record_age=max_record_age, on_failure=on_failure, parallelization_factor=parallelization_factor, retry_attempts=retry_attempts)

        jsii.create(StreamEventSource, self, [props])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, _target: _IFunction_1c1de0bc) -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param _target: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="enrichMappingOptions")
    def _enrich_mapping_options(self, *, event_source_arn: str, batch_size: typing.Optional[jsii.Number]=None, bisect_batch_on_error: typing.Optional[bool]=None, enabled: typing.Optional[bool]=None, max_batching_window: typing.Optional[_Duration_5170c158]=None, max_record_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional[_IEventSourceDlq_64554172]=None, parallelization_factor: typing.Optional[jsii.Number]=None, retry_attempts: typing.Optional[jsii.Number]=None, starting_position: typing.Optional[_StartingPosition_98f65751]=None) -> _EventSourceMappingOptions_2fe36144:
        """
        :param event_source_arn: The Amazon Resource Name (ARN) of the event source. Any record added to this stream can invoke the Lambda function.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10000. Default: - Amazon Kinesis and Amazon DynamoDB is 100 records. Both the default and maximum for Amazon SQS are 10 messages.
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: Set to false to disable the event source upon creation. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Valid Range: - Minimum value of 0 - Maximum value of 10000 Default: 10000
        :param starting_position: The position in the DynamoDB or Kinesis stream where AWS Lambda should start reading. Default: - Required for Amazon Kinesis and Amazon DynamoDB Streams sources.

        stability
        :stability: experimental
        """
        options = _EventSourceMappingOptions_2fe36144(event_source_arn=event_source_arn, batch_size=batch_size, bisect_batch_on_error=bisect_batch_on_error, enabled=enabled, max_batching_window=max_batching_window, max_record_age=max_record_age, on_failure=on_failure, parallelization_factor=parallelization_factor, retry_attempts=retry_attempts, starting_position=starting_position)

        return jsii.invoke(self, "enrichMappingOptions", [options])

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "StreamEventSourceProps":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "props")


class _StreamEventSourceProxy(StreamEventSource):
    @jsii.member(jsii_name="bind")
    def bind(self, _target: _IFunction_1c1de0bc) -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param _target: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_target])


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda_event_sources.StreamEventSourceProps", jsii_struct_bases=[], name_mapping={'starting_position': 'startingPosition', 'batch_size': 'batchSize', 'bisect_batch_on_error': 'bisectBatchOnError', 'max_batching_window': 'maxBatchingWindow', 'max_record_age': 'maxRecordAge', 'on_failure': 'onFailure', 'parallelization_factor': 'parallelizationFactor', 'retry_attempts': 'retryAttempts'})
class StreamEventSourceProps():
    def __init__(self, *, starting_position: _StartingPosition_98f65751, batch_size: typing.Optional[jsii.Number]=None, bisect_batch_on_error: typing.Optional[bool]=None, max_batching_window: typing.Optional[_Duration_5170c158]=None, max_record_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional[_IEventSourceDlq_64554172]=None, parallelization_factor: typing.Optional[jsii.Number]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """The set of properties for event sources that follow the streaming model, such as, Dynamo and Kinesis.

        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        stability
        :stability: experimental
        """
        self._values = {
            'starting_position': starting_position,
        }
        if batch_size is not None: self._values["batch_size"] = batch_size
        if bisect_batch_on_error is not None: self._values["bisect_batch_on_error"] = bisect_batch_on_error
        if max_batching_window is not None: self._values["max_batching_window"] = max_batching_window
        if max_record_age is not None: self._values["max_record_age"] = max_record_age
        if on_failure is not None: self._values["on_failure"] = on_failure
        if parallelization_factor is not None: self._values["parallelization_factor"] = parallelization_factor
        if retry_attempts is not None: self._values["retry_attempts"] = retry_attempts

    @builtins.property
    def starting_position(self) -> _StartingPosition_98f65751:
        """Where to begin consuming the stream.

        stability
        :stability: experimental
        """
        return self._values.get('starting_position')

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        """The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}

        default
        :default: 100

        stability
        :stability: experimental
        """
        return self._values.get('batch_size')

    @builtins.property
    def bisect_batch_on_error(self) -> typing.Optional[bool]:
        """If the function returns an error, split the batch in two and retry.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('bisect_batch_on_error')

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        default
        :default: Duration.seconds(0)

        stability
        :stability: experimental
        """
        return self._values.get('max_batching_window')

    @builtins.property
    def max_record_age(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum age of a record that Lambda sends to a function for processing.

        Valid Range:

        - Minimum value of 60 seconds
        - Maximum value of 7 days

        default
        :default: Duration.days(7)

        stability
        :stability: experimental
        """
        return self._values.get('max_record_age')

    @builtins.property
    def on_failure(self) -> typing.Optional[_IEventSourceDlq_64554172]:
        """An Amazon SQS queue or Amazon SNS topic destination for discarded records.

        default
        :default: discarded records are ignored

        stability
        :stability: experimental
        """
        return self._values.get('on_failure')

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        """The number of batches to process from each shard concurrently.

        Valid Range:

        - Minimum value of 1
        - Maximum value of 10

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('parallelization_factor')

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000.

        default
        :default: 10000

        stability
        :stability: experimental
        """
        return self._values.get('retry_attempts')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StreamEventSourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class DynamoEventSource(StreamEventSource, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda_event_sources.DynamoEventSource"):
    """Use an Amazon DynamoDB stream as an event source for AWS Lambda.

    stability
    :stability: experimental
    """
    def __init__(self, table: _ITable_e6850701, *, starting_position: _StartingPosition_98f65751, batch_size: typing.Optional[jsii.Number]=None, bisect_batch_on_error: typing.Optional[bool]=None, max_batching_window: typing.Optional[_Duration_5170c158]=None, max_record_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional[_IEventSourceDlq_64554172]=None, parallelization_factor: typing.Optional[jsii.Number]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """
        :param table: -
        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        stability
        :stability: experimental
        """
        props = DynamoEventSourceProps(starting_position=starting_position, batch_size=batch_size, bisect_batch_on_error=bisect_batch_on_error, max_batching_window=max_batching_window, max_record_age=max_record_age, on_failure=on_failure, parallelization_factor=parallelization_factor, retry_attempts=retry_attempts)

        jsii.create(DynamoEventSource, self, [table, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_1c1de0bc) -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [target])

    @builtins.property
    @jsii.member(jsii_name="eventSourceMappingId")
    def event_source_mapping_id(self) -> str:
        """The identifier for this EventSourceMapping.

        stability
        :stability: experimental
        """
        return jsii.get(self, "eventSourceMappingId")


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda_event_sources.DynamoEventSourceProps", jsii_struct_bases=[StreamEventSourceProps], name_mapping={'starting_position': 'startingPosition', 'batch_size': 'batchSize', 'bisect_batch_on_error': 'bisectBatchOnError', 'max_batching_window': 'maxBatchingWindow', 'max_record_age': 'maxRecordAge', 'on_failure': 'onFailure', 'parallelization_factor': 'parallelizationFactor', 'retry_attempts': 'retryAttempts'})
class DynamoEventSourceProps(StreamEventSourceProps):
    def __init__(self, *, starting_position: _StartingPosition_98f65751, batch_size: typing.Optional[jsii.Number]=None, bisect_batch_on_error: typing.Optional[bool]=None, max_batching_window: typing.Optional[_Duration_5170c158]=None, max_record_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional[_IEventSourceDlq_64554172]=None, parallelization_factor: typing.Optional[jsii.Number]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """
        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        stability
        :stability: experimental
        """
        self._values = {
            'starting_position': starting_position,
        }
        if batch_size is not None: self._values["batch_size"] = batch_size
        if bisect_batch_on_error is not None: self._values["bisect_batch_on_error"] = bisect_batch_on_error
        if max_batching_window is not None: self._values["max_batching_window"] = max_batching_window
        if max_record_age is not None: self._values["max_record_age"] = max_record_age
        if on_failure is not None: self._values["on_failure"] = on_failure
        if parallelization_factor is not None: self._values["parallelization_factor"] = parallelization_factor
        if retry_attempts is not None: self._values["retry_attempts"] = retry_attempts

    @builtins.property
    def starting_position(self) -> _StartingPosition_98f65751:
        """Where to begin consuming the stream.

        stability
        :stability: experimental
        """
        return self._values.get('starting_position')

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        """The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}

        default
        :default: 100

        stability
        :stability: experimental
        """
        return self._values.get('batch_size')

    @builtins.property
    def bisect_batch_on_error(self) -> typing.Optional[bool]:
        """If the function returns an error, split the batch in two and retry.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('bisect_batch_on_error')

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        default
        :default: Duration.seconds(0)

        stability
        :stability: experimental
        """
        return self._values.get('max_batching_window')

    @builtins.property
    def max_record_age(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum age of a record that Lambda sends to a function for processing.

        Valid Range:

        - Minimum value of 60 seconds
        - Maximum value of 7 days

        default
        :default: Duration.days(7)

        stability
        :stability: experimental
        """
        return self._values.get('max_record_age')

    @builtins.property
    def on_failure(self) -> typing.Optional[_IEventSourceDlq_64554172]:
        """An Amazon SQS queue or Amazon SNS topic destination for discarded records.

        default
        :default: discarded records are ignored

        stability
        :stability: experimental
        """
        return self._values.get('on_failure')

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        """The number of batches to process from each shard concurrently.

        Valid Range:

        - Minimum value of 1
        - Maximum value of 10

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('parallelization_factor')

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000.

        default
        :default: 10000

        stability
        :stability: experimental
        """
        return self._values.get('retry_attempts')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DynamoEventSourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class KinesisEventSource(StreamEventSource, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda_event_sources.KinesisEventSource"):
    """Use an Amazon Kinesis stream as an event source for AWS Lambda.

    stability
    :stability: experimental
    """
    def __init__(self, stream: _IStream_c7ff3ed6, *, starting_position: _StartingPosition_98f65751, batch_size: typing.Optional[jsii.Number]=None, bisect_batch_on_error: typing.Optional[bool]=None, max_batching_window: typing.Optional[_Duration_5170c158]=None, max_record_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional[_IEventSourceDlq_64554172]=None, parallelization_factor: typing.Optional[jsii.Number]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """
        :param stream: -
        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        stability
        :stability: experimental
        """
        props = KinesisEventSourceProps(starting_position=starting_position, batch_size=batch_size, bisect_batch_on_error=bisect_batch_on_error, max_batching_window=max_batching_window, max_record_age=max_record_age, on_failure=on_failure, parallelization_factor=parallelization_factor, retry_attempts=retry_attempts)

        jsii.create(KinesisEventSource, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_1c1de0bc) -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [target])

    @builtins.property
    @jsii.member(jsii_name="eventSourceMappingId")
    def event_source_mapping_id(self) -> str:
        """The identifier for this EventSourceMapping.

        stability
        :stability: experimental
        """
        return jsii.get(self, "eventSourceMappingId")

    @builtins.property
    @jsii.member(jsii_name="stream")
    def stream(self) -> _IStream_c7ff3ed6:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "stream")


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda_event_sources.KinesisEventSourceProps", jsii_struct_bases=[StreamEventSourceProps], name_mapping={'starting_position': 'startingPosition', 'batch_size': 'batchSize', 'bisect_batch_on_error': 'bisectBatchOnError', 'max_batching_window': 'maxBatchingWindow', 'max_record_age': 'maxRecordAge', 'on_failure': 'onFailure', 'parallelization_factor': 'parallelizationFactor', 'retry_attempts': 'retryAttempts'})
class KinesisEventSourceProps(StreamEventSourceProps):
    def __init__(self, *, starting_position: _StartingPosition_98f65751, batch_size: typing.Optional[jsii.Number]=None, bisect_batch_on_error: typing.Optional[bool]=None, max_batching_window: typing.Optional[_Duration_5170c158]=None, max_record_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional[_IEventSourceDlq_64554172]=None, parallelization_factor: typing.Optional[jsii.Number]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """
        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        stability
        :stability: experimental
        """
        self._values = {
            'starting_position': starting_position,
        }
        if batch_size is not None: self._values["batch_size"] = batch_size
        if bisect_batch_on_error is not None: self._values["bisect_batch_on_error"] = bisect_batch_on_error
        if max_batching_window is not None: self._values["max_batching_window"] = max_batching_window
        if max_record_age is not None: self._values["max_record_age"] = max_record_age
        if on_failure is not None: self._values["on_failure"] = on_failure
        if parallelization_factor is not None: self._values["parallelization_factor"] = parallelization_factor
        if retry_attempts is not None: self._values["retry_attempts"] = retry_attempts

    @builtins.property
    def starting_position(self) -> _StartingPosition_98f65751:
        """Where to begin consuming the stream.

        stability
        :stability: experimental
        """
        return self._values.get('starting_position')

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        """The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}

        default
        :default: 100

        stability
        :stability: experimental
        """
        return self._values.get('batch_size')

    @builtins.property
    def bisect_batch_on_error(self) -> typing.Optional[bool]:
        """If the function returns an error, split the batch in two and retry.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('bisect_batch_on_error')

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        default
        :default: Duration.seconds(0)

        stability
        :stability: experimental
        """
        return self._values.get('max_batching_window')

    @builtins.property
    def max_record_age(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum age of a record that Lambda sends to a function for processing.

        Valid Range:

        - Minimum value of 60 seconds
        - Maximum value of 7 days

        default
        :default: Duration.days(7)

        stability
        :stability: experimental
        """
        return self._values.get('max_record_age')

    @builtins.property
    def on_failure(self) -> typing.Optional[_IEventSourceDlq_64554172]:
        """An Amazon SQS queue or Amazon SNS topic destination for discarded records.

        default
        :default: discarded records are ignored

        stability
        :stability: experimental
        """
        return self._values.get('on_failure')

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        """The number of batches to process from each shard concurrently.

        Valid Range:

        - Minimum value of 1
        - Maximum value of 10

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('parallelization_factor')

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000.

        default
        :default: 10000

        stability
        :stability: experimental
        """
        return self._values.get('retry_attempts')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'KinesisEventSourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "ApiEventSource",
    "DynamoEventSource",
    "DynamoEventSourceProps",
    "KinesisEventSource",
    "KinesisEventSourceProps",
    "S3EventSource",
    "S3EventSourceProps",
    "SnsDlq",
    "SnsEventSource",
    "SqsDlq",
    "SqsEventSource",
    "SqsEventSourceProps",
    "StreamEventSource",
    "StreamEventSourceProps",
]

publication.publish()
