import time
import uuid

from google.cloud import bigquery
from google.cloud import storage
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery

from tmg.data import bq
from tmg.data import mysql
from tmg.data import ftp
from tmg.data._helper import merge_files
from tmg.data._helper import clean_mysql_export, get_bq_write_disposition
from tmg.data import logs



class Client:
    """
    Client to bundle transfers from a source to destination.

    Args:
        project (str): The Project ID for the project which the client acts on behalf of.
    """

    def __init__(self, project):
        self.project = project

    def bq_to_gs(self, table, bucket_name, separator=',', print_header=True):
        """Extract BigQuery table into the GoogleStorage

        Args:
            table (str):  The BigQuery table name. For example: ``my-project-id.you-dataset.my-table``
            bucket_name (str):  The name of the bucket in GoogleStorage.
            separator (:obj:`str`, optional): The separator. Defaults to :data:`,`.
            print_header (:obj:`boolean`, optional):  True to print a header row in the exported data otherwise False. Defaults to :data:`True`.

        Returns:
            list: The list of GoogleStorage paths for the uploaded files into the GoogleStorage.
            if the table is big, the exported files will be multiple.

        Examples:
            >>> from tmg.data import transfer
            >>> client = transfer.Client(project='my-project-id')
            >>> client.bq_to_gs('my-project-id.some_dataset.some_table', 'some-bucket-name')
        """

        project, dataset_id, table_id = table.split('.')
        dataset_ref = bigquery.DatasetReference(project=project, dataset_id=dataset_id)
        table_ref = bigquery.TableReference(dataset_ref, table_id=table_id)

        bq_client = bigquery.Client(project=self.project)
        logs.client.logger.info('Extracting from {table} to gs://{bucket_name}/{table_id}_*'.format(
            bucket_name=bucket_name, table_id=table_id, table=table)
        )
        extract_job = bq_client.extract_table(
            source=table_ref,
            destination_uris='gs://{bucket_name}/{table_id}_*'.format(bucket_name=bucket_name, table_id=table_id),
            job_config=bigquery.ExtractJobConfig(field_delimiter=separator, print_header=print_header)
        )
        extract_job.result()

        storage_client = storage.Client(project=self.project)
        logs.client.logger.info('Getting the list of available blobs in gs://{}'.format(bucket_name))
        blobs = storage_client.list_blobs(bucket_name)

        return ['gs://{}/{}'.format(bucket_name, blob.name) for blob in blobs]

    def gs_to_bq(self, gs_uri, table, auto_detect=True, skip_leading_rows=True, separator=',',
                 write_preference='append', schema=()):
        """Load file from Google Storage into the BigQuery table

        Args:
            gs_uri (str):  The Google Storage uri for the file. For example: ``gs://my_bucket_name/my_filename``.
            table (str): The BigQuery table name. For example: ``project.dataset.table``.
            auto_detect (boolean, Optional):  True if the schema should automatically be detected otherwise False. Defaults to :data:`True`.
            skip_leading_rows (boolean, Optional):  True to skip the first row of the file otherwise False. Defaults to :data:`True`.
            separator (str, Optional): The separator. Defaults to :data:`,`
            write_preference (str, Optional): The option to specify what action to take when you load data from a source file. Value can be on of
                                              ``'empty'``: Writes the data only if the table is empty.
                                              ``'append'``: Appends the data to the end of the table.
                                              ``'truncate'``: Erases all existing data in a table before writing the new data.
                                              Defaults to 'append'

            schema (tuple): The BigQuery table schema. For example: ``(('first_field','STRING'),('second_field', 'STRING'))``

        Examples:
            >>> from tmg.data import transfer
            >>> client = transfer.Client(project='my-project-id')
            >>> client.gs_to_bq(gs_uri='gs://my-bucket-name/my-filename',table='my-project-id.my_dataset.my_table')
        """

        project, dataset_id, table_id = table.split('.')
        dataset_ref = bigquery.DatasetReference(project=project, dataset_id=dataset_id)
        table_ref = bigquery.TableReference(dataset_ref, table_id=table_id)

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1 if skip_leading_rows else 0,
            autodetect=auto_detect,
            field_delimiter=separator,
            write_disposition=get_bq_write_disposition(write_preference)
        )

        if schema:
            job_config.schema = [bigquery.SchemaField(schema_field[0], schema_field[1]) for schema_field in schema]

        bigquery_client = bigquery.Client(project=self.project)
        logs.client.logger.info('Loading BigQuery table {} from {}'.format(table, gs_uri))
        job = bigquery_client.load_table_from_uri(gs_uri, table_ref, job_config=job_config)

        job.result()

    def bq_to_mysql(self, connection_string, bq_table, mysql_table):
        """Export from BigQuery table to MySQL table

        .. note:: The CloudSQL service account which can be found in Cloud SQL UI
              needs to have a storage object admin access.

        Args:
            connection_string (str): The MySQL connection string. For example: ``{my-username}:{my-password}@{mysql-host}:{mysql-port}/{my-database}``
            bq_table (str): The BigQuery table. For example: ``my-project-id.my-dataset.my-table``
            mysql_table (str):  The MySQL table. For example: ``my-mysql-database.my-table``

        Examples:
            >>> from tmg.data import transfer
            >>> client = transfer.Client(project='my-project-id')
            >>> client.bq_to_mysql(
            >>>     connection_string='{my-username}:{my-password}@{mysql-host}:{mysql-port}/{my-database}'
            >>>     bq_table='my-project-id.my-dataset.my-table'
            >>>     mysql_table='my-mysql-database.my-mysql-table'
            >>> )
        """

        # download the files locally
        bq_client = bq.Client(self.project)
        file_names = bq_client.download_table(bq_table, print_header=False)

        # merge the downloaded files
        if len(file_names) > 1:
            logs.client.logger.info('Merging {}'.format(','.join(file_names)))
            output_file_name = merge_files(file_names)
        else:
            output_file_name = file_names[0]

        # upload the merged file into mysql
        database, table = mysql_table.split(".")
        mysql_client = mysql.Client(connection_string)
        mysql_client.upload_table(file_path=output_file_name, database=database, table=table)

    def mysql_to_gs(self, instance_name, database, query, gs_uri):
        """Export from MySQL to Google Storage in CSV format

        .. note:: Be aware that the exported CSV file has "N as a field value when there is no value for that field.

        Args:
            instance_name (str): The CloudSQL instance name. It's the instance name in CloudSQL UI but without project.location
            database (str): The MySQL database name
            query (str): The query to get the data from MySQL
            gs_uri (str): The GoogleStorage uri. For example: ``gs://bucket_name/file_name``

        Examples:
            >>> from tmg.data import transfer
            >>> client = transfer.Client(project='my-project-id')
            >>> client.mysql_to_gs(
            >>>     instance_name='{my-mysql-instance-name}',
            >>>     database='my-database',
            >>>     query='SELECT * FROM my-table',
            >>>     gs_uri='gs://my-bucket-name/my-filename'
            >>> )
        """

        # make the discovery service
        credentials = GoogleCredentials.get_application_default()
        service = discovery.build('sqladmin', 'v1beta4', credentials=credentials)

        # make the request body
        instances_export_request_body = {
            "exportContext": {
                "fileType": "CSV",
                "uri": gs_uri,
                "databases": [database],
                "csvExportOptions": {
                    "selectQuery": query
                }
            }
        }

        # send the request and get the operation id
        logs.client.logger.info('Exporting from MySQL database {} with query "{}" to {}'.format(database, query, gs_uri))
        request = service.instances().export(
            project=self.project,
            instance=instance_name,
            body=instances_export_request_body
        )
        response = request.execute()
        operation_id = response['name']

        # wait until the job is done
        status = 'PENDING'
        while status in ['PENDING', 'RUNNING']:
            request = service.operations().get(project=self.project, operation=operation_id)
            status = request.execute()['status']
            time.sleep(2)  # Avoid to hammer the APIs (100queries per users every 100seconds is the maximum).

        if status != 'DONE':
            raise Exception('Failed to export data from MySQL, process status {}'.format(status))

    def mysql_to_bq(self, instance_name, database, query, bq_table, bq_table_schema, write_preference='append'):
        """Export from MySQL to BigQuery

        Args:
            instance_name (str): The CloudSQL instance name. It's the instance name in CloudSQL UI but without project.location
            database (str):  The MySQL database name
            query (str): The query to get the data from MySQL
            bq_table (str): The BigQuery table. For example: ``my-project-id.my-dataset.my-table``
            bq_table_schema (tuple): The BigQuery table schema. For example: ``(('first_field','STRING'),('second_field', 'STRING'))``
            write_preference (str, Optional): The option to specify what action to take when you load data from a source file. Value can be on of
                                              ``'empty'``: Writes the data only if the table is empty.
                                              ``'append'``: Appends the data to the end of the table.
                                              ``'truncate'``: Erases all existing data in a table before writing the new data.
                                              Defaults to 'append'

        Examples:
            >>> from tmg.data import transfer
            >>> client = transfer.Client(project='my-project-id')
            >>> client.mysql_to_bq(
            >>>     instance_name='{my-mysql-instance-name}',
            >>>     database='my-database',
            >>>     query='SELECT * FROM my-table',
            >>>     bq_table='my-project-id.my-dataset.my-table',
            >>>     bq_table_schema=(('first_field','STRING'),('second_field', 'STRING'))
            >>> )

        """

        # make the temp bucket
        storage_client = storage.Client(project=self.project)
        tmp_bucket_name = str(uuid.uuid4())
        logs.client.logger.info('Creating the temporary bucket {}'.format(tmp_bucket_name))
        tmp_bucket = storage_client.create_bucket(tmp_bucket_name, location='EU')
        tmp_file_name = str(uuid.uuid4())

        # export from mysql to temp bucket
        self.mysql_to_gs(
            instance_name=instance_name,
            database=database,
            query=query,
            gs_uri='gs://{}/{}.csv'.format(tmp_bucket_name, tmp_file_name)
        )

        # download the exported file from the temp bucket into local
        blob = tmp_bucket.blob('{}.csv'.format(tmp_file_name))
        logs.client.logger.info('Downloading {}'.format(blob.name))
        blob.download_to_filename('{}.csv'.format(tmp_file_name))

        # clean the file by replacing ,"N with space
        logs.client.logger.info('Cleaning the exported file {}.csv'.format(tmp_file_name))
        cleaned_file_name = clean_mysql_export('{}.csv'.format(tmp_file_name))

        # upload the cleaned file into BigQuery
        bq_client = bq.Client(project=self.project)
        bq_client.upload_table(
            file_path=cleaned_file_name,
            table=bq_table,
            auto_detect=False,
            schema=bq_table_schema,
            skip_leading_rows=False,
            write_preference=write_preference
        )

        # cleanup
        blob.delete()
        logs.client.logger.info('Deleting temporary bucket {}'.format(tmp_bucket_name))
        tmp_bucket.delete()

    def ftp_to_bq(self, ftp_connection_string, ftp_filepath, bq_table, separator=',',
                  skip_leading_rows=True, write_preference='append'):
        """Export from FTP to BigQuery

        Args:
            ftp_connection_string (str): The FTP connection string in the format {username}:{password}@{host}:{port}
            bq_table (str): The BigQuery table. For example: ``my-project-id.my-dataset.my-table``
            ftp_filepath (str): The path to the file to download.
            separator (:obj:`str`, optional): The separator. Defaults to :data:`,`.
            skip_leading_rows (boolean, Optional):  True to skip the first row of the file otherwise False. Defaults to :data:`True`.
            write_preference (str, Optional): The option to specify what action to take when you load data from a source file. Value can be on of
                                              ``'empty'``: Writes the data only if the table is empty.
                                              ``'append'``: Appends the data to the end of the table.
                                              ``'truncate'``: Erases all existing data in a table before writing the new data.
                                              Defaults to 'append'
        Examples:
            >>> from tmg.data import transfer
            >>> client = transfer.Client(project='my-project-id')
            >>> client.ftp_to_bq(
            >>>     ftp_connection_string='username:password@hots:port',
            >>>     ftp_filepath='/my-path/to-the-ftp-file',
            >>>     bq_table='my-project-id.my-dataset.my-table'
            >>> )

        """

        # download the ftp file
        ftp_client = ftp.Client(connection_string=ftp_connection_string)
        local_file = ftp_client.download_file(ftp_filepath)

        # upload the ftp file into BigQuery
        bq_cli = bq.Client(project=self.project)
        bq_cli.upload_table(
            file_path=local_file,
            table=bq_table,
            separator=separator,
            skip_leading_rows=skip_leading_rows,
            write_preference=write_preference
        )

    def bq_to_ftp(self, bq_table, ftp_connection_string, ftp_filepath, separator=',', print_header=True):

        """Export from BigQuery to FTP

        Args:
            bq_table (str): The BigQuery table. For example: ``my-project-id.my-dataset.my-table``
            ftp_connection_string (str): The FTP connection string in the format {username}:{password}@{host}:{port}
            ftp_filepath (str): The path to the file to download.
            separator (:obj:`str`, optional): The separator. Defaults to :data:`,`.
            print_header (boolean, Optional):  True to write header for the CSV file, otherwise False. Defaults to :data:`True`.

        Examples:
            >>> from tmg.data import transfer
            >>> client = transfer.Client(project='my-project-id')
            >>> client.bq_to_ftp(
            >>>     bq_table='my-project-id.my-dataset.my-table',
            >>>     ftp_connection_string='username:password@hots:port',
            >>>     ftp_filepath='/my-path/to-the-ftp-file'
            >>> )

        """
        # download the the BigQuery table into local
        bq_client = bq.Client(project=self.project)
        local_files = bq_client.download_table(
            table=bq_table,
            separator=separator,
            print_header=print_header
        )

        # merge the files if they are more than one
        if len(local_files) > 1:
            logs.client.logger.info('Merging {}'.format(','.join(local_files)))
            merged_file = merge_files(local_files)
        else:
            merged_file = local_files[0]

        # upload the merged file
        ftp_client = ftp.Client(connection_string=ftp_connection_string)
        ftp_client.upload_file(local_path=merged_file, remote_path=ftp_filepath)
