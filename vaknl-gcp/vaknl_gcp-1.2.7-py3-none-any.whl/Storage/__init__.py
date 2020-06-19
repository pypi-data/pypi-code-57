__author__ = "Wytze Bruinsma"

import newlinejson as nlj
import random
import string
from google.cloud import storage

from vaknl_gcp.Bigquery import BigqueryClient
from vaknl_gcp.DataClasses import rec_to_json


class StorageClient(object):

    def __init__(self, project_id):
        self.project_id = project_id

        self.storage_client = storage.Client(project=project_id)
        self.bigquery_client = BigqueryClient(project_id=project_id)

        self.bucket_name = f'storage_to_bigquery-{self.project_id}'
        self.bucket = self.storage_client.get_bucket(self.bucket_name)

    def __rec_compose(self, blobs, blob_name, table_ref, write_disposition, n=0):
        """
        Recursive function that keeps composing blobs until there is one left

        Args:
            blobs: dataclasses to process
            blob_name: name of the blob to store data into
            table_ref: dataset_name.table_name
            n: compose iteration level
        """

        new_blobs = []
        for i in range(0, len(blobs), 32):
            composed_blob_name = f'composed/{n}:{i}_{blob_name}.json'
            self.bucket.blob(composed_blob_name).compose(blobs[i:i + 32])
            new_blobs.append(self.bucket.get_blob(composed_blob_name))

        for blob in blobs:
            blob.delete()

        if len(new_blobs) > 1:
            self.__rec_compose(new_blobs, blob_name, table_ref, write_disposition, n + 1)
        else:
            self.bigquery_client.write_disposition_bucket(blob_name=new_blobs[0].name, table_ref=table_ref,
                                                          write_disposition=write_disposition)
            for blob in new_blobs:
                blob.delete()

    def storage_to_bigquery(self, objects: list, table_ref, write_disposition, batch_size=5000, objects_name=None):
        """
        Function that stores data into multiple storage blobs. Afterwards these wil be composed into one storage blob.
        The reason for this process is to downsize the sie of the data send to Google Cloud Storage.

        Args:
            objects: dataclasses to process
            table_ref: dataset_name.table_name
            write_disposition: how to write to google bigquery
            batch_size: row size blobs will be created in google storage before they are composed and send to bigquery
            objects_name: name of the them objects stored in storage 
        """

        assert len(objects) > 0, 'List is empty. No data is send'

        if objects_name is None:
            objects_name = objects[0].__class__.__name__  # retrieve name of the first object
        random_string = ''.join(random.choice(string.ascii_lowercase) for _ in
                                range(12))  # Make blob_base_name unique so processes don't interact
        blob_base_name = f'{objects_name}_{random_string}'  # Generate a dynamic name from the object
        blobs = []

        # Create batches and store them in multiple blob files. Warning blob files can be to big for Bigquery.
        for i in range(0, len(objects), batch_size):
            batch = objects[i:i + batch_size]
            nl_json_batch = nlj.dumps(list(map(lambda x: rec_to_json(x), batch)))
            # Blobs will be stored in folder import
            blob = self.bucket.blob(f'import/{i}_{blob_base_name}.json')
            blobs.append(blob)
            blob.upload_from_string(nl_json_batch)

        self.__rec_compose(blobs=blobs, blob_name=blob_base_name, table_ref=table_ref,
                           write_disposition=write_disposition)

    def single_storage_to_bigquery(self, object, table_ref, write_disposition, batch_size=500, object_name=None):
        """
        Function that stores data into a storage blob. Then check if there are more than the batch_size. 
        If so it will compose similar blobs and send them to google bigquery.
        The reason for this process is to not stream single rows of data into bigquery but wait until there are more and than send them together.
        
        Args:            
            object: dataclass
            table_ref: dataset_name.table_name
            write_disposition: how to write to google bigquery
            batch_size: how many blobs until composing and sending to google bigquery
            object_name: name of the them object stored in storage 
        """
        if object_name is None:
            object_name = object.__class__.__name__  # retrieve name of the object
        blob_base_name = f'{object_name}_{generate_random_string()}'  # Generate a dynamic name from the object

        nl_json = nlj.dumps([rec_to_json(object)])
        blob = self.bucket.blob(f'import/{object_name}/{blob_base_name}.json')
        blob.upload_from_string(nl_json)

        blobs = self.list_blobs_with_prefix(bucket_name=self.bucket_name, prefix=f'import/{object_name}/')

        if len(blobs) > batch_size:
            self.__rec_compose(blobs=blobs, blob_name=f'{object_name}_{generate_random_string()}', table_ref=table_ref,
                               write_disposition=write_disposition)

    def get_blobs_from_bucket(self, bucket_name):
        """
        Args:
            bucket_name: bucket_name
        
        Return:
            list: blobs
        """
        return self.storage_client.list_blobs(bucket_name)

    def upload_from_string(self, blob, string):
        """
        Args:
            blob: blob
            string: data to write in the blob
        Return:
            string: url
        """
        blob.upload_from_string(string)
        return blob.public_url

    def get_bucket(self, bucket_name):
        """
        Args:
            string: bucket_name
        Return:
            string: url
        """
        return self.storage_client.get_bucket(bucket_name)

    def list_blobs_with_prefix(self, bucket_name, prefix, delimiter=None):
        """
        Lists all the blobs in the bucket that begin with the prefix.

        This can be used to list all blobs in a "folder", e.g. "public/".

        The delimiter argument can be used to restrict the results to only the
        "files" in the given "folder". Without the delimiter, the entire tree under
        the prefix is returned. For example, given these blobs:

            a/1.txt
            a/b/2.txt

        If you just specify prefix = 'a', you'll get back:

            a/1.txt
            a/b/2.txt

        However, if you specify prefix='a' and delimiter='/', you'll get back:

            a/1.txt

        Additionally, the same request will return blobs.prefixes populated with:

            a/b/

        Args:
            bucket_name: bucket_name
            prefix: string
            delimiter: string

        Return:
            list: blobs
        """

        blobs = self.storage_client.list_blobs(
            bucket_name, prefix=prefix, delimiter=delimiter
        )

        if delimiter:
            return [prefix for prefix in blobs.prefixes]
        else:
            return list(blobs)


def generate_random_string():
    """
    Make blob_base_name unique so processes don't interact

    Return:
        string: random string of characters
    """
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
