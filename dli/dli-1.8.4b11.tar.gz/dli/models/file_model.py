import contextlib
import os
import shutil
import ntpath
from urllib.parse import urljoin, urlparse

from dli.client.aspects import analytics_decorator, logging_decorator
from dli.client.components.urls import consumption_urls
from dli.models import log_public_functions_calls_using, AttributesDict


def flatten_s3_file_path(s3_path):
    path = urlparse(s3_path)[2]  # [scheme, netloc, path, ...]
    head, tail = ntpath.split(path)
    file = tail or ntpath.basename(head)
    return file


def get_or_create_os_path(s3_path: str, to: str, flatten: bool) -> str:
    if flatten:
        destination_key = flatten_s3_file_path(s3_path)
    else:
        destination_key = urlparse(s3_path).path.lstrip('/')

    to_path = os.path.join(
        to, os.path.normpath(destination_key)
    )

    to_path = os.path.abspath(to_path)

    if len(to_path) > 259 and os.name == 'nt':
        raise Exception(f"Apologies {s3_path} can't be downloaded "
                        f"as the file name would be too long. You "
                        f"may want to try calling again with "
                        f"Instance.download(flatten=True), which "
                        f"will put the file in a directory of your choice")

    else:
        directory, _ = os.path.split(to_path)
        os.makedirs(directory, exist_ok=True)

    return to_path


@log_public_functions_calls_using(
    [analytics_decorator, logging_decorator],
    class_fields_to_log=['datafile_id', 'path']
)
class FileModel(AttributesDict):

    @contextlib.contextmanager
    def open(self):
        response = self._client.session.get(
            urljoin(
                self._client._environment.consumption,
                consumption_urls.consumption_download.format(
                    id=self.datafile_id,
                    path=self.path
                )
            ),
            stream=True
        )
        # otherwise you get raw secure
        response.raw.decode_content = True
        yield response.raw
        response.close()

    def download(self, to='./', flatten=False):
        """
        Download one or more files and save them in the user specified
        directory.

        :param str to: The path on the system, where the files
            should be saved. Must be a directory, if doesn't exist, will be
            created.

        :param bool flatten: The default behaviour (=False) is to use the s3
            file structure when writing the downloaded files to disk. Example:
            [
              'storm/climate/storm_data/storm_fatalities/as_of_date=2019-09-10/type=full/StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',
              'storm/climate/storm_data/storm_fatalities/as_of_date=2019-09-10/type=full/StormEvents_details-ftp_v1.0_d1951_c20160223.csv.gz'
            ]

            When flatten = True, we remove the s3 structure. Example:

            Example output for new behaviour:
            [
              './storm-flattened/StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',
              './storm-flattened/StormEvents_details-ftp_v1.0_d1951_c20160223.csv.gz'
            ]

        :return: The path to the directory where the files were written.
        """

        # if flatten:
        #     c_path, filename = os.path.split(to_path)
        #     pd_path, as_of_date = os.path.split(c_path)
        #     pd_path = pd_path[2:].replace('/', '-')
        #     to_path = './{}-{}/{}'.format(pd_path, as_of_date[11:], filename)
        to_path = get_or_create_os_path(
            s3_path=self.path, to=to, flatten=flatten
        )

        print(f'Downloading {self.path} to: {to_path}...')

        with self.open() as download_stream:
            with open(to_path, 'wb') as target_download:
                # copyfileobj is just a simple buffered
                # file copy function with some sane
                # defaults and optimisations.
                shutil.copyfileobj(
                    download_stream, target_download
                )
                print(f'Completed download to: {to_path}.')

        return to_path
