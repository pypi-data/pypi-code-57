from datetime import datetime as datetime
import json
from servicemapper.decorators import trace
from servicemapper.ioc import Core, Mapper
from servicemapper.types import Constants, DataDialect, EventSources, Operations, ServiceConnectorData, _operation_dialect_factory, _queue_arn_to_url


class MapperWorker():

    def __init__(self):
        self.logger = Core.logger()
        self.service_connector = Mapper.service_connector()
        self.sqs_client = Mapper.sqs_client()

        config = Core.config()
        self.inbound_queue_url = config['service_mapper']['inbound_queue_url']
        assert isinstance(self.inbound_queue_url, str)

        self.outbound_queue_url = config['service_mapper']['outbound_queue_url']
        assert isinstance(self.outbound_queue_url, str)

        self.EVENT_SOURCE_OPERATION = {
            EventSources.QUEUE: _operation_dialect_factory(Operations.PUSH_TO_SERVICE, DataDialect.DATA_STEWARD),
            EventSources.TIMER: _operation_dialect_factory(Operations.PULL_FROM_SERVICE, DataDialect.CONNECTED_SERVICE),
            EventSources.WEBHOOK: _operation_dialect_factory(Operations.RECEIVE_FROM_SERVICE, DataDialect.CONNECTED_SERVICE),
            EventSources.OTHER: _operation_dialect_factory(Operations.NOOP, DataDialect.NONE)
        }      

    @trace
    def _cleanup_input_event(self, record) -> None:
        """Do any cleanup work needed for the input event (i.e. delete from queue)
        
        Arguments:
            record {[type]} -- [description]
        """
        self.logger.debug('BEGIN: _cleanup_input_event')
        source = self._get_event_source(record=record)
        self.logger.debug(f'Source: {source}')

        if source == EventSources.QUEUE:
            self.logger.info('Deleting message from queue')
            url = _queue_arn_to_url(queue_arn=record['eventSourceARN'])
            receipt_handle = record['receiptHandle']
            self.sqs_client.delete_message(QueueUrl=url, ReceiptHandle=receipt_handle)
            
    @trace
    def _get_event_source(self, record) -> EventSources:
        """Get the event source based on the input record
        
        Arguments:
            record {Input record} -- An SQS, SNS, or CloudWatch record
        
        Returns:
            EventSources -- The event source
        """
        if ('eventSource' in record and record['eventSource'] == 'aws:sqs'):
            event_source = EventSources.QUEUE
        elif ('EventSource' in record and record['EventSource'] == 'aws:sns'):
            event_source = EventSources.WEBHOOK
        elif ('source' in record and record['source'] == 'aws.events'):
            event_source = EventSources.TIMER
        else:
            raise ValueError('Unsupported event source')

        return event_source

    @trace
    def _get_input_records(self, input_event) -> []:
        """Convert the input_event to an iterable list
        
        Arguments:
            input_event {Lambda Input Event} -- The event data that triggered the function\
      
        Returns:
            [records] -- List of records to process
        """
        # We can be triggered by SNS and SQS, which have a 'Records' list, or by a periodic 
        # CloudWatch event, which does not have a 'Records' list
        records = input_event['Records'] if 'Records' in input_event else [ input_event ]
        return records

    # @trace
    # def _read_from_outbound_queue(self) -> ServiceConnectorData:
    #     self.logger.error("Not Implemented: _read_from_outbound_queue")
    #     return ServiceConnectorData(data=Constants.EMPTY_DICTIONARY, dialect=DataDialect.DATA_STEWARD, timestamp=0)

    @trace
    def _read_input_data(self, record: dict) -> (ServiceConnectorData, Operations):
        """Get the input data.  The input location is dependant on the operation
           we are performing.  It may come from the connected service, the webhook
           data, or the output data queue
        
        Arguments:
            record {Input record} -- An SQS, SNS, or CloudWatch record
        
        Returns:
            (input_data, data_dialect, operation) -- Tuple consisting of the data, the dialect, and the operation
        """
        self.logger.debug(f"Record: {record}")

        # Get the event source for this record
        source = self._get_event_source(record)

        # Get the data based on the event source
        if source == EventSources.WEBHOOK or source == EventSources.TIMER:
            data = self.service_connector.read_from_service()
        elif source == EventSources.QUEUE:
            try:
                message = json.loads(record['body'])
            except Exception as e: # pragma: no cover
                error = f'Failed to load JSON from record: {record}'
                self.logger.error(error)
                raise RuntimeError(error)

            try:
                message_data = message['data']
                data_source = message['source']
                data_type = message['data_type']
            except Exception as e:
                error = f'Exception while parsing data from queue: {e}'
                self.logger.error(error)
                raise

            data = ServiceConnectorData(data=[message_data],
                                        receipt_handle=record['receiptHandle'],
                                        dialect=DataDialect.DATA_STEWARD,
                                        source=data_source,
                                        data_type=data_type,
                                        timestamp=int(datetime.utcnow().timestamp()))
        else: #pragma: no cover
            raise ValueError(f"Unknown event source: {source}")

        ret_val = (
            data, self.EVENT_SOURCE_OPERATION[source][Constants.KEY_OPERATION]
        )

        self.logger.debug(f"END: _read_input_data returning {ret_val}")
        return ret_val

    @staticmethod
    @trace
    def _run_output_builder(input_dialect: DataDialect, output_dialect: DataDialect, operation: Operations):
        return {
            Constants.KEY_INPUT: {
                Constants.KEY_DIALECT: input_dialect
            },
            Constants.KEY_OUTPUT: {
                Constants.KEY_DIALECT: output_dialect
            },
            Constants.KEY_OPERATION: operation
        }

    @trace
    def _write_output_data(self, output_data: dict, operation: Operations) -> dict:
        if operation == Operations.PUSH_TO_SERVICE:
            retval = self.service_connector.write_to_service(output_data=output_data)
        elif operation == Operations.PULL_FROM_SERVICE or operation.RECEIVE_FROM_SERVICE:
            # Write the data to the inbound queue
            retval = self._write_to_inbound_queue(data_from_service=output_data)
        elif operation == Operations.NOOP: #pragma: no cover
            self.logger.info("_write_output_data:  Operation.NOOP")
            retval = Constants.EMPTY_DICTIONARY
            pass
        else: #pragma: no cover
            raise ValueError(f"Unknown operation: {operation}")
        return retval

    @trace
    def _write_to_inbound_queue(self, data_from_service: ServiceConnectorData) -> dict:
        assert isinstance(data_from_service, ServiceConnectorData)
        # TODO:  Optimize to use send_message_batch
        items = data_from_service.data
        source = data_from_service.source
        data_type = data_from_service.data_type
        timestamp = data_from_service.timestamp

        for item in items:
            item['datasteward'] = {
                'source': source,
                'data_type': data_type,
                'timestamp': timestamp
            }
            self.sqs_client.send_message(QueueUrl=self.inbound_queue_url,
                                         MessageBody=json.dumps(item))
        return Constants.EMPTY_DICTIONARY

    @trace
    def run(self, input_event: dict, context: dict) -> dict:
        self.logger.info("BEGIN: MapperWorker.run")
        self.logger.debug(f"input_event: {json.dumps(input_event, indent=2)}")

        # Get the input data
        records = self._get_input_records(input_event=input_event)
        self.logger.debug(f"{len(records)} records in the input event")

        retval = {
            Constants.KEY_RECORDS: []
        }
        for r in records:
            self.logger.debug(f"Processing record: {r}")

            # Get the input data
            input_data, operation = self._read_input_data(record=r)

            # Translate the data to the correct dialect
            output_data = self.service_connector.translate_data(input_data=input_data)
            self.logger.info(f"Translated data from {input_data.dialect} to {output_data.dialect}")

            # Write the data to the destination
            self._write_output_data(output_data=output_data, operation=operation)

            # Finish processing the input event
            self._cleanup_input_event(record=r)

            record_retval = self._run_output_builder(input_dialect=input_data.dialect, output_dialect=output_data.dialect, operation=operation)
            retval[Constants.KEY_RECORDS].append(record_retval)
    
        return retval
            