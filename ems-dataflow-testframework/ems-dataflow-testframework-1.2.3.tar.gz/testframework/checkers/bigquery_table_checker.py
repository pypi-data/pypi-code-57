import datetime

import inflection

from testframework.checkers.bigquery_checker import BigqueryChecker


class BigqueryTableChecker:

    def __init__(self, bigquery_checker: BigqueryChecker, dataset_name: str, table_name: str, checker_message_factory) -> None:
        self.bigquery_checker = bigquery_checker
        self.dataset_name = dataset_name
        self.table_name = table_name
        self.__checker_message_factory = checker_message_factory

    def common_table_has_row_for(self, event):
        return self.bigquery_checker.table_has_row_for(self.dataset_name, self.table_name, event)

    def customer_table_has_row_for(self, event):
        return self.bigquery_checker.table_has_row_for(self.dataset_name,
                                                       self.table_name + "_" + str(event["customer_id"]),
                                                       event)

    def common_table_returns_row_for(self, event):
        return self.bigquery_checker.table_returns_row_for(self.dataset_name,
                                                           self.table_name,
                                                           event)

    def customer_table_returns_row_for(self, event):
        return self.bigquery_checker.table_returns_row_for(self.dataset_name,
                                                           self.table_name + "_" + str(event["customer_id"]),
                                                           event)

    def has_waiting_row_for(self, event, event_type):
        now = datetime.datetime.utcnow()

        dataset_name = "dataflow_waiting_events"
        table_name = "waiting_events_*"

        waiting_event = self.__checker_message_factory.get_event_as_waiting(event, event_type)

        filter = "_TABLE_SUFFIX IN ('{}', '{}', '{}')".format(
            (now - datetime.timedelta(hours=1)).strftime("%Y%m%d_%H"),
            now.strftime("%Y%m%d_%H"),
            (now + datetime.timedelta(hours=1)).strftime("%Y%m%d_%H"),
        )
        regexp_template = ' AND REGEXP_CONTAINS(event_json, r".*{}.*")'
        for field_value in event.get_unique_fields().values():
            filter += regexp_template.format(field_value)

        return self.bigquery_checker.table_has_row_for(dataset_name, table_name, waiting_event, False, filter)

    def has_backup_row_for(self, topic, event):
        dataset_name = "dataflow_backup"
        table_name = inflection.underscore(topic)
        backup_event = self.__checker_message_factory.get_event_as_backup(event)

        return self.bigquery_checker.table_has_row_for(dataset_name, table_name, backup_event)

    def has_error_row_for(self, event, event_type_field, event_type):
        error_event = self.__checker_message_factory.get_event_as_error(event, event_type_field, event_type)

        regexp_template = ' AND REGEXP_CONTAINS(data, r".*{}.*")'
        filter_for_error_query = "TRUE "
        for field_value in event.get_unique_fields().values():
            filter_for_error_query += regexp_template.format(field_value)

        return self.bigquery_checker.table_has_row_for(self.dataset_name, self.table_name, error_event, where=filter_for_error_query, loaded_at_field="timestamp")
