from time import sleep

from .client_libs.data_wrappers import ZuoraExportQueryResult, ZuoraQueryJobResponse
from .client_libs.zuora_client_exceptions import (ZuoraExportQueryFormatError,
                                                  ZuoraExportQueryResultError)
from .zuora_basic_client import ZuoraBasicClient


class ZuoraClient(ZuoraBasicClient):

    @staticmethod
    def __prepare_export_query(zoql_queries):
        if not isinstance(zoql_queries, (list, tuple)):
            raise ZuoraExportQueryFormatError('Queries must be in a list or a tuple')

        query_base = {
            'format': 'csv',
            'version': '1.0',
            'name': 'queries',
            'encrypted': 'none',
            'dateTimeUtc': True,
            'queries': [
                {
                    'name': f'query{i}',
                    'query': q,
                    'type': 'zoqlexport'
                } for i, q in enumerate(zoql_queries)
            ]
        }
        return query_base

    def __send_batch_query(self, queries):
        q_url = f'/v1/batch-query/'
        query_data = self.__prepare_export_query(queries)
        batch_query = self.post(q_url, data=query_data).as_dict

        if batch_query['status'] in ('failed', 'error', 'cancelled'):
            raise ZuoraExportQueryResultError(batch_query)

        return batch_query['id']

    def __check_batch_query(self, batch_query_id):

        check_url = f'/v1/batch-query/jobs/{batch_query_id}'
        query_check = self.get(check_url).as_dict
        status = query_check['status']

        while status != 'completed':

            if self.query_retry_timeout > 0:
                sleep(self.query_retry_timeout)

            print('Waiting for the query to be completed...')
            query_check = self.get(check_url).as_dict
            status = query_check['status']
            print(f'Current status is {status}')

            if status in ('failed', 'error', 'cancelled'):
                raise ZuoraExportQueryResultError(query_check)

        else:
            return (x['fileId'] for x in query_check['batches'])

    def get_result_files(self, files_list):
        self.set_default_content_type()
        for file_id in files_list:
            f_url = f'/v1/files/{file_id}'
            file_resp = self.get(f_url)
            yield ZuoraExportQueryResult(file_resp.raw_data)

    def run_export_queries(self, queries=None):
        self.set_default_content_type()
        query_id = self.__send_batch_query(queries)
        file_id_list = self.__check_batch_query(query_id)
        return self.get_result_files(file_id_list)

    def get_invoice_by_id(self, invoice_id):
        self.set_default_content_type()
        resp = self.get(f'/v1/object/invoice/{invoice_id}')
        return resp.as_dict

    def update_invoice_by_id(self, invoice_id, data):
        self.set_default_content_type()
        url = f'/v1/object/invoice/{invoice_id}'
        resp = self.put(url, data=data)

        return resp.as_dict

    def update_account(self, account_id, data):
        self.set_default_content_type()
        url = f'/v1/accounts/{account_id}'
        resp = self.put(url, data=data)

        return resp.as_dict

    def update_credit_memo(self, credit_memo_id, data):
        self.set_default_content_type()
        url = f'/v1/creditmemos/{credit_memo_id}'
        resp = self.put(url, data=data)

        return resp.as_dict

    def cancel_credit_memo(self, memo_id):
        self.set_default_content_type()
        url = f'/v1/creditmemos/{memo_id}/cancel'
        resp = self.put(url)
        return resp.as_dict

    def get_accounting_periods(self):

        url = f'/v1/accounting-periods'
        resp = self.get(url)
        return resp.as_dict

    def get_sequences(self):

        url = f'/v1/sequence-sets'
        resp = self.get(url)
        return resp.as_dict

    def delete_sequence_set(self, sequence_set_id):

        url = f'/v1/sequence-sets/{sequence_set_id}'
        resp = self.delete(url)
        return resp.as_dict

    def run_query_job(self, query=None, output_format='JSON', custom_separator=None, compression='NONE'):
        if output_format not in ('JSON', 'CSV', 'TSV', 'DSV'):
            raise ZuoraExportQueryFormatError('Output format must be one of "JSON", "CSV", "TSV", "DSV"')
        self.set_default_content_type()
        url = f'/query/jobs'
        query_body = {
            'compression': compression,
            'output': {'target': 'S3'},
            'outputFormat': output_format,
            'query': query
        }
        status_check = self.post(f'{url}/', data=query_body).as_dict['data']
        status = status_check['queryStatus']

        while status != 'completed':
            if self.query_retry_timeout > 0:
                sleep(self.query_retry_timeout)
            status_check = self.get(f"{url}/{status_check['id']}").as_dict['data']
            status = status_check['queryStatus']

            if status in ('failed', 'error', 'cancelled'):
                raise ZuoraExportQueryResultError(status_check)
        else:
            return ZuoraQueryJobResponse(query_job_id=status_check['id'],
                                         output_format=output_format,
                                         custom_separator=custom_separator,
                                         items_num=status_check['outputRows'],
                                         response_url=status_check['dataFile'])

    def cancel_query_job(self, query_job_id):
        url = f'/query/jobs/{query_job_id}'
        return self.delete(url)

